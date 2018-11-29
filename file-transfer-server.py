#!/usr/bin/python

"""
TCP File Transfer Server

Author:

Piyotr Kao

A00996404
"""

from socket import *
import os
import time            
linkHost = ''                                 # '' to set the default IP to localhost
linkPort = 7005                               # Default port number
transferHost = ''                             # Host name for file transfer
transferPort = 7006                           # Host port for file transfer

sockobj = socket(AF_INET, SOCK_STREAM)      # Create a TCP socket object
sockobj.bind((linkHost, linkPort))              # bind it to server port number
transferSock = socket(AF_INET,SOCK_STREAM)

sockobj.listen(1)

request = ''

def getFile():
    data = connection.recv(4096)              # Wait for client to enter filename
    if data:
        connection.send(b'File name received')
        f = open(data.decode('utf-8'), 'wb')
    else:
        print('filename not received')
        return
    print('Starting Transfer...')

    transferSock.bind((transferHost,transferPort))
    transferSock.listen(5)
    conn, address = transferSock.accept()
    print('Client Connection:', address)

    receivedFile = conn.recv(4096)
    while (receivedFile):
        print('Receiving...')
        f.write(receivedFile)
        receivedFile = conn.recv(4096)
    f.close()

    conn.close()
    print('Receiving done!')

def sendFile():
    filename = connection.recv(1024)           # Wait for client to enter filename
    try:
        f = open(filename.decode('utf-8'), 'rb')
    except OSError as err:
        print("OS error: {0}".format(err))
        connection.send(b'Error, file does not exist!')
        return
    connection.send(b'File found!')
    print('file: ' + filename.decode('utf-8') + ' was found!')

    c_HostName = connection.recv(1024)         # Get client host address
    transferHost = c_HostName.decode('utf-8')
    connection.send(b'Host name received!')
    
    print('Starting file transfer...')
    transferSock.connect((transferHost, transferPort))

    sendFile = f.read(4096)
    while(sendFile):
        print('Sending...')
        transferSock.send(sendFile)
        sendFile = f.read(4096)
    f.close()

    transferSock.close()
    print('Sending done!')

while True:
    connection, address = sockobj.accept()
    print('Client Connection:', address)
    print('Processing request...')

    while True:                              # Receive request made first
        data = connection.recv(1024)
        if data:
            break

    request = data.decode('utf-8')
    print('A ' + request + ' request was received')
    connection.send(b'A ' + request.encode() + b' request was successfully received')

    if 'GET' in request:
        sendFile()
    elif 'SEND' in request:
        getFile()

    connection.close()