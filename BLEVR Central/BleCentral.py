import platform
import asyncio
import struct
import json
import time
import BleCentralLibrary as myBle
from bleak import BleakScanner, BleakClient, BleakError


class BleCentral():

    bleakClients = []
    loop = None
    initialized = False

    def initialize(self):
        self.loop = asyncio.get_event_loop()
        self.initialized = True

    def shutdown(self):
        if not self.initialized:
            return

        self.loop.close()
        self.initialized = False

    def connectToNearbySensors(self):
        if not self.initialized:
            return None

        return self.loop.run_until_complete(self.asyncConnectToNearbySensors())

    def refreshSensorData(self):
        if not self.initialized:
            return None

        return self.loop.run_until_complete(self.asyncRefreshSensorData())

    async def asyncConnectToNearbySensors(self):
        uuids = await myBle.findNearbyBleSensorUuids()
        print(uuids)

        self.bleakClients = []
        connections = []

        for uuid in uuids:
            client = BleakClient(uuid, loop=self.loop)
            connected = await client.connect()
            if connected:
                self.bleakClients.append(client)
                connections.append(uuid)

        return connections

    async def asyncRefreshSensorData(self):
        allJsonSensorData = []

        for client in self.bleakClients:
            rawSensorData = []
            rawSensorData = await myBle.getRawSensorData(client, self.loop)

            if rawSensorData is None:
                print("Failed to get this sensor data: " + client.address)
                continue

            try:
                processedSensorData = myBle.processRawSensorData(
                    client.address, rawSensorData)
            except IndexError as e:
                print("skipping: " + client.address)
                continue

            jsonSensorData = myBle.serializeToJson(processedSensorData)

            allJsonSensorData.append(jsonSensorData)

        return allJsonSensorData


# central = BleCentral()
# central.initialize()
# print("initialized: " + str(central.initialized))

# sensors = central.connectToNearbySensors()
# print("sensors: " + str(sensors))

# sensorData = central.refreshSensorData()
# print("sensorData: " + str(sensorData))

# central.shutdown()
