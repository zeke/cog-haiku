import random
import tempfile
import time
from pathlib import Path
from typing import Generator

from PIL import Image, ImageDraw, ImageFont

import haiku
from cog import BasePredictor, Input
from cog import Path as CogPath


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
      ) -> Generator[str, None, None]:

        haiku = self.get_haiku(seed)

        for word in haiku.split():
          yield word
          time.sleep(sleep)


class ImagePredictor(HaikuBasePredictor):
    """
    Return haiku as an image.
    """
    def predict(self, 
      seed: int = Input(description="A seed to always return the same result (optional)", ge=0, default=None)
      ) -> CogPath:
        haiku = self.get_haiku(seed)
        image_path = self.generate_image(haiku)
        return image_path

    def generate_image(self, text): 
      img = Image.new('RGB', (512, 512), color = (73, 109, 137))
      draw = ImageDraw.Draw(img)
      font = ImageFont.load_default()
      draw.text((10,10), text, font=font, fill=(255,255,0))
      output_path = Path(tempfile.mkdtemp()) / "haiku.png"
      img.save(output_path)
      return output_path