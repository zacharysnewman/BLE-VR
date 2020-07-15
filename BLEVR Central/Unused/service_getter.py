"""
Service Explorer
----------------

An example showing how to access and print out the services, characteristics and
descriptors of a connected GATT server.

Created on 2019-03-25 by hbldh <henrik.blidh@nedomkull.com>

"""
import platform
import asyncio
import logging
import struct
import json
from bleak import BleakClient, BleakScanner


async def run(address, loop):
    async with BleakClient(address, loop=loop, timeout=1) as client:
        isClientConnected = await client.is_connected()
        #     print("Connected: {0}".format(isClientConnected))

        # if not isClientConnected:
        #     print("Connected: {0}".format(isClientConnected))
        #     return None

        pitch = bytes(await client.read_gatt_char("42EA697D-7DF9-4356-A35F-5765A37F788E".lower()))
        roll = bytes(await client.read_gatt_char("D11D3A7F-0B36-4B7D-B646-948A016583F8".lower()))
        yaw = bytes(await client.read_gatt_char("B0158511-E858-4877-823C-AA032A8D67F1".lower()))
        deltaTime = bytes(await client.read_gatt_char("172F4F16-9D0C-47EC-89BC-D8CC41A1D993".lower()))

        sensorDataDict = {
            "uuid": address,
            "angle": {
                "x": struct.unpack('f', pitch)[0],
                "y": struct.unpack('f', roll)[0],
                "z": struct.unpack('f', yaw)[0]
            },
            "deltaTime": struct.unpack('f', deltaTime)[0]
        }

        jsonData = json.dumps(sensorDataDict)
        # print(jsonData)

        return jsonData


# How to use
if __name__ == "__main__":
    address = (  # 1
        "24:71:89:cc:09:05"
        if platform.system() != "Darwin"
        else "611DA503-0F79-405E-81A2-BE1A5CEECC91"  # 2
    )
    loop = asyncio.get_event_loop()  # 3
    loop.run_until_complete(run(address, loop))  # 4
