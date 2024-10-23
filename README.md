# Smashcima

A library and a framework for synthesizing images containing music, intended for use as training data for OMR models.


## A tutorial

> **Note:** The tool is under development and does not yet have a fixed public API. The tutorial is being developed and from it the whole tool is being built top-down.

To quickly learn how to start using Smashcima for your project, start with the tutorial.

[Smashcima Tutorial](docs/tutorial.md)


## How it works

Smashcima is not really a single tool, but more like a framework. To fully learn how to leverage its abilities, start by reading its documentation:

[Smashcima Documentation - Introduction](docs/introduction.md)


## After cloning

Create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
.venv/bin/pip3 install -e .

# to run jupyter notebooks:
.venv/bin/pip3 install -e .[jupyter]
```


## Packaging and development notes

- Read this: https://packaging.python.org/en/latest/tutorials/packaging-projects/
- Package configuration inspired by this: https://github.com/vega/altair/blob/main/pyproject.toml
- For development setup inspiration check out: https://altair-viz.github.io/getting_started/installation.html#development-installation
- jupyter notebooks in git: https://mg.readthedocs.io/git-jupyter.html
- deploying voila: https://voila.readthedocs.io/en/stable/deploy.html
