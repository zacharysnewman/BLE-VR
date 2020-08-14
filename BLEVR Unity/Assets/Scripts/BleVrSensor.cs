using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[System.Serializable]
public class BleVrSensor
{
    public string uuid = "";
    public Vector3 angle = Vector3.zero;
    public float deltaTime = 0;

    public BleVrSensor() { }
    public BleVrSensor(string uuid, Vector3 angle, float deltaTime)
    {
        this.uuid = uuid;
        this.angle = angle;
        this.deltaTime = deltaTime;
    }
}
