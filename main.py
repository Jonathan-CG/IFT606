#! /usr/bin/env python3

import subprocess
import re
import socket
import fcntl
import struct

class Neighbour:
    def __init__(self, ipAddress, status):
        self.ipAddress = ipAddress
        self.status = status

if __name__ == "__main__":
    print([(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1])
    #HARDCODED - through ifconfig, need to figure out local adress/mask
    nmapOutput = subprocess.check_output(["nmap", "-p", "22", "10.44.88.*"])
    nmapString = nmapOutput.decode("utf-8")
    listedNmapString = nmapString.splitlines()
    del listedNmapString[-1]
    del listedNmapString[0]
    del listedNmapString[0]
    neighbours  = []
    i = 0
    for entry in listedNmapString:
        if entry :
            if i % 4 == 0 :
                ipAddress = re.findall(r'(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})',entry)[0]
            if i % 4 == 3 :
                status = entry.split()[1]
                neighbours.append(Neighbour(ipAddress, status))
            i = i + 1
    for nb in neighbours :
        if nb.status == "open" :
            print(nb.ipAddress)
            print(nb.status)

