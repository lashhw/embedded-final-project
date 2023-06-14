import json
import subprocess
from geopy.geocoders import Nominatim


def get_current_address():
    lat, lon = get_gps_reading()

    geolocation = Nominatim(user_agent="geotest")
    location = geolocation.reverse(f"{lat}, {lon}")

    address = location.address.split(", ")
    address.pop(-2)
    address = "".join(address[::-1])

    return address


def get_gps_reading():
    out = subprocess.getoutput("gpspipe -x 5 -w | grep -m 1 lat")

    try:
        json_data = json.loads(out)
        return json_data["lat"], json_data["lon"]
    except:
        return None


if __name__ == "__main__":
    print(get_gps_reading())
