#!/usr/bin/python

from socket import *
from packet import Packet
import pickle

host = "localhost"
port = 8001
bufsize = 1024

sockobj = socket(AF_INET, SOCK_DGRAM)
sockobj.bind(("", port))

print("Server")

print("waiting on port:", port)
f = open("hello1.txt", 'w')

data, addr = sockobj.recvfrom(bufsize)

while (data):
    packet = pickle.loads(data)
    f.write(packet.getData().decode('utf-8'))
    data, addr = sockobj.recvfrom(bufsize)

f.close()
sockobj.sendto(b'Ack From Server', addr)

#print("\nReceived: ", data, "From: ", addr)

#print("finished writing to file.")
#print("\nSent: ", "Server -> Network", "To: ", addr)
