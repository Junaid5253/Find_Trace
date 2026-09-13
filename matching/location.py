import math
from functools import lru_cache

from geopy.geocoders import Nominatim


geolocator = Nominatim(
    user_agent="findtrace-missing-person-system"
)


@lru_cache(maxsize=500)
def geocode_location(location):
    """
    Convert a human-readable location into latitude/longitude
    using Nominatim (OpenStreetMap).
    """

    if not location:
        return None

    location = str(location).strip()

    if not location:
        return None

    try:
        result = geolocator.geocode(
            location,
            timeout=10
        )

        if result is None:
            return None

        return {
            "lat": result.latitude,
            "lng": result.longitude,
        }

    except Exception:
        return None


def haversine_distance_km(lat1, lon1, lat2, lon2):
    """
    Calculate the geographic distance between two coordinates.
    Returns distance in kilometers.
    """

    earth_radius = 6371.0

    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1)
        * math.cos(lat2)
        * math.sin(delta_lon / 2) ** 2
    )

    c = 2 * math.asin(math.sqrt(a))

    return earth_radius * c


def location_score(query, candidate):
    """
    Calculate geographic similarity between two locations.

    Returns a score between 0.0 and 1.0.

    1.0 = extremely close
    0.8 = relatively close
    0.5 = moderate distance
    0.0 = very far or unavailable
    """

    if not query or not candidate:
        return 0.0

    query_coordinates = geocode_location(str(query).strip())
    candidate_coordinates = geocode_location(str(candidate).strip())

    if not query_coordinates or not candidate_coordinates:
        return 0.0

    distance = haversine_distance_km(
        query_coordinates["lat"],
        query_coordinates["lng"],
        candidate_coordinates["lat"],
        candidate_coordinates["lng"],
    )

    if distance <= 2:
        return 1.00

    elif distance <= 5:
        return 0.95

    elif distance <= 10:
        return 0.90

    elif distance <= 25:
        return 0.80

    elif distance <= 50:
        return 0.68

    elif distance <= 100:
        return 0.50

    elif distance <= 250:
        return 0.30

    elif distance <= 500:
        return 0.15

    return 0.0