# Mashcima 2

A library and a framework for synthesizing images containing music, intended for use as training data for OMR models.


## Plan for the first release

Coerce the old Mashcima 1 into a modular format similar to how NLTK is deisgned and then extend it with additional functionality.

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
