#!/usr/bin/python

from socket import *
from packet import Packet
import pickle

host = "localhost"
port = 8001
bufsize = 1024
packetList = []

sockobj = socket(AF_INET, SOCK_DGRAM)
sockobj.bind(("", port))

#print("Server")

print("waiting on port:", port)
f = open("test1.jpeg", 'wb')

data, addr = sockobj.recvfrom(bufsize)

while (data):
    packet = pickle.loads(data)
    packetList.append(packet)
    f.write(packet.getData())
    if (packet.getPacketType() == "EOT"):
        for pckt in packetList:
                ack = Packet("ACK", 1, data, pckt.getSeqNum())
                ackStr = pickle.dumps(ack)
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
