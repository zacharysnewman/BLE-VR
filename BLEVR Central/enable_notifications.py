# -*- coding: utf-8 -*-
"""
Notifications
-------------
Example showing how to add notifications to a characteristic and handle the responses.
Updated on 2019-07-03 by hbldh <henrik.blidh@gmail.com>
"""

import logging
import asyncio
import platform

from bleak import BleakClient
from bleak import _logger as logger


# <--- Change to the characteristic you want to enable notifications from.
CHARACTERISTIC_UUID = "42EA697D-7DF9-4356-A35F-5765A37F788E".lower()


def notification_handler(sender, data):
    """Simple notification handler which prints the data received."""
    print("{0}: {1}".format(sender, data))


async def run(address, loop, debug=False):
    if debug:
        import sys

        # loop.set_debug(True)
        l = logging.getLogger("asyncio")
        l.setLevel(logging.DEBUG)
        h = logging.StreamHandler(sys.stdout)
        h.setLevel(logging.DEBUG)
        l.addHandler(h)
        logger.addHandler(h)

    async with BleakClient(address, loop=loop) as client:
        x = await client.is_connected()
        logger.info("Connected: {0}".format(x))

        await client.start_notify(CHARACTERISTIC_UUID.lower(), notification_handler)
        await asyncio.sleep(5.0, loop=loop)
        await client.stop_notify(CHARACTERISTIC_UUID.lower())


if __name__ == "__main__":
    import os

    os.environ["PYTHONASYNCIODEBUG"] = str(1)
    address = (
        # <--- Change to your device's address here if you are using Windows or Linux
        "24:71:89:cc:09:05"
        if platform.system() != "Darwin"
        # <--- Change to your device's address here if you are using macOS
        else "611DA503-0F79-405E-81A2-BE1A5CEECC91"
    )
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(address, loop, True))
