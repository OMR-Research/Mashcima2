from pathlib import Path


class AssetRepository:
    """A folder on the local machine, where asset bundles are downloaded to
    and prepared"""
    
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
        """Returns the default asset repository to use for a python project"""
        return AssetRepository(
            # kinda like "node_modules" for npm
            Path.cwd() / "mashcima_assets"
        )
