// A C# program for Client 
using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using UnityEngine;
using Newtonsoft.Json;

namespace Socketing
{
    public class Client : MonoBehaviour
    {
        public BleVrSensor sensorData = new BleVrSensor();

        // Main Method 
        void Start()
        {
            ExecuteClient();
        }

        // ExecuteClient() Method 
        private void ExecuteClient()
        {
            try
            {
                // Establish the remote endpoint  
                // for the socket. This example  
                // uses port 11111 on the local  
                // computer. 
                IPHostEntry ipHost = Dns.GetHostEntry(Dns.GetHostName());
                IPAddress ipAddr = System.Net.IPAddress.Parse("127.0.0.1");//ipHost.AddressList[0];
                IPEndPoint localEndPoint = new IPEndPoint(ipAddr, 11111);
                Debug.Log($"IP: {ipAddr}");

                // Creation TCP/IP Socket using  
                // Socket Class Costructor 
                Socket sender = new Socket(ipAddr.AddressFamily,
                           SocketType.Stream, ProtocolType.Tcp);

                try
                {

                    // Connect Socket to the remote  
                    // endpoint using method Connect() 
                    sender.Connect(localEndPoint);

                    // We print EndPoint information  
                    // that we are connected 
                    Debug.Log(string.Format("Socket connected to -> {0} ",
                                  sender.RemoteEndPoint.ToString()));

                    // Creation of messagge that 
                    // we will send to Server 
                    // byte[] messageSent = Encoding.UTF8.GetBytes("Test Client<EOF>");
                    // int byteSent = sender.Send(messageSent);

                    // Data buffer 
                    byte[] messageReceived = new byte[1024];

                    // We receive the message using  
                    // the method Receive(). This  
                    // method returns number of bytes 
                    // received, that we'll use to  
                    // convert them to string 
                    while (!Input.GetKeyDown(KeyCode.Space))
                    {
                        int byteRecv = sender.Receive(messageReceived);
                        string jsonString = Encoding.UTF8.GetString(messageReceived, 0, byteRecv);
                        Debug.Log("Message from Server -> " + jsonString);
                        sensorData = JsonConvert.DeserializeObject<BleVrSensor>(jsonString);
                    }

                    // // Close Socket using  
                    // // the method Close() 
                    sender.Shutdown(SocketShutdown.Both);
                    sender.Close();
                }

                // Manage of Socket's Exceptions 
                catch (ArgumentNullException ane)
                {
                    Debug.Log(string.Format("ArgumentNullException : {0}", ane.ToString()));
                }

                catch (SocketException se)
                {
                    Debug.Log(string.Format("SocketException : {0}", se.ToString()));
                }

                catch (Exception e)
                {
                    Debug.Log(string.Format("Unexpected exception : {0}", e.ToString()));
                }

                finally
                {
                    // Close Socket using  
                    // the method Close() 
                    // sender.Shutdown(SocketShutdown.Both);
                    // sender.Close();
                }
            }

            catch (Exception e)
            {

                Debug.Log(e.ToString());
            }
        }
    }
}