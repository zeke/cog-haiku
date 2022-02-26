from cog.server.http import create_app
from fastapi.testclient import TestClient

from cog import BasePredictor
from predict import ImagePredictor, ProgressivePredictor, StandardPredictor


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
    assert resp.json() == {"status": "success", "output": "bar"}

class TestStandardPredictor:
  def test_with_seed(self):
      client = make_client(StandardPredictor())
      resp = client.post("/predictions", json={"input": {"seed": 123}})
      assert resp.status_code == 200
      assert resp.json() == {"status": "success", "output": "from somewhere\npear blossoms\n\na curve in the road"}

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
      assert resp.json() == {"status": "success", "output": "road"} # last word

class TestImagePredictor:
  def test_returns_an_image(self):
      client = make_client(ImagePredictor())
      resp = client.post("/predictions", json={"input": {"seed": 123}})
      assert resp.status_code == 200
      header, b64data = resp.json()["output"].split(",", 1)
      assert header == "data:image/png;base64"