import haiku

class TestHaiku:
  haikus = haiku.load_all()

  def test_load_all(self):

    assert type(self.haikus) == list
    assert len(self.haikus) > 4000

  def test_every_haiku_has_three_lines(self):
    for entry in self.haikus:
      assert entry.count("\n") == 2

  def test_every_haiku_is_trimmed(self):
    for entry in self.haikus:
      assert entry == entry.strip()