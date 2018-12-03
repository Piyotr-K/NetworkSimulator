#!/usr/bin/python

from socket import *
import pickle
from packet import Packet
from sys import getsizeof

host = "localhost"
port = 8000
bufsize = 512
seqnum = 0
sockobj = socket(AF_INET, SOCK_DGRAM)
sockobj.bind(("", 0))

print("Client")

f=open("hello.txt","rb")
data = f.read(bufsize)
seqnum += getsizeof(data)
packet = Packet("data", 1, data, 65507, 1)
packetStr = pickle.dumps(packet, 0)

while (data):
    if(sockobj.sendto(packetStr, (host, port))):
        data = f.read(bufsize)
        seqnum += getsizeof(data)
        packet = Packet("data", seqnum, data, 65507, 1)
        packetStr = pickle.dumps(packet, 0)

packet = Packet("EOT", seqnum, "EOT", 65507, 1)
packetStr = pickle.dumps(packet)
sockobj.sendto(packetStr, (host, port))
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
