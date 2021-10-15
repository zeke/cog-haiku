# Cog Kitchen Sink

This repo is for testing out [Cog](https://github.com/replicate/cog) containers for machine learning.

## Tests

Cog isn't published to PyPi yet. You'll need a local git checkout:

```sh
git clone https://github.com/replicate/cog
cd cog/python
python setup.py develop
```

Then:

```sh
pytest -s
```