using System.Threading;
// using System.Diagnostics;
using System.Threading.Tasks;
using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using UnityEngine;

public static class SocketClient
{
    // private static Socket sender;

    public static void GetData()
    {
        ExecuteClient();
    }

    // public static void Stop()
    // {
    //     client.Dispose();
    // }

    // ExecuteClient() Method 
    // private static void Loop()
    // {
    //     while (true)
    //     {
    //         byte[] messageSent = Encoding.ASCII.GetBytes("Test Client<EOF>");
    //         int byteSent = sender.Send(messageSent);

    //         byte[] messageReceived = new byte[1024];

    //         int byteRecv = sender.Receive(messageReceived);
    //         Debug.Log(string.Format("Message from Server -> {0}",
    //           Encoding.ASCII.GetString(messageReceived,
    //                                      0, byteRecv)));
    //     }
    // }

    private static void ExecuteClient()
    {
        //await System.Threading.Tasks.Task.Run(() => WriteLine("Test"));
        try
        {
            var ipHost = Dns.GetHostEntry(Dns.GetHostName());
            var ipAddr = IPAddress.Parse("127.0.0.1");//ipHost.AddressList[0];
            var localEndPoint = new System.Net.IPEndPoint(ipAddr, 11111);
            Debug.Log(string.Format($"IP: {ipAddr}"));

            var sender = new Socket(ipAddr.AddressFamily, SocketType.Stream, ProtocolType.Tcp);

            try
            {
                sender.Connect(localEndPoint);
                Debug.Log(string.Format("Socket connected to -> {0} ", sender.RemoteEndPoint.ToString()));

                // while (true)
                // {
                byte[] messageSent = System.Text.Encoding.ASCII.GetBytes("Test Client<EOF>");
                int byteSent = sender.Send(messageSent);

                byte[] messageReceived = new byte[1024];

                int byteRecv = sender.Receive(messageReceived);
                Debug.Log(string.Format("Message from Server -> {0}",
                        System.Text.Encoding.ASCII.GetString(messageReceived,
                                                    0, byteRecv)));
                // }

                sender.Shutdown(SocketShutdown.Both);
                sender.Close();
            }

            // Manage Socket's Exceptions 
            catch (System.ArgumentNullException ane)
            {
                Debug.Log(string.Format("ArgumentNullException : {0}", ane.ToString()));
            }

            catch (System.Net.Sockets.SocketException se)
            {
                Debug.Log(string.Format("SocketException : {0}", se.ToString()));
            }

            catch (System.Exception e)
            {
                Debug.Log(string.Format("Unexpected exception : {0}", e.ToString()));
            }

            finally
            {
                // Close Socket using  
                // the method Close() 
                sender.Shutdown(System.Net.Sockets.SocketShutdown.Both);
                sender.Close();
            }
        }

        catch (System.Exception e)
        {
            Debug.Log(string.Format(e.ToString()));
        }
    }
}
