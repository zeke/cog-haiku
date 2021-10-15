from predict import Predictor

def test_seed_always_returns_same_haiku():
  p = Predictor()
  p.setup()
  output = p.predict(seed=123)
  assert "pear blossoms" in output

  output = p.predict(seed=123)
  assert "pear blossoms" in output

def test_without_seed_returns_random_haiku():
  p = Predictor()
  p.setup()
  output1 = p.predict(seed=None)
  assert isinstance(output1, str)

  output2 = p.predict(seed=None)
  assert isinstance(output2, str)

  assert output1 != output2