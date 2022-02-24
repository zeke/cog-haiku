import os
import subprocess

import numpy as np
from PIL import Image

from predict import ImagePredictor, ProgressivePredictor, StandardPredictor


def get_unique_colors(path):
    image = Image.open(path)
    image = image.resize((16, 16), resample=Image.NEAREST)
    image = image.convert("RGB")
    data = image.getdata()
    rgb_array = np.array(data)
    unique_colors = np.unique(rgb_array, axis=0)
    return unique_colors

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

class TestImagePredictor:
  def test_returns_image_path(self):
    p = ImagePredictor()
    p.setup()
    output_file = p.predict()
  
    if not os.environ.get('CI'):
      print(output_file)
      subprocess.run(['open', output_file], check=True)

    assert os.path.exists(output_file)

    # background should be black because no source image was provided
    unique_colors = get_unique_colors(output_file)
    assert [0, 0, 0] in unique_colors

  def test_gets_background_color_from_source_image(self):
      p = ImagePredictor()
      p.setup()
      source_image = "./fixtures/leaves.png"
      output_file = p.predict(source_image=source_image)
    
      if not os.environ.get('CI'):
        print(output_file)
        subprocess.run(['open', output_file], check=True)

      assert os.path.exists(output_file)

      # background should NOT be black because a source image was provided
      unique_colors = get_unique_colors(output_file)
      assert [47, 99, 55] in unique_colors
      # assert [0, 0, 0] not in unique_colors