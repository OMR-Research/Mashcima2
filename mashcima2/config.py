import os
from pathlib import Path


# cache location
# (inspired by https://github.com/huggingface/datasets)
DEFAULT_XDG_CACHE_HOME = "~/.cache"
XDG_CACHE_HOME = os.getenv("XDG_CACHE_HOME", DEFAULT_XDG_CACHE_HOME)
DEFAULT_MC_CACHE_HOME = os.path.join(XDG_CACHE_HOME, "mashcima2")
MC_CACHE_HOME = os.path.expanduser(os.getenv("HF_HOME", DEFAULT_MC_CACHE_HOME))

# default asset repository path
DEFAULT_MC_ASSETS_CACHE = os.path.join(MC_CACHE_HOME, "assets")
MC_ASSETS_CACHE = Path(os.getenv("MC_ASSETS_CACHE", DEFAULT_MC_ASSETS_CACHE))
