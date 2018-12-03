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

print("Network")
print("Waiting on traffic from: ", portc, "& ", ports)

def recvPackets():
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

if len(sys.argv) == 3:
    sockobjc.bind((sys.argv[1], portc))
    sockobjs.bind((sys.argv[2], 0))
    print('Client ip: ' + sys.argv[1])
    print('Server ip: ' + sys.argv[2])
else:
    sockobjc.bind(("", portc))
    sockobjs.bind(("", 0))
    print('Using default of localhost. To use custom connections use: udpn.py <ipClient> <ipServer>')

recvPackets()


#print packet.getData()
#print("\nReceived: ", datac, "From: ", addrc)

#sockobjs.sendto(datac, (host, ports))
#print("\nSent: ", "Network -> Server", "To: ", host, ports)

##datas, addrs = sockobjs.recvfrom(bufsize)
#print("\nReceived: ", datas, "From: ", addrs)

##sockobjc.sendto(b"Ack From Network", addrc)
#print("\nSent: ", "Network -> Client", "To: ", addrc)
