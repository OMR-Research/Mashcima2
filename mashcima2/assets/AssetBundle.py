import abc


class AssetBundle(abc.ABC):
    """
    Base class representing an asset bundle.
    
    Asset is any piece of external data, which can be used during syntehsis.
    This can be a MUSCIMA++ symbol mask, trained generative ML model,
    or some aggregated distribution.

    Asset bundle is a group of these assets that is downloaded, unpacked,
    and used as a single unit. It is a "library of assets".
    """
    pass
