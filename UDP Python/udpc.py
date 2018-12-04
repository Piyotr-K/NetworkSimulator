#!/usr/bin/python

from socket import *
import os
import pickle
from packet import Packet
from sys import getsizeof
import threading
import sys

host = "localhost"
port = 8000
bufsize = 512
seqnum = 1
windowSize = 5490
amountSent = 0
prevPacketSize = 0
packetList = []
toReT = []
ackList = []
ackFound = 0
sockobj = socket(AF_INET, SOCK_DGRAM)
sockobj.bind(("", 0))

#print("Client")

def openFile(filename):
    global f
    try:
        f = open(filename, 'rb')
    except FileNotFoundError as e:
        print 'File not found'

if len(sys.argv) == 3:
    host = sys.argv[1]
    openFile(sys.argv[2])
elif len(sys.argv) == 2:
    openFile(sys.argv[1])
    print 'Using Default of localhost'

data = f.read(bufsize)
seqnum += getsizeof(data)
packet = Packet("Data", seqnum, data, 1)
packetStr = packet.toString()

while (data):
    if (amountSent + getsizeof(packetStr) <= windowSize):
        packetList.append(packet)
        if(sockobj.sendto(packetStr, (host, port))):
            print 'Sent Packet Type: ' + str(packet.getPacketType()) + ", Sequence Number: " + str(packet.getSeqNum())
            amountSent += getsizeof(packetStr)
            data = f.read(bufsize)
            seqnum += getsizeof(data)
            if (getsizeof(data) < prevPacketSize):
                packet = Packet("EOT", seqnum, data, 1)
            elif (amountSent + getsizeof(packetStr) >= windowSize - getsizeof(packetStr) and amountSent + getsizeof(packetStr) <= windowSize):
                packet = Packet("EOT", seqnum, data, 1)
            else:
                packet = Packet("Data", seqnum, data, 1)
            packetStr = packet.toString()
            prevPacketSize = getsizeof(packet.getData())
    else:
        amountSent = 0
        data, addr = sockobj.recvfrom(1024)
        toResend = []
        while (data):
            ack = Packet.decode(Packet(), data)
            print 'Received Packet Type: ' + str(ack.getPacketType()) + ", Acknowledgement Number: " + str(ack.getAckNum())
            ackList.append(ack)
            data, addr = sockobj.recvfrom(1024)
            if (data == "EOT"):
                break
        for pckt in packetList:
            ackFound = 0
            for ack in ackList:
                if (str(pckt.getSeqNum()) == str(ack.getAckNum())):
                    ackFound = 1
                    break
            if (ackFound == 0):
                toResend.append(pckt)
                
        for x in range(0, len(toResend)):
            if (x == len(toResend)):
                toResend[x].setPacketType("EOT")
                packetStr = toResend[x].toString()
                sockobj.sendto(packetStr, (host, port))
            else:
                packetStr = packetList[x].toString()
                sockobj.sendto(packetStr, (host, port))
        toResend = []

f.close()
