#!/usr/bin/python

from socket import *
from packet import Packet
import pickle

host = "localhost"
port = 8001
bufsize = 1024
packetList = []
global f

sockobj = socket(AF_INET, SOCK_DGRAM)
sockobj.bind(("", port))

#print("Server")

print("waiting on port:", port)

f = open('hello1.txt', 'wb')
data, addr = sockobj.recvfrom(bufsize)

while (data):
    packet = Packet.decode(Packet(), data)
    packetList.append(packet)
    f.write(packet.getData())
    if (packet.getPacketType() == "EOT"):
        for pckt in packetList:
                ack = Packet("ACK", 1, data, pckt.getSeqNum())
                ackStr = ack.toString()
                sockobj.sendto(ackStr, addr)
        packetList = []
        sockobj.sendto("EOT", addr)
    data, addr = sockobj.recvfrom(bufsize)

f.close()

#print("\nReceived: ", data, "From: ", addr)

#print("finished writing to file.")
#f.close()
#sockobj.sendto(b'Ack From Server', addr)
#print("\nSent: ", "Server -> Network", "To: ", addr)
