#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 11111        # Port to listen on (non-privileged ports are > 1023)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print(f'Listening on port ({PORT}) and IP ({HOST})')
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            jsonString = '{ "uuid": "abcd-1234", "angle": { "x": 1.0, "y": 2.0, "z": 3.0 }, "deltaTime": "0.0" }'
            data = bytes(jsonString, 'utf-8')
            print(len(data))
            while True:
                recvd = conn.recv(1024)
                if not recvd:
                    break
                conn.sendall(data)

                # print('Sending data back: ' + str(data))
                # conn.sendall(bytes('Test Server echo ', 'utf-8') + data)

                # -- ERROR thrown when client disconnects from server --
                #  File "/Users/zacknewman/Projects/BLEVR Project/BLEVR Central/Sockets/SocketServer.py", line 19, in <module>
                # recvd = conn.recv(1024)
                # ConnectionResetError: [Errno 54] Connection reset by peer
