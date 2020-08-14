
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
            uuids.append(deviceUuid)

    return uuids


###################################################################
### Get sensor data from each sensor's services/characteristics ###
###################################################################
async def getRawSensorData(client, loop):
    charValues = []

    for service in client.services:
        if service.uuid.lower() == sensorServiceUuid:
            for char in service.characteristics:
                if "read" in char.properties:
                    try:
                        value = bytes(await client.read_gatt_char(char.uuid))
                    except:
                        value = None
                else:
                    value = None
                charValues.append(value)
    return charValues


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
