import random
import tempfile
import time
from typing import Iterator

from colorthief import ColorThief
from PIL import Image, ImageDraw, ImageFont

import haiku
from cog import BasePredictor, Input, Path

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

    def generate_image(self, text, color = (0, 0, 0)): 
      img = Image.new('RGB', (512, 512), color=color)
      draw = ImageDraw.Draw(img)
      font = ImageFont.load_default()
      draw.text((10,10), text, font=font, fill=(255,255,0))
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
        words = haiku.split(" ")
        for i,_word in enumerate(words):
          haiku_so_far = " ".join(words[0:i+1])
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
          color = ColorThief(source_image).get_color(quality=1)
        else:
          color = None

        image_path = self.generate_image(haiku, color=color)
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
          color = ColorThief(source_image).get_color(quality=1)
        else:
          color = None

        words = haiku.split(" ")
        for i,_word in enumerate(words):
          haiku_so_far = " ".join(words[0:i+1])
          image_path = self.generate_image(haiku_so_far, color=color)
          yield Path(image_path)
          time.sleep(sleep)