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
f = open("hello1.txt", 'wb')

if len(sys.argv) == 2:
    host = sys.argv[1]
else:
    print 'Using Default of localhost'

data, addr = sockobj.recvfrom(bufsize)

while (data):
    packet = Packet.decode(Packet(), data)
    print 'Received Packet Type: ' + str(packet.getPacketType()) + ", Sequence Number: " + str(packet.getSeqNum())
    packetList.append(packet)
    f.write(packet.getData())
    if (packet.getPacketType() == "EOT"):
        for pckt in packetList:
            ack = Packet("ACK", 1, "", pckt.getSeqNum())
            ackStr = ack.toString()
            sockobj.sendto(ackStr, addr)
            print 'Sent Packet Type: ' + str(ack.getPacketType()) + ", Acknowledgement Number: " + str(ack.getAckNum())
        packetList = []
        sockobj.sendto("EOT", addr)
    data, addr = sockobj.recvfrom(bufsize)

f.close()
