import OSMPythonTools
import OSMPythonTools.nominatim

from typing import Optional, Tuple
from OSMPythonTools.nominatim import Nominatim


def get_coordinates_by_address(address: str) -> Optional[Tuple[float, float]]:
    nominatim = Nominatim()
    result: OSMPythonTools.nominatim.NominatimResult = nominatim.query(address)
    
    if result is not None:
        if len(result.toJSON()) == 0:
            return None
        
        json_data: dict = result.toJSON()[0]
        lat = json_data.get("lat", 0.0)
        lon = json_data.get("lon", 0.0)
        return lat, lon
    else:
        return None
