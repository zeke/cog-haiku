# Cog Haiku

A project that generates haiku for testing out [Cog](https://github.com/replicate/cog) containers for machine learning.

## Predictors

This repo contains several Cog predictors, each of which is published as a model on Replicate.

- [replicate.com/zeke/haiku-standard](https://replicate.com/zeke/haiku-standard) returns a haiku string.
- [replicate.com/zeke/haiku-progressive](https://replicate.com/zeke/haiku-standard) yields a haiku string, one word at a time.
- [replicate.com/zeke/haiku-image](https://replicate.com/zeke/haiku-standard) return a haiku image.

## Tests

```sh
script/test
```