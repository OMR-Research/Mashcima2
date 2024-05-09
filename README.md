# Mashcima 2

A library and a framework for synthesizing images containing music, intended for use as training data for OMR models.


## A tutorial

> **Note:** The tool is under development and does not yet have a fixed public API. The tutorial is being developed and from it the whole tool is being built top-down.

To quickly learn how to start using Mashcima for your project, start with the tutorial.

[Mashcima Tutorial](docs/tutorial.md)


## How it works

Mashcima is not really a single tool, but more like a framework. To fully learn how to leverage its abilities, start by reading its documentation:

[Mashcima Documentation - Introduction](docs/introduction.md)


## After cloning

Create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
.venv/bin/pip3 install -r requirements.txt
```


## TODO list

The first milestone to hit is to convert Mashcima 1 into the modular structure of Mashcima 2, thereby settling most of its interfaces. The only additional logic is full-page synthesis.

- The `Scene` data model
    - The data model for the output of the synthesizer
    - Inspired by and closely tied to SVG
    - That can accomodate lots of different annotations (consider COCO compatibility)
    - Physically-based coordinate system (millimeters, DPI)
    - Aims to desribe one page of paper - one physical document
- Page synthesizer
    - creates a page of paper with stafflines
    - very crude to begin with, nothing complicated
- Staff sythesizer
    - the Mashcima 1, just modularized
- Symbol synthesizer
    - the Mashcima 1, just modularized
- Assets layer - `AssetBundle` as a "library" of assets
    - can download, process, and prepare external datasets to be used for the syntehsis process; this incudes trained ML models
    - Asset = a resource used during synthesis
- Symbolic logic
    - parsing & conversions of formats
    - MusicXML as the primary input format
    - generation of synthetic music