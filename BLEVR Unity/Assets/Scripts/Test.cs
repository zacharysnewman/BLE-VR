using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Test : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        // SocketClient.GetData();
    }

    // Update is called once per frame
    void Update()
    {
        // if (Input.GetKeyDown(KeyCode.Space))
        SocketClient.GetData();
    }

    void OnApplicationQuit()
    {
        // SocketClient.Stop();
    }
}
