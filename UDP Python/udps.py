#!/usr/bin/python

from socket import *

port = 8001
host = "localhost"
sockobj = socket(AF_INET, SOCK_DGRAM)
sockobj.bind(("", port))

print "waiting on port:", port
while 1:
    data, addr = sockobj.recvfrom(1024)
    print "\nReceived: ", data, "From: ", addr
    f = open("hello1.txt", 'wb')
    f.write(data.decode('utf-8'))

sockobj.sendto("Ack From Server", addr)
print "\nSent: ", "Server -> Network", "To: ", addr
