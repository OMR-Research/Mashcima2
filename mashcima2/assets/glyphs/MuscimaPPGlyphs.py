from ..AssetBundle import AssetBundle
from ..datasets.MuscimaPP import MuscimaPP


class MuscimaPPGlyphs(AssetBundle):
    def __post_init__(self):
        self.muscima_pp = self.dependency_resolver.resolve_bundle(MuscimaPP)
    
    def install(self):
        print("Running install...")
        pass
