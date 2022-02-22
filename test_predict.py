from predict import StandardPredictor, ProgressivePredictor


class TestStandardPredictor:
  def test_seed_always_returns_same_haiku(self):
    p = StandardPredictor()
    p.setup()
    output = p.predict(seed=123)
    assert "pear blossoms" in output

    output = p.predict(seed=123)
    assert "pear blossoms" in output

  def test_without_seed_returns_random_haiku(self):
    p = StandardPredictor()
    p.setup()
    output1 = p.predict(seed=None)
    assert isinstance(output1, str)

    output2 = p.predict(seed=None)
    assert isinstance(output2, str)

    assert output1 != output2

class TestProgressivePredictor:
  def test_seed_always_returns_same_haiku(self):
    p = ProgressivePredictor()
    p.setup()
    output = [result for result in p.predict(seed=123, sleep=0.1)]
    assert(len(output) == 9)
    assert(" ".join(output) == "from somewhere pear blossoms a curve in the road")

  def test_without_seed_returns_random_haiku(self):
    p = ProgressivePredictor()
    p.setup()
    output1 = [result for result in p.predict(sleep=0.01)]
    assert(len(output1) > 5)

    output2 = [result for result in p.predict(sleep=0.01)]
    assert(len(output2) > 5)
    
    assert output1 != output2