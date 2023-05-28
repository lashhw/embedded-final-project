import json
import asyncio
from geopy.geocoders import Nominatim


async def get_current_address():
    lat, lon = get_gps_reading()

    geolocation = Nominatim(user_agent="geotest")
    location = geolocation.reverse(f"{lat}, {lon}")

    address = location.address.split(", ")
    address.pop(-2)
    address = "".join(address[::-1])

    return address


async def get_gps_reading():
    proc = await asyncio.create_subprocess_shell(
        "gpspipe -x 5 -w | grep -m 1 lat",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout, stderr = await proc.communicate()

    try:
        json_data = json.loads(stdout.decode())
        return json_data["lat"], json_data["lon"]
    except:
        return None


async def test():
    ret = await get_gps_reading()
    print(ret)


if __name__ == "__main__":
    asyncio.run(test())
