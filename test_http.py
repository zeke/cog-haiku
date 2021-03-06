from cog.server.http import create_app
from fastapi.testclient import TestClient

from cog import BasePredictor
from predict import ImagePredictor, Output, ProgressiveImagePredictor, ProgressivePredictor, StandardPredictor, MultiOutputPredictor


def make_client(predictor: BasePredictor, **kwargs) -> TestClient:
    app = create_app(predictor)
    with TestClient(app, **kwargs) as client:
        return client

def test_setup_is_called():
    class Predictor(BasePredictor):
        def setup(self):
            self.foo = "bar"

        def predict(self) -> str:
            return self.foo

    client = make_client(Predictor())
    resp = client.post("/predictions")
    assert resp.status_code == 200
    assert resp.json() == {"status": "succeeded", "output": "bar"}

class TestStandardPredictor:
  def test_with_seed(self):
      client = make_client(StandardPredictor())
      resp = client.post("/predictions", json={"input": {"seed": 123}})
      assert resp.status_code == 200
      assert resp.json() == {"status": "succeeded", "output": "from an open barn\nthe odor of hay and manure\nand climbing roses"}

  def test_without_seed(self):
      client = make_client(StandardPredictor())
      resp = client.post("/predictions")
      assert resp.status_code == 200
      output1 = resp.json()["output"]
      assert(len(output1) > 10)

      resp = client.post("/predictions")
      assert resp.status_code == 200
      output2 = resp.json()["output"]
      assert(len(output2) > 10)

      assert(output1 != output2)

class TestProgressivePredictor:
  def test_returns_last_yielded_output(self):
      client = make_client(ProgressivePredictor())
      resp = client.post("/predictions", json={"input": {"seed": 123}})
      assert resp.status_code == 200
      assert resp.json()["status"] == "succeeded"
      assert resp.json()["output"][0] == "from"
      assert resp.json()["output"][1] == "from an"
      assert resp.json()["output"][2] == "from an open"
      assert resp.json()["output"][3] == "from an open barn\n"
      assert resp.json()["output"][4] == "from an open barn\nthe"
      assert resp.json()["output"][-1] == "from an open barn\nthe odor of hay and manure\nand climbing roses"

class TestImagePredictor:
  def test_returns_an_image(self):
      client = make_client(ImagePredictor())
      resp = client.post("/predictions", json={"input": {"seed": 123}})
      assert resp.status_code == 200
      header, b64data = resp.json()["output"].split(",", 1)
      assert header == "data:image/png;base64"

class TestProgressiveImagePredictor:
  def test_returns_last_yielded_output(self):
      client = make_client(ProgressiveImagePredictor())
      resp = client.post("/predictions", json={"input": {"seed": 123}})
      assert resp.status_code == 200
      output = resp.json()["output"]

      assert type(output) == list
      assert len(output) > 1
      for i, img in enumerate(output):
          header, b64data = img.split(",", 1)
          assert header == "data:image/png;base64"
          assert len(b64data) > 0

class TestMultiOutputPredictor:
  def test_returns_multiple_outputs(self):
      client = make_client(MultiOutputPredictor())
      resp = client.post("/predictions", json={"input": {"seed": 123}})
      assert resp.status_code == 200
      output = resp.json()["output"]
      assert type(output) == dict
      assert list(output.keys()) == ["image", "text", "seed"]