using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Test : MonoBehaviour
{
    public BleVrSensor sensor;

    // Start is called before the first frame update
    void Start()
    {
    }

    // Update is called once per frame
    void Update()
    {
        var data = SocketClient.GetJsonDataFromLocalServer();
        Debug.Log(data);
    }
}
