#!/usr/bin/python

from socket import *
from packet import Packet
import pickle

host = "localhost"
portc = 8000
ports = 8001
bufsize = 1024
packetList = []

sockobjc = socket(AF_INET, SOCK_DGRAM)
sockobjs = socket(AF_INET, SOCK_DGRAM)
sockobjc.bind(("", portc))
sockobjs.bind(("", 0))

print("Network")
print("Waiting on traffic from: ", portc, "& ", ports)

datac, addrc = sockobjc.recvfrom(bufsize)

while (datac):
    packet = pickle.loads(datac)
    if packet.getPacketType() == "EOT":
        for pckt in packetList:
            sockobjs.sendto(pickle.dumps(pckt), (host, ports))
        break
    else:
        packetList.append(packet)
        datac, addrc = sockobjc.recvfrom(bufsize)

#print packet.getData()
#print("\nReceived: ", datac, "From: ", addrc)

#sockobjs.sendto(datac, (host, ports))
#print("\nSent: ", "Network -> Server", "To: ", host, ports)

##datas, addrs = sockobjs.recvfrom(bufsize)
#print("\nReceived: ", datas, "From: ", addrs)

##sockobjc.sendto(b"Ack From Network", addrc)
#print("\nSent: ", "Network -> Client", "To: ", addrc)
