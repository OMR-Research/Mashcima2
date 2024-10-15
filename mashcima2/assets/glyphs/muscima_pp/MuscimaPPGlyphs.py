from ...AssetBundle import AssetBundle
from ...datasets.MuscimaPP import MuscimaPP
from mashcima2.rendering.DebugGlyphRenderer import DebugGlyphRenderer
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
from .MppGlyphMetadata import MppGlyphMetadata
from pathlib import Path
import pickle
from tqdm import tqdm
import shutil
import cv2


class MuscimaPPGlyphs(AssetBundle):
    def __post_init__(self):
        self.muscima_pp = self.dependency_resolver.resolve_bundle(MuscimaPP)

    @property
    def symbol_repository_path(self) -> Path:
        return self.bundle_directory / "symbol_repository.pkl"
    
    def install(self):
        """Extracts data from the MUSCIMA++ dataset and bundles it up
        in the symbol repository in a pickle file."""
        document_paths = list(
            self.muscima_pp.cropobjects_directory.glob("CVC-MUSCIMA_*-ideal.xml")
        )

        repository = SymbolRepository()

        # go through all the MUSCIMA++ XML files
        for document_path in tqdm(document_paths):
            page = MppPage.load(document_path)

            # and extract glyphs
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

            # TODO: and extract lines

            # TODO: and extract distributions

        # dump the repository into a pickle file
        with open(self.symbol_repository_path, "wb") as file:
            pickle.dump(repository, file)
            print("Writing...", self.symbol_repository_path)
    
    def load_symbol_repository(self) -> SymbolRepository:
        """Loads the symbol repository from its pickle file"""
        with open(self.symbol_repository_path, "rb") as file:
            repository = pickle.load(file)
        assert isinstance(repository, SymbolRepository)
        return repository
    
    def build_debug_folder(self):
        """Creates a debug folder in the bundle folder, where it dumps
        all the extracted glyphs for visual inspection."""
        repository = self.load_symbol_repository()
        
        debug_folder = self.bundle_directory / "debug"
        shutil.rmtree(debug_folder, ignore_errors=True)
        debug_folder.mkdir()

        # glyphs
        glyph_renderer = DebugGlyphRenderer()
        for glyph_class, glyphs in repository.glyphs_by_class.items():
            glyphs_folder = debug_folder / glyph_class.replace(":", "-")
            glyphs_folder.mkdir()

            print(glyph_class, "...")
            for glyph in tqdm(glyphs):
                meta = MppGlyphMetadata.of_glyph(glyph, fail_if_none=True)
                cv2.imwrite(
                    str(glyphs_folder / (meta.mpp_crop_object_uid + ".png")),
                    glyph_renderer.render(glyph)
                )


if __name__ == "__main__":
    from ...AssetRepository import AssetRepository
    from pathlib import Path
    import sys
    
    assets = AssetRepository(Path("mashcima_assets"))

    print("Re-installing MUSCIMA++ glyphs...")
    bundle = assets.resolve_bundle(MuscimaPPGlyphs, force_install=True)
    # bundle = assets.resolve_bundle(MuscimaPPGlyphs) # TODO: DEBUG
    
    if sys.argv[1] == "--debug":
        print("Building the debug folder...")
        bundle.build_debug_folder()

    print("Done.")
