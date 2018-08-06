#! /usr/bin/env python3
        
import socket

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('', 50000))
serverSocket.listen(5)

while True:
        conn, addr = serverSocket.accept()
        
        conn.sendall('OK'.encode('utf-8'))
        conn.close()

