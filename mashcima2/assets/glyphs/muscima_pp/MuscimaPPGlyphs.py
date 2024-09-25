from ...AssetBundle import AssetBundle
from ...datasets.MuscimaPP import MuscimaPP
from .MppPage import MppPage
from .get_symbols import \
    get_full_noteheads, \
    get_empty_noteheads, \
    get_normal_barlines
from .SymbolRepository import SymbolRepository
from pathlib import Path
import pickle


class MuscimaPPGlyphs(AssetBundle):
    def __post_init__(self):
        self.muscima_pp = self.dependency_resolver.resolve_bundle(MuscimaPP)

    @property
    def symbol_repository_path(self) -> Path:
        return self.bundle_directory / "symbol_repository.pkl"
    
    def install(self):
        document_paths = list(
            self.muscima_pp.cropobjects_directory.glob("CVC-MUSCIMA_*-ideal.xml")
        )

        repository = SymbolRepository()

        # TODO: for each document
        for document_path in document_paths:
            print("Processing page:", document_path.name)

            page = MppPage.load(document_path)

            full_noteheads = get_full_noteheads(page)
            empty_noteheads = get_empty_noteheads(page)
            normal_barlines = get_normal_barlines(page)

            repository.full_noteheads += full_noteheads
            repository.empty_noteheads += empty_noteheads
            repository.normal_barlines += normal_barlines

            # TODO: this is dummy so that it does not take forever to regenerate
            if len(empty_noteheads) > 0:
                break
        
        # store all glyphs in a pickle that can then be loaded
        # on-request by a MPP glyph synthesizer
        with open(self.symbol_repository_path, "wb") as file:
            pickle.dump(repository, file)
            print("Writing...", self.symbol_repository_path)
    
    def load_symbol_repository(self) -> SymbolRepository:
        with open(self.symbol_repository_path, "rb") as file:
            repository = pickle.load(file)
        assert isinstance(repository, SymbolRepository)
        return repository


if __name__ == "__main__":
    print("Re-installing MUSCIMA++ glyphs...")
    from ...AssetRepository import AssetRepository
    from pathlib import Path
    assets = AssetRepository(Path("mashcima_assets"))
    assets.resolve_bundle(MuscimaPPGlyphs, force_install=True)
    print("Done.")
