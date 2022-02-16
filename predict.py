from cog import BasePredictor, Input
import haiku
import random

class Predictor(BasePredictor):
    def setup(self):
      self.haikus = haiku.load_all()

    def predict(self, 
      seed: int = Input(description="An optional random seed", ge=0, default=None)) -> str:
      if seed:
        return self.haikus[seed % len(self.haikus)]
      else:
        return random.choice(self.haikus)