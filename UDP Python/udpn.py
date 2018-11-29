#!/usr/bin/python

from socket import *

portc = 8000
host = "localhost"
ports = 8001

sockobjc = socket(AF_INET, SOCK_DGRAM)
sockobjs = socket(AF_INET, SOCK_DGRAM)
sockobjc.bind(("", portc))
sockobjs.bind(("", 0))

print "Waiting on traffic from: ", portc, "& ", ports

datac, addrc = sockobjc.recvfrom(1024)
print "\nReceived: ", datac, "From: ", addrc

sockobjs.sendto(datac, (host, ports))
print "\nSent: ", "Network -> Server", "To: ", host, ports

datas, addrs = sockobjs.recvfrom(1024)
print "\nReceived: ", datas, "From: ", addrs

sockobjc.sendto("Ack From Network", addrc)
print "\nSent: ", "Network -> Client", "To: ", addrc
