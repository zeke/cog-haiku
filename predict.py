import random
import tempfile
import time
from typing import Iterator

from colorthief import ColorThief
from PIL import Image, ImageDraw, ImageFont

import haiku
from cog import BasePredictor, BaseModel, Input, Path

def haiku_to_words(haiku):
  return haiku.replace("\n", "\n ").split(" ")

class HaikuBasePredictor(BasePredictor):
    """
    Base predictor from which Standard and Progressive predictors inherit
    """
    def setup(self):
      self.haikus = haiku.load_all()

    def get_haiku(self, seed: int = None) -> str:
      if seed and type(seed) == int:
        return self.haikus[seed % len(self.haikus)]
      
      return random.choice(self.haikus)

    def generate_image(self, text, text_color=None, bg_color = None) -> Path:

      if not bg_color:
        bg_color = 'papayawhip'

      if not text_color:
        text_color = 'indianred'

      width = 512
      height = 200
      img = Image.new('RGB', (width, height), color=bg_color)
      draw = ImageDraw.Draw(img)
      font = ImageFont.truetype("fonts/CedarvilleCursive-Regular.ttf", 32)
      draw.text((30,25), text, font=font, fill=text_color)
      output_path = Path(tempfile.mkdtemp()) / "haiku.png"
      img.save(output_path)

      return output_path


class StandardPredictor(HaikuBasePredictor):
    """
    Return haiku as a single string.
    """
    def predict(self, 
      seed: int = Input(description="A seed to always return the same result (optional)", ge=0, default=None)
      ) -> str:
        haiku = self.get_haiku(seed)
        return haiku

class ProgressivePredictor(HaikuBasePredictor):
    """
    Yield haiku as progressive output, one word at a time.
    """
    def predict(self, 
      seed: int = Input(description="A seed to always return the same result (optional)", ge=0, default=None),
      sleep: float = Input(description="Time to sleep between each word (when using progressive output)", default=0.1),
      ) -> Iterator[str]:

        haiku = self.get_haiku(seed)
        words = haiku_to_words(haiku)
        for i,_word in enumerate(words):
          haiku_so_far = " ".join(words[0:i+1]).replace("\n ", "\n")
          yield haiku_so_far
          time.sleep(sleep)


class ImagePredictor(HaikuBasePredictor):
    """
    Return haiku as an image.
    """
    def predict(self, 
      seed: int = Input(description="A seed to always return the same result (optional)", ge=0, default=None),
      source_image: Path = Input(description="An image from which to derive a background color for the output image (optional)", default=None),
      ) -> Path:
        haiku = self.get_haiku(seed)

        # extract dominant color from source image for use in output image
        if source_image and type(source_image) == str:
          bg_color = ColorThief(source_image).get_color(quality=1)
        else:
          bg_color = None

        image_path = self.generate_image(haiku, bg_color=bg_color)
        return image_path


class ProgressiveImagePredictor(HaikuBasePredictor):
    """
    Yield haiku as progressive output images, one word at a time.
    """
    def predict(self, 
      seed: int = Input(description="A seed to always return the same result (optional)", ge=0, default=None),
      sleep: float = Input(description="Time to sleep between each word (when using progressive output)", default=0.1),
      source_image: Path = Input(description="An image from which to derive a background color for the output image (optional)", default=None),
      ) -> Iterator[Path]:

        haiku = self.get_haiku(seed)

        # extract dominant color from source image for use in output image
        if source_image and type(source_image) == str:
          bg_color = ColorThief(source_image).get_color(quality=1)
        else:
          bg_color = None

        words = haiku_to_words(haiku)
        for i,_word in enumerate(words):
          haiku_so_far = " ".join(words[0:i+1]).replace("\n ", "\n")
          image_path = self.generate_image(haiku_so_far, bg_color=bg_color)
          yield Path(image_path)
          time.sleep(sleep)


class Output(BaseModel):
    # These are intentionally not in alphabetical order, so we know that the order is preserved
    image: Path
    text: str
    seed: int

class MultiOutputPredictor(HaikuBasePredictor):
    """
    Return haiku as an image and text (plus the seed).
    """
    def predict(self, 
      seed: int = Input(description="A seed to always return the same result (optional)", ge=0, default=None),
      source_image: Path = Input(description="An image from which to derive a background color for the output image (optional)", default=None),
      ) -> Output:
        # this predictor returns `seed`` as part of its output, so it cannot be None
        if not seed:
          seed = random.randrange(0, len(self.haikus))

        haiku = self.get_haiku(seed)

        # extract dominant color from source image for use in output image
        if source_image and type(source_image) == str:
          bg_color = ColorThief(source_image).get_color(quality=1)
        else:
          bg_color = None

        image_path = self.generate_image(haiku, bg_color=bg_color)

        return Output(text=haiku, image=image_path, seed=seed)