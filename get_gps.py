import json
import asyncio


async def get_gps():
    proc = await asyncio.create_subprocess_shell(
        "gpspipe -x 5 -w | grep -m 1 lat",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await proc.communicate()

    try:
        json_data = json.loads(stdout.decode())
        return json_data["lat"], json_data["lon"]
    except:
        return None


async def test():
    ret = await get_gps()
    print(ret)


if __name__ == "__main__":
    asyncio.run(test())
