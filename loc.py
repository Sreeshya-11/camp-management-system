import requests
from geopy.geocoders import Nominatim

def get_location_from_ip():
    try:
        ip_data = requests.get("https://ipinfo.io/json").json()
        location = ip_data.get("loc", "")  # Latitude,Longitude
        if location:
            latitude, longitude = map(float, location.split(","))
            geolocator = Nominatim(user_agent="geoapiExercises")
            address = geolocator.reverse((latitude, longitude), language="en")
            return {
                "ip": ip_data.get("ip"),
                "city": ip_data.get("city"),
                "region": ip_data.get("region"),
                "country": ip_data.get("country"),
                "latitude": latitude,
                "longitude": longitude,
                "address": address.address if address else "Unknown Address"
            }
    except Exception as e:
        return {"error": str(e)}

print(get_location_from_ip())
