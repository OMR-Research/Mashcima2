from .LineGlyph import LineGlyph
from dataclasses import dataclass


@dataclass
class LedgerLine(LineGlyph):
    """Ledger line (visual), extending the stafflines outside their range"""
    pass
