import abc
from pathlib import Path
import shutil
import json


BUNDLE_FILENAME = "bundle.json"


class AssetBundle(abc.ABC):
    """
    Base class representing an asset bundle.
    
    Asset is any piece of external data, which can be used during syntehsis.
    This can be a MUSCIMA++ symbol mask, trained generative ML model,
    or some aggregated distribution.

    Asset bundle is a group of these assets that is downloaded, unpacked,
    and used as a single unit. It is a "library of assets".
    """
    def __init__(self, bundle_directory: Path):
        assert isinstance(bundle_directory, Path)
        self.bundle_directory = bundle_directory
        "Path to the directory where the bundle should be installed"

    @abc.abstractmethod
    def install(self):
        """Downloads and installs the bundle into the bundle directory."""
        raise NotImplementedError
    
    def remove(self):
        """Removes the bundle from the asset repository folder"""
        shutil.rmtree(self.bundle_directory, ignore_errors=True)
        assert not self.bundle_directory.exists()
    
    def write_metadata(self):
        """Writes the metadata file for the bundle"""
        metadata = {
            # more metadata can be added in the future,
            # such as install datetime, install mashcima version, etc.
            "installed": True
        }
        with open(self.bundle_directory / BUNDLE_FILENAME, "w") as f:
            json.dump(metadata, f)
    
    def metadata_exists(self) -> bool:
        """Returns true if the metadata file exists for the bundle"""
        return (self.bundle_directory / BUNDLE_FILENAME).is_file()
