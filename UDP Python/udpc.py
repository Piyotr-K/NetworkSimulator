#!/usr/bin/python

from socket import *
import os
import pickle
from packet import Packet
from sys import getsizeof
import sys

host = "localhost"
port = 8000
bufsize = 512
seqnum = 1
windowSize = 5490
amountSent = 0
prevPacketSize = 0
packetList = []
ackList = []
ackFound = 0
sockobj = socket(AF_INET, SOCK_DGRAM)
sockobj.bind(("", 0))
global f

#print("Client")

def openFile(filename):
    global f
    try:
        f = open(filename, 'rb')
    except FileNotFoundError as e:
        print 'File not found'

if len(sys.argv) == 3:
    openFile(sys.argv[2])

data = f.read(bufsize)
seqnum += getsizeof(data)
packet = Packet("Data", seqnum, data, 1)
packetStr = packet.toString()
packetList.append(packet)

while (data):
    if (amountSent + getsizeof(packetStr) <= windowSize):
        if(sockobj.sendto(packetStr, (host, port))):
            amountSent += getsizeof(packetStr)
            print amountSent
            data = f.read(bufsize)
            seqnum += getsizeof(data)
            if (getsizeof(data) < prevPacketSize):
                packet = Packet("EOT", seqnum, data, 1)
            elif (amountSent + getsizeof(packetStr) >= windowSize - getsizeof(packetStr) and amountSent + getsizeof(packetStr) <= windowSize):
                packet = Packet("EOT", seqnum, data, 1)
            else:
                packet = Packet("Data", seqnum, data, 1)
            packetList.append(packet)
            packetStr = packet.toString()
            prevPacketSize = getsizeof(packet.getData())
    else:
        amountSent = 0
        data, addr = sockobj.recvfrom(1024)
        while (data):
            ack = Packet.decode(Packet(), data)
            ackList.append(ack)
            data, addr = sockobj.recvfrom(1024)
            if (data == "EOT"):
                break
f.close()
