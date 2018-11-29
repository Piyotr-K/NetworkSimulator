#!/usr/bin/python

"""
TCP File Transfer client

NOTE: Specify commandline arguments as follows:

./echo-client.py [host]
or
./echo-client.py [host] [GET/SEND]

Author:

Piyotr Kao

A00996404
"""

import sys
import os
import time
import socket
from socket import *              
serverHost = 'localhost'        # Default IP to connect to
serverPort = 7005               # Default port number
transferSENDHost = 'localhost'
transferGETHost = ''
transferPort = 7006
choice = 'SEND'                 # SEND Request by default

sockobj = socket(AF_INET, SOCK_STREAM)      # Create a TCP socket object
transferSock = socket(AF_INET, SOCK_STREAM) # Create a socket object for transfer use

def mkReq(request):                         # Determine which request was made
    sockobj.send(request.encode('utf-8'))
    reqdata = sockobj.recv(1024)
    receivedmsg = reqdata.decode('utf-8')
    print(receivedmsg)
    if 'success' in receivedmsg:
        return 0
    else:
        return 1

def sendFile():
    filename = input('Enter the file name and extension to SEND (eg. hello.txt): ')
    try:
        f = open(filename, 'rb')
    except OSError as err:
        print("OS error: {0}".format(err))
        return
    
    sockobj.send(filename.encode())         # Send file name to be transferred
    serverResponse()                        # Wait for server response

    transferSock.connect((transferSENDHost, transferPort))  # Create connection to server on port 7006 for transfer
    print('Starting file transfer...')

    sendFile = f.read(4096)
    while(sendFile):
        print('Sending...')
        transferSock.send(sendFile)
        sendFile = f.read(4096)
    f.close()

    transferSock.close()
    print('Sending done!')

def getFile():
    filename = input('Enter the file name and extension to GET (eg. hello.txt): ')
    try:
        f = open(filename, 'wb')
    except OSError as err:
        print("OS error: {0}".format(err))
    sockobj.send(filename.encode())        # Send file name to be transferred
    if serverResponse() == -1:             # Wait for server response
        print('Error! File not found!')
        return

    sockobj.send(transferGETHost.encode('utf-8'))        # Send client host information
    serverResponse()                                     # Wait for server response

    print('Starting Transfer...')

    transferSock.bind((transferGETHost,transferPort))    # Bind to a port number
    transferSock.listen(5)                               # Wait for server to connect before receiving
    conn, address = transferSock.accept()

    print('Server Connection:', address)

    receivedFile = conn.recv(4096)
    while (receivedFile):
        print('Receiving...')
        f.write(receivedFile)
        receivedFile = conn.recv(4096)
    f.close()

    conn.close()
    print('Receiving done!')

def serverResponse():
    data = sockobj.recv(1024)
    print('Received From Server:', data.decode('utf-8'))
    if 'Error' in data.decode('utf-8'):
        return -1     

if len(sys.argv) > 1:
    serverHost = sys.argv[1]    # User has provided a server IP at cmd line arg 1
    transferGETHost = sys.argv[1]
    print('<ip>: ' + sys.argv[1] + ' <GET/SEND>: ' + sys.argv[2])
    if len(sys.argv) > 2:       # User GET and SEND
        choice = sys.argv[2]

sockobj.connect((serverHost, serverPort))   # connect to server IP + port
print('Connection established') 

print('Making Request')

if not mkReq(choice):
    if 'GET' in choice:
        getFile()
    elif 'SEND' in choice:
        sendFile()
else:
    print('Error making request!')

sockobj.close()                