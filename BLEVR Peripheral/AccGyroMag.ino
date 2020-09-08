/*
  Sensor Fusion

  Adapts code from the Simple Accelerometer, Simple Gyroscope, 
  Simple Magnetometer, SensorFusion, MPU9250_SPI_SF, LED, and Battery 
  Monitor examples to advertise Sensor Fusion data over BLE.

  The circuit:
  - Arduino Nano 33 BLE (983KB Program Storage Space, 262KB Dynamic Memory) 

  The output:
  - Data is advertised as 4 little endian floating point numbers (probably represented in HEX or BYTES)

  created 8 Jul 2020
  by Zachary Newman
*/
#include <Streaming.h>
#include <Arduino_LSM9DS1.h>
#include "SensorFusion.h" //SF
#include <ArduinoBLE.h>

 // BLE Services
BLEService fuseService("3A7E9484-D7D3-4DEA-B422-7C62274CBED3");
BLEFloatCharacteristic pitchChar("42EA697D-7DF9-4356-A35F-5765A37F788E", BLERead | BLENotify);
BLEFloatCharacteristic rollChar("D11D3A7F-0B36-4B7D-B646-948A016583F8", BLERead | BLENotify);
BLEFloatCharacteristic yawChar("B0158511-E858-4877-823C-AA032A8D67F1", BLERead | BLENotify);
BLEFloatCharacteristic deltaChar("172F4F16-9D0C-47EC-89BC-D8CC41A1D993", BLERead | BLENotify);
BLEDescriptor pitchDesc("2901", "Pitch");
BLEDescriptor rollDesc("2901", "Roll");
BLEDescriptor yawDesc("2901", "Yaw");
BLEDescriptor deltaDesc("2901", "Delta Time");

SF fusion;

String newl = "\n";

float gx, gy, gz, ax, ay, az, mx, my, mz;
float pitch, roll, yaw;
float deltat;

bool logging = false; // DEBUGGING ONLY! Set to "false" when uploading PROD version, otherwise it won't start advertising until the Serial Monitor is connected

void setup() {
  if(logging) {
    Serial.begin(9600);
    while (!Serial);
    Serial.println("Started");
  }

  if (!IMU.begin()) {
    if(logging)
      Serial.println("Failed to initialize IMU!");
    while (1);
  }

  if(logging)
    LogSampleRates();
    
  Advertise();
}

void loop() {
  CentralUpdate();
}

void LogSampleRates() {
  Serial << "Accelerometer sample rate = " << (String)IMU.accelerationSampleRate() << " Hz\n" << "Acceleration in G's\nX\tY\tZ";
  Serial << "Gyroscope sample rate = " << (String)IMU.gyroscopeSampleRate() << " Hz\n" << "Gyroscope in degrees/second\nX\tY\tZ";
  Serial << "Magnetic field sample rate = " << (String)IMU.magneticFieldSampleRate() << " uT\n" << "Magnetic Field in uT\nX\tY\tZ";
}

void Advertise() {
  pinMode(LED_BUILTIN, OUTPUT); // initialize the built-in LED pin to indicate when a central is connected

  // begin initialization
  if (!BLE.begin()) {
    if(logging)
      Serial.println("starting BLE failed!");

    while (1);
  }

  BLE.setDeviceName("BLE VR Sensor");
  BLE.setLocalName("BLE VR Sensor");

  BLEFloatCharacteristic fuseChars[] = {pitchChar, rollChar, yawChar, deltaChar};
  BLEDescriptor fuseDescs[] = {pitchDesc, rollDesc, yawDesc, deltaDesc};
  SetupService(fuseService, fuseChars, fuseDescs, 4);

  // start advertising
  BLE.advertise();

  if(logging)
    Serial.println("Bluetooth device active, waiting for connections...");
}

void SetupService(BLEService newService, BLEFloatCharacteristic characteristics[], BLEDescriptor descriptors[], int numValues)
{
  BLE.setAdvertisedService(newService); // add the service UUID
  for(int i = 0; i < numValues; i++) {
      characteristics[i].addDescriptor(descriptors[i]);
      newService.addCharacteristic(characteristics[i]);
  }

  BLE.addService(newService); // Add the service

  for(int i = 0; i < numValues; i++) {
    characteristics[i].writeValue(0); // set initial value for this characteristic
  }
}

void ReadAcc() {
  float x, y, z;

  if (IMU.accelerationAvailable()) {
    IMU.readAcceleration(x, y, z);

      gx = x * DEG_TO_RAD;
      gy = y * DEG_TO_RAD;
      gz = z * DEG_TO_RAD;

//      if(logging)
//        Serial << "Acc\t" << (String)x << "\t" << (String)y << "\t" << (String)z << newl;
  }
}

void ReadGyro() {
  float x, y, z;

  if (IMU.gyroscopeAvailable()) {
    IMU.readGyroscope(x, y, z);

    ax = x;
    ay = y;
    az = z;

//    if(logging)
//      Serial << "Gyro\t" << (String)x << "\t" << (String)y << "\t" << (String)z << newl;
  }
}

void ReadMag() {
  float x, y, z;

  if (IMU.magneticFieldAvailable()) {
    IMU.readMagneticField(x, y, z);
    
    mx = x;
    my = y;
    mz = z;
    
//  if(logging)
//    Serial << "Mag\t" << (String)x << "\t" << (String)y << "\t" << (String)z << newl;
  }
}

void Fuse() {
  if(logging) {
    Serial << "From last Update:\t"; Serial.println(deltat, 6);
    Serial << "GYRO:\tx:" << gx << "\t\ty:" << gy << "\t\tz:" << gz << newl;
    Serial << "ACC:\tx:" << ax << "\t\ty:" << ay << "\t\tz:" << az << newl;
    Serial << "MAG:\tx:" << mx << "\t\ty:" << my << "\t\tz:" << mz << newl;
//    Serial << "TEMP:\t" << temp << newl << newl;
  }

  deltat = fusion.deltatUpdate();
  //fusion.MahonyUpdate(gx, gy, gz, ax, ay, az, mx, my, mz, deltat);  //mahony is suggested if there isn't the mag
  fusion.MadgwickUpdate(gx, gy, gz, ax, ay, az, mx, my, mz, deltat);  //else use the magwick

  roll = fusion.getRoll();
  pitch = fusion.getPitch();
  yaw = fusion.getYaw();

  if(logging)
    Serial << "Pitch:\t" << pitch << "\t\tRoll:\t" << roll << "\t\tYaw:\t" << yaw << newl << newl;

//#ifdef PROCESSING
//  roll = fusion.getRollRadians();
//  pitch = fusion.getPitchRadians();
//  yaw = fusion.getYawRadians();
//  if(logging)
//    Serial  << pitch << ":" << roll << ":" << yaw << newl;
//#endif
}

void CentralUpdate() {
  // wait for a BLE central
  BLEDevice central = BLE.central();

  // if a central is connected to the peripheral:
  if (central) {
    if(logging) {
      Serial.print("Connected to central: ");
      Serial.println(central.address());    // print the central's BT address:
    }

    digitalWrite(LED_BUILTIN, HIGH);    // turn on the LED to indicate the connection:

    // while the central is connected:
    while (central.connected()) {
      ReadAcc();
      ReadGyro();
      ReadMag();
      Fuse();
      pitchChar.writeValue(pitch);
      rollChar.writeValue(roll);
      yawChar.writeValue(yaw);
    }

    // when the central disconnects, turn off the LED:
    digitalWrite(LED_BUILTIN, LOW);

    if(logging) {
      Serial.print("Disconnected from central: ");
      Serial.println(central.address());
    }
  }
}
