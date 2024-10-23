import os
os.environ["MC_ASSETS_CACHE"] = "./smashcima_assets"

from smashcima.assets.AssetRepository import AssetRepository
from smashcima.assets.datasets.MuscimaPP import MuscimaPP
from smashcima.assets.glyphs.muscima_pp.MuscimaPPGlyphs import MuscimaPPGlyphs

repo = AssetRepository.default()

bundle = repo.resolve_bundle(MuscimaPPGlyphs, force_install=True)

repository = bundle.load_symbol_repository()
# repository = bundle.repository

glyph = repository.whole_notes[0]
print(glyph.space.inlinks)
