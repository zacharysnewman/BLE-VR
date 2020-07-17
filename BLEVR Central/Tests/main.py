###################################################################
# Imports (Libraries)                                           ###
###################################################################
import platform
import asyncio
import struct
import json
import time
from bleak import BleakScanner, BleakClient, BleakError


###################################################################
# Define constant values (UUID's, etc.)                         ###
###################################################################
sensorServiceUuid = "3A7E9484-D7D3-4DEA-B422-7C62274CBED3".lower()
sensorPitchCharacteristicUuid = "42EA697D-7DF9-4356-A35F-5765A37F788E".lower()
sensorRollCharacteristicUuid = "D11D3A7F-0B36-4B7D-B646-948A016583F8".lower()
sensorYawCharacteristicUuid = "B0158511-E858-4877-823C-AA032A8D67F1".lower()
sensorDeltaTimeCharacteristicUuid = "172F4F16-9D0C-47EC-89BC-D8CC41A1D993".lower()

bleakClients = []


###################################################################
# Main (Program Entry)                                          ###
###################################################################
async def main(loop):
    bleakClients = []
    uuids = await findNearbyBleSensorUuids()

    allJsonSensorData = []

    for uuid in uuids:
        client = BleakClient(uuid, loop=loop)
        connected = await client.connect(timeout=0.01)
        bleakClients.append(client)

    for client in bleakClients:
        rawSensorData = []

    # Third
        startTime = time.time()
        try:
            rawSensorData.append(bytes(await client.read_gatt_char(sensorPitchCharacteristicUuid)))
            rawSensorData.append(bytes(await client.read_gatt_char(sensorRollCharacteristicUuid)))
            rawSensorData.append(bytes(await client.read_gatt_char(sensorYawCharacteristicUuid)))
            rawSensorData.append(bytes(await client.read_gatt_char(sensorDeltaTimeCharacteristicUuid)))
        except:
            print(f'Elapsed Fail: [{time.time()-startTime}]')
            print("Failed to get characteristics!")
            return None
        print(f'Elapsed Success: [{time.time()-startTime}]')

    # Second
        # client.set_disconnected_callback(onDisconnected)
        # connected = await client.connect(timeout=0.01)
        # test = await client.is_connected()
        # print(test)

        # try:
        # await client.start_notify(sensorPitchCharacteristicUuid, onNotifyNewData)
        #     print(f"{uuid} 1) When is this called?")
        # except:
        #     onDisconnected(client)
        #     await client.disconnect()
        #     onDisconnected(client)
        #     print("Failure?")

        # print(f"{uuid} 2) When is this called?")

    # First
        # rawSensorData = await getRawSensorData(uuid, loop)

        # if rawSensorData is None:
        #     print("Failed to get this sensor data: " + uuid)
        #     continue

        # processedSensorData = processRawSensorData(uuid, rawSensorData)
        # jsonSensorData = serializeToJson(processedSensorData)
        # allJsonSensorData.append(jsonSensorData)

    # print(allJsonSensorData)
    print("end")


def onNotifyNewData(uuid, notifyBytes):
    print('uuid: {0}'.format(uuid))


def onDisconnected(client):
    print(f'Is Connected: {client.is_connected}')

###################################################################
# Get List of BLE VR Sensors                                    ###
###################################################################


async def findNearbyBleSensorUuids():
    allBleDevices = await BleakScanner.discover()
    uuids = []

    for d in allBleDevices:
        deviceInfo = str(d).split(": ")
        deviceUuid = deviceInfo[0]
        deviceName = deviceInfo[1]

        if deviceName == "BLE VR Sensor":
            # print(d)
            uuids.append(deviceUuid)

    return uuids

# Usage:
# loop = asyncio.get_event_loop()
# loop.run_until_complete(run())


###################################################################
### Get sensor data from each sensor's services/characteristics ###
###################################################################
async def getRawSensorData(address, loop):
    # print("start")
    async with BleakClient(address, loop=loop) as client:
        # print("check connection")
        try:
            isClientConnected = await client.is_connected()
        except:
            print("Failed to connect")
            return None

        # print("connected: {0}".format(isClientConnected))
        if not isClientConnected:
            print("Client did not connect")
            return None

        rawSensorData = []

        # print("starting get chars...")
        print(f'Start: [{time.time()}]')
        try:
            rawSensorData.append(bytes(await client.read_gatt_char(sensorPitchCharacteristicUuid)))
            rawSensorData.append(bytes(await client.read_gatt_char(sensorRollCharacteristicUuid)))
            rawSensorData.append(bytes(await client.read_gatt_char(sensorYawCharacteristicUuid)))
            rawSensorData.append(bytes(await client.read_gatt_char(sensorDeltaTimeCharacteristicUuid)))
        except:
            print(f'End Fail: [{time.time()}]')
            print("Failed to get characteristics!")
            return None
        print(f'End Success: [{time.time()}]')

        return rawSensorData

# Usage:
# if __name__ == "__main__":
#     address = "611DA503-0F79-405E-81A2-BE1A5CEECC91"
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(getSensorData(address, loop))


###################################################################
### Convert data from bytes to floats                           ###
###################################################################
def processRawSensorData(uuid, rawSensorData):
    processedSensorData = {
        "uuid": uuid,
        "angle": {
            "x": struct.unpack('f', rawSensorData[0])[0],
            "y": struct.unpack('f', rawSensorData[1])[0],
            "z": struct.unpack('f', rawSensorData[2])[0]
        },
        "deltaTime": struct.unpack('f', rawSensorData[3])[0]
    }
    return processedSensorData


###################################################################
### Return or send JSON formatted sensor data out to C# code    ###
###################################################################
def serializeToJson(objectToSerialize):
    jsonString = json.dumps(objectToSerialize)
    return jsonString


# RUN
if __name__ == "__main__":  # <--- What does this do?
    loop = asyncio.get_event_loop()
    while True:
        print("Starting loop. " + str(bleakClients))
        try:
            loop.run_until_complete(main(loop))
        except BleakError as e:
            print('ERROR: ' + str(e).replace('Device with address ',
                                             '').replace(' was not found', '') + ' device was not found.')
