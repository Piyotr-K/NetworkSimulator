#!/usr/bin/python

from socket import *
import os
import pickle
from packet import Packet
from sys import getsizeof

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

#print("Client")

f=open("test.jpeg","rb")
data = f.read(bufsize)
seqnum += getsizeof(data)
packet = Packet("Data", seqnum, data, 1)
packetStr = pickle.dumps(packet)
packetList.append(packet)

while (data):
    if (amountSent + getsizeof(packetStr) <= windowSize):
        if(sockobj.sendto(packetStr, (host, port))):
            amountSent += getsizeof(packetStr)
            print amountSent
            data = f.read(bufsize)
            seqnum += getsizeof(data)
            if (getsizeof(data) <= prevPacketSize):
                packet = Packet("EOT", seqnum, data, 1)
            elif (amountSent + getsizeof(packetStr) >= windowSize - getsizeof(packetStr) and amountSent + getsizeof(packetStr) <= windowSize):
                packet = Packet("EOT", seqnum, data, 1)
            else:
                packet = Packet("Data", seqnum, data, 1)
            packetList.append(packet)
            packetStr = pickle.dumps(packet)
            prevPacketSize = getsizeof(packet.getData())
    else:
        amountSent = 0
        data, addr = sockobj.recvfrom(1024)
        while (data):
            ack = pickle.loads(data)
            ackList.append(ack)
            data, addr = sockobj.recvfrom(1024)
            if (data == "EOT"):
                break

        '''for pckt in packetList:
            ackFound = 0
            for ack in ackList:
                if (pckt.getSeqNum() == ack.getAckNum()):
                    ackFound = 1
            if (ackFound == 0):
                packetStr = pickle.dumps(pckt)
                sockobj.sendto(packetStr, (host, port))
        if (ackFound == 0):
            packet = Packet("EOT", 0, "", 1)
            packetStr = pickle.dumps(packet)
            sockobj.sendto(packetStr, (host, port))
        print "packet"
        for pckt in packetList:
            print pckt.getSeqNum()
        print "ack"
        for ack in ackList:
            print ack.getAckNum()
        print "\n\n"'''

f.close()

#sockobj.sendto(data, (host, port))
#while (data):
#    if(sockobj.sendto(data, (host, port))):
        #print("sending ...")
#        data = f.read(buffer)

#sockobj.sendto(data, (host, port))
#print("\nSent: ", "Client -> Network", "From: ", host)

#data, addr = sockobj.recvfrom(buffer)
#print("\nReceived: ", data, "From: ", addr)
