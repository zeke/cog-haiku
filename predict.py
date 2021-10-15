import cog
import haiku
import random

class Predictor(cog.Predictor):
    def setup(self):
      self.haikus = haiku.load_all()

    @cog.input("seed", type=int, help="An optional random seed", min=0, max=1000, default=None)
    def predict(self, seed):
      if seed:
        return self.haikus[seed]
      else:
        return random.choice(self.haikus)