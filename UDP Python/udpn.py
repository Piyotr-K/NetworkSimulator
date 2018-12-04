#!/usr/bin/python

from socket import *
from packet import Packet
import pickle
from sys import getsizeof

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

datac, addrc = sockobjc.recvfrom(bufsize)

while (datac):
    packet = Packet.decode(Packet(), datac)
    print 'Received Packet Type: ' + str(packet.getPacketType()) + ", Sequence Number: " + str(packet.getSeqNum())
    packetList.append(packet)
    if (packet.getPacketType() == "EOT"):
        for pckt in packetList:
            sockobjs.sendto(pckt.toString(), (host, ports))
            print 'Sent Packet Type: ' + str(pckt.getPacketType()) + ", Sequence Number: " + str(pckt.getSeqNum())
        packetList = []
        datas, addrs = sockobjs.recvfrom(bufsize)
        while (datas):
            ack = Packet.decode(Packet(), datas)
            print 'Received Packet Type: ' + str(ack.getPacketType()) + ", Acknowledgement Number: " + str(ack.getAckNum())
            ackList.append(ack)
            datas, addrs = sockobjs.recvfrom(bufsize)
            if (datas == "EOT"):
                break
        for acks in ackList:
            sockobjc.sendto(acks.toString(), addrc)
            print 'Sent Packet Type: ' + str(acks.getPacketType()) + ", Acknowledgement Number: " + str(acks.getAckNum())
        ackList = []
        sockobjc.sendto("EOT", addrc)
    datac, addrc = sockobjc.recvfrom(bufsize)
