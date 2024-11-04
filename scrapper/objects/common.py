from typing import Optional, Tuple
from OSMPythonTools.nominatim import Nominatim


def get_coordinates_by_address(address: str) -> Optional[Tuple[float, float]]:
    nominatim = Nominatim()
    result = nominatim.query(address)
    
    if result is not None:
        lat = result.latitude
        lon = result.longitude
        return lat, lon
    else:
        return None