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
    packet = pickle.loads(datac)
    packetList.append(packet)
    if (packet.getPacketType() == "EOT"):
        for pckt in packetList:
            sockobjs.sendto(pickle.dumps(pckt), (host, ports))
            print pckt.getSeqNum()
        packetList = []
        datas, addrs = sockobjs.recvfrom(bufsize)
        while (datas):
            ack = pickle.loads(datas)
            ackList.append(ack)
            datas, addrs = sockobjs.recvfrom(bufsize)
            if (datas == "breakpl0x"):
                break
        for acks in ackList:
            sockobjc.sendto(pickle.dumps(acks), (host, portc))
    datac, addrc = sockobjc.recvfrom(bufsize)

#print packet.getData()
#print("\nReceived: ", datac, "From: ", addrc)

#sockobjs.sendto(datac, (host, ports))
#print("\nSent: ", "Network -> Server", "To: ", host, ports)

##datas, addrs = sockobjs.recvfrom(bufsize)
#print("\nReceived: ", datas, "From: ", addrs)

##sockobjc.sendto(b"Ack From Network", addrc)
#print("\nSent: ", "Network -> Client", "To: ", addrc)
