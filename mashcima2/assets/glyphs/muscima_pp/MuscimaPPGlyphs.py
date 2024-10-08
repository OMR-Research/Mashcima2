from ...AssetBundle import AssetBundle
from ...datasets.MuscimaPP import MuscimaPP
from .MppPage import MppPage
from .get_symbols import \
    get_full_noteheads, \
    get_empty_noteheads, \
    get_normal_barlines, \
    get_whole_rests, \
    get_half_rests, \
    get_quarter_rests, \
    get_eighth_rests, \
    get_sixteenth_rests, \
    get_g_clefs, \
    get_f_clefs, \
    get_c_clefs
from .SymbolRepository import SymbolRepository
from pathlib import Path
import pickle
from tqdm import tqdm


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

        for document_path in tqdm(document_paths):
            page = MppPage.load(document_path)

            repository.add_glyphs(get_full_noteheads(page))
            repository.add_glyphs(get_empty_noteheads(page))
            repository.add_glyphs(get_normal_barlines(page))
            repository.add_glyphs(get_whole_rests(page))
            repository.add_glyphs(get_half_rests(page))
            repository.add_glyphs(get_quarter_rests(page))
            repository.add_glyphs(get_eighth_rests(page))
            repository.add_glyphs(get_sixteenth_rests(page))
            repository.add_glyphs(get_g_clefs(page))
            repository.add_glyphs(get_f_clefs(page))
            repository.add_glyphs(get_c_clefs(page))

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
