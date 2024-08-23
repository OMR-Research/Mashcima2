from pathlib import Path
from typing import TypeVar, Type
from .AssetBundle import AssetBundle
from ..config import MC_ASSETS_CACHE


T = TypeVar("T", bound=AssetBundle)


class AssetRepository:
    """
    A folder on the local machine, where asset bundles are downloaded to
    and prepared. It also acts as the manager that installs and resolves
    asset bundles from this folder.
    """
    
    def __init__(self, path: Path):
        if path.exists() and not path.is_dir():
            raise Exception(
                f"The path at {path} has to be a directory or be non-existing."
            )
        
        self.path = path
        "Path to the asset repository folder"

        self.path.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def default() -> "AssetRepository":
        """Returns the default asset repository to use this process"""
        return AssetRepository(
            Path(MC_ASSETS_CACHE).resolve()
        )
    
    def resolve_bundle(self, bundle_type: Type[T]) -> T:
        """Ensures that a bundle is installed and returns its instance"""
        # instantiate the bundle
        bundle = bundle_type(
            bundle_directory=self.path / bundle_type.__name__
        )

        # do nothing if already installed
        if bundle.metadata_exists():
            return bundle
        
        print(f"[Mashcima Assets]: Installing bundle {bundle_type.__name__}...")

        # clear its directory
        bundle.remove()
        bundle.bundle_directory.mkdir()

        # run the installation
        bundle.install()

        # store metadata
        bundle.write_metadata()

        print(f"[Mashcima Assets]: Bundle {bundle_type.__name__} installed.")

        return bundle
