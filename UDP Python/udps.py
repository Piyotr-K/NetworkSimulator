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
f = open("hello1.txt", 'w')

data, addr = sockobj.recvfrom(bufsize)

while (data):
    packet = pickle.loads(data)
    if (packet.getPacketType() == "EOT"):
        for pckt in packetList:
                ack = Packet("ACK", 1, data, pckt.getSeqNum())
                ackStr = pickle.dumps(ack)
                sockobj.sendto(ackStr, addr)
    packet = pickle.loads(data)
    print packet.getSeqNum()
    packetList.append(packet)
    f.write(packet.getData().decode('utf-8'))
    data, addr = sockobj.recvfrom(bufsize)



#print("\nReceived: ", data, "From: ", addr)

#print("finished writing to file.")
#f.close()
#sockobj.sendto(b'Ack From Server', addr)
#print("\nSent: ", "Server -> Network", "To: ", addr)
