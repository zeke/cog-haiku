from cog import BasePredictor, Input
from typing import Any
import time
import haiku
import random

class Predictor(BasePredictor):
    def setup(self):
      self.haikus = haiku.load_all()

    def predict(self, 
      seed: int = Input(description="A seed to always return the same result (optional, defaults to a random integer)", ge=0, default=None),
      progressive: bool = Input(description="Yield haiku words one at a time, sleepin between each word", default=False),
      sleep: float = Input(description="Time to sleep between each word (when using progressive output)", default=0.5),
      ) -> Any:
        if seed:
          haiku = self.haikus[seed % len(self.haikus)]
        else:
          haiku = random.choice(self.haikus)

        print("seed: ", seed)
        print("progressive: ", progressive)
        print("sleep: ", sleep)

        if progressive:
          for word in haiku.split():
            yield word
            time.sleep(sleep)
        else:
          return haiku