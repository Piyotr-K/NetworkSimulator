#!/usr/bin/python

from socket import *

port = 8000
host = "localhost"
sockobj = socket(AF_INET, SOCK_DGRAM)
sockobj.bind(("", 0))

print("Client")

f=open("hello.txt","rb")
data = f.read(1024)

while (data):
    if(sockobj.sendto(data, (host, port))):
        print("sending ...")
        data = f.read(1024)

sockobj.sendto(data, (host, port))
print("\nSent: ", "Client -> Network", "From: ", host)

data, addr = sockobj.recvfrom(1024)
print("\nReceived: ", data, "From: ", addr)
