import abc
from pathlib import Path
import shutil
import json
from typing import TypeVar, Type


T = TypeVar("T", bound="AssetBundle")


class BundleResolver(abc.ABC):
    """Interface representing something that can resolve asset bundles"""
    
    @abc.abstractmethod
    def resolve_bundle(self, bundle_type: Type[T]) -> T:
        """Ensures that a bundle is installed and returns its instance"""
        raise NotImplementedError


BUNDLE_META_FILE = "bundle.json"


class AssetBundle(abc.ABC):
    """
    Base class representing an asset bundle.
    
    Asset is any piece of external data, which can be used during syntehsis.
    This can be a MUSCIMA++ symbol mask, trained generative ML model,
    or some aggregated distribution.

    Asset bundle is a group of these assets that is downloaded, unpacked,
    and used as a single unit. It is a "library of assets".
    """
    def __init__(
        self,
        bundle_directory: Path,
        dependency_resolver: BundleResolver
    ):
        assert isinstance(bundle_directory, Path)
        self.bundle_directory = bundle_directory
        "Path to the directory where the bundle should be installed"

        self.dependency_resolver = dependency_resolver
        "Use this to resolve additional bundle dependencies"

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
            # such as install datetime, install smashcima version, etc.
            "installed": True
        }
        with open(self.bundle_directory / BUNDLE_META_FILE, "w") as f:
            json.dump(metadata, f)
    
    def metadata_exists(self) -> bool:
        """Returns true if the metadata file exists for the bundle"""
        return (self.bundle_directory / BUNDLE_META_FILE).is_file()
