import os
os.environ["MC_ASSETS_CACHE"] = "./mashcima_assets"

from mashcima2.assets.AssetRepository import AssetRepository
from mashcima2.assets.datasets.MuscimaPP import MuscimaPP
from mashcima2.assets.glyphs.muscima_pp.MuscimaPPGlyphs import MuscimaPPGlyphs

repo = AssetRepository.default()

bundle = repo.resolve_bundle(MuscimaPPGlyphs, force_install=True)

repository = bundle.load_symbol_repository()
# repository = bundle.repository

glyph = repository.whole_notes[0]
print(glyph.space.inlinks)
