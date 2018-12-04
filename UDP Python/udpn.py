#!/usr/bin/python

from socket import *
from packet import Packet
import pickle
from sys import getsizeof
import sys
import random

host = "localhost"
portc = 8000
ports = 8001
bufsize = 1024
packetList = []
ackList = []
sockobjc = socket(AF_INET, SOCK_DGRAM)
sockobjs = socket(AF_INET, SOCK_DGRAM)
sockobjc.bind(("", portc))
sockobjs.bind(("", 0))

print("Network")
print("Waiting on traffic from: ", portc, "& ", ports)

if len(sys.argv) == 3:
    host = sys.argv[1]
    print 'Random drop chance: ' + sys.argv[2] + '%'
elif len(sys.argv) == 2:
    print 'Random drop chance: ' + sys.argv[1] + '%'
    dropRate = 100/int(sys.argv[1])
    print 'Using Default of localhost'

datac, addrc = sockobjc.recvfrom(bufsize)

while (datac):
    packet = Packet.decode(Packet(), datac)
    packetList.append(packet)
    if (packet.getPacketType() == "EOT"):
        for pckt in packetList:
            if (random.randint(0, dropRate) == 1):
                print "Packet dropped!"
            else:
                sockobjs.sendto(pckt.toString(), (host, ports))
        packetList = []
        datas, addrs = sockobjs.recvfrom(bufsize)
        while (datas):
            ack = Packet.decode(Packet(), datas)
            ackList.append(ack)
            datas, addrs = sockobjs.recvfrom(bufsize)
            if (datas == "EOT"):
                break
        for acks in ackList:
            sockobjc.sendto(acks.toString(), addrc)
        ackList = []
        sockobjc.sendto("EOT", addrc)
    datac, addrc = sockobjc.recvfrom(bufsize)
