from ...AssetBundle import AssetBundle
from ...datasets.MuscimaPP import MuscimaPP
from .MppPage import MppPage
from .get_symbols import get_whole_notes


class MuscimaPPGlyphs(AssetBundle):
    def __post_init__(self):
        self.muscima_pp = self.dependency_resolver.resolve_bundle(MuscimaPP)
    
    def install(self):
        document_paths = list(
            self.muscima_pp.cropobjects_directory.glob("CVC-MUSCIMA_*-ideal.xml")
        )

        # TODO: for each document
        for document_path in document_paths:
            page = MppPage.load(document_path)

            whole_notes = get_whole_notes(page)
            print(whole_notes)

            if len(whole_notes) > 0:
                break
        
        # TODO: store all glyphs in a pickle that can then be loaded
        # on-request by a MPP glyph synthesizer
