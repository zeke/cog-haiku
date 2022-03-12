# Cog Haiku

A project that generates haiku for testing out [Cog](https://github.com/replicate/cog) containers for machine learning.

This model is using the [pydantic version of Cog](https://github.com/replicate/cog/releases/tag/v0.1.0).

## Predictors

This repo contains several Cog predictors, each of which is published as a model on Replicate.

- [replicate.com/zeke/haiku-standard](https://replicate.com/zeke/haiku-standard) returns a haiku string.
- [replicate.com/zeke/haiku-progressive](https://replicate.com/zeke/haiku-standard) yields a haiku string, one word at a time.
- [replicate.com/zeke/haiku-image](https://replicate.com/zeke/haiku-standard) return a haiku image.

## Tests

```sh
script/test
```

## Server

```sh
script/server
```

- http://localhost:5000
- http://localhost:5000/docs
- http://localhost:5000/openapi.json

## Release

To push a model to Replicate:

1. uncomment the appropriate `image` / `predict` pair in [cog.yaml](cog.yaml)
1. `cog push`