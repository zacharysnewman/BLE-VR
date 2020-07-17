import json
import asyncio
from bleak import BleakScanner


async def run():
    devices = await BleakScanner.discover()

    for d in devices:
        # deviceName = str(d).split(": ")[1]
        # if deviceName == "BLE VR Sensor":
        print(d)

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
