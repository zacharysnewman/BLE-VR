using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using UnityEngine;

public static class SocketClient
{
    public static string GetJsonDataFromLocalServer()
    {
        try
        {
            var ipHost = Dns.GetHostEntry(Dns.GetHostName());
            var ipAddr = IPAddress.Parse("127.0.0.1");//ipHost.AddressList[0];
            var localEndPoint = new IPEndPoint(ipAddr, 11111);
            // Debug.Log(string.Format($"IP: {ipAddr}"));

            var sender = new Socket(ipAddr.AddressFamily, SocketType.Stream, ProtocolType.Tcp);

            sender.Connect(localEndPoint);
            // Debug.Log(string.Format("Socket connected to -> {0} ", sender.RemoteEndPoint.ToString()));

            byte[] messageToSend = Encoding.ASCII.GetBytes("Test Client<EOF>");
            int byteSent = sender.Send(messageToSend);

            byte[] messageReceived = new byte[1024];
            int byteRecv = sender.Receive(messageReceived);

            var messageJson = Encoding.ASCII.GetString(messageReceived,
                                                0, byteRecv);

            // Debug.Log(string.Format("Message from Server -> {0}", messageJson));

            sender.Shutdown(SocketShutdown.Both);
            sender.Close();

            return messageJson;
        }

        // Manage Socket's Exceptions 
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

        return null;
    }
}
