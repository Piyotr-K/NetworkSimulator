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
    print packet.getSeqNum()
    if (packet.getPacketType() == "EOT"):
        for pckt in packetList:
            sockobjs.sendto(pickle.dumps(pckt), (host, ports))
        packetList = []
        datas, addrs = sockobjs.recvfrom(bufsize)
        while (datas):
            print "hi"
            ack = pickle.loads(datas)
            ackList.append(ack)
            datas, addrs = sockobjs.recvfrom(bufsize)
            if (datas == "EOT"):
                break
        for acks in ackList:
            sockobjc.sendto(pickle.dumps(acks), addrc)
        ackList = []
        sockobjc.sendto("EOT", addrc)
    datac, addrc = sockobjc.recvfrom(bufsize)

f.close()


#print packet.getData()
#print("\nReceived: ", datac, "From: ", addrc)

#sockobjs.sendto(datac, (host, ports))
#print("\nSent: ", "Network -> Server", "To: ", host, ports)

##datas, addrs = sockobjs.recvfrom(bufsize)
#print("\nReceived: ", datas, "From: ", addrs)

##sockobjc.sendto(b"Ack From Network", addrc)
#print("\nSent: ", "Network -> Client", "To: ", addrc)
