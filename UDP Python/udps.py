#!/usr/bin/python

from socket import *
from packet import Packet

port = 8001
host = "localhost"
sockobj = socket(AF_INET, SOCK_DGRAM)
sockobj.bind(("", port))

print("Server")

print("waiting on port:", port)

data, addr = sockobj.recvfrom(1024)
print("\nReceived: ", data, "From: ", addr)
f = open("hello1.txt", 'w')
f.write(data.decode('utf-8'))
print("finished writing to file.")

sockobj.sendto(b'Ack From Server', addr)
print("\nSent: ", "Server -> Network", "To: ", addr)
