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

from bleak import BleakClient


def notification_handler(sender, data):
    """Simple notification handler which prints the data received."""
    print("{0}: {1}".format(sender, data))


async def run(address, loop, debug=False):
    log = logging.getLogger(__name__)
    if debug:
        import sys

        loop.set_debug(True)
        log.setLevel(logging.DEBUG)
        h = logging.StreamHandler(sys.stdout)
        h.setLevel(logging.DEBUG)
        log.addHandler(h)

    async with BleakClient(address, loop=loop) as client:
        charValues = []

        for service in client.services:
            if service.uuid == "3A7E9484-D7D3-4DEA-B422-7C62274CBED3":
                for char in service.characteristics:
                    if "read" in char.properties:
                        try:
                            value = bytes(await client.read_gatt_char(char.uuid))
                        except:
                            value = None
                    else:
                        value = None
                    charValues.append(value)

        print(charValues)

        if charValues == []:
            return None
        else:
            return charValues


if __name__ == "__main__":
    address = (
        "24:71:89:cc:09:05"
        if platform.system() != "Darwin"
        else "611DA503-0F79-405E-81A2-BE1A5CEECC91"
    )
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(address, loop, True))
