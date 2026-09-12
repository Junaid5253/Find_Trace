import math
import os
import requests


def geocode_location(location):
    """Convert a human-readable location into latitude/longitude using Google Maps."""
    if not location:
        return None

    api_key = os.getenv("GOOGLE_MAPS_API_KEY")

    if not api_key:
        try:
            import streamlit as st
            api_key = st.secrets.get("GOOGLE_MAPS_API_KEY")
        except Exception:
            api_key = None

    if not api_key:
        return None

    try:
        response = requests.get(
            "https://maps.googleapis.com/maps/api/geocode/json",
            params={
                "address": location,
                "key": api_key,
            },
            timeout=10,
        )

        response.raise_for_status()
        data = response.json()

        if data.get("status") != "OK" or not data.get("results"):
            return None

        coordinates = data["results"][0]["geometry"]["location"]

        return {
            "lat": coordinates["lat"],
            "lng": coordinates["lng"],
        }

    except Exception:
        return None


def haversine_distance_km(lat1, lon1, lat2, lon2):
    """Calculate the real geographic distance between two coordinates."""

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
    0.0 = very far / unavailable
    """

    if not query or not candidate:
        return 0.0

    query_coordinates = geocode_location(query)
    candidate_coordinates = geocode_location(candidate)

    if not query_coordinates or not candidate_coordinates:
        return 0.0

    distance = haversine_distance_km(
        query_coordinates["lat"],
        query_coordinates["lng"],
        candidate_coordinates["lat"],
        candidate_coordinates["lng"],
    )

    # Geographic evidence scoring
    if distance <= 2:
        return 1.00

    if distance <= 5:
        return 0.95

    if distance <= 10:
        return 0.90

    if distance <= 25:
        return 0.80

    if distance <= 50:
        return 0.68

    if distance <= 100:
        return 0.50

    if distance <= 250:
        return 0.30

    if distance <= 500:
        return 0.15

    return 0.0