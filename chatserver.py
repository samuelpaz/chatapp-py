#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from socket import *
from threading import Thread

def accept_incoming_connections():
    
    while True:
        client, client_address = SERVER.accept()
        print("%s: %s connected." % client_address)
        client.send(bytes(" Greetings from the batcave! " +
                            "Now, type you nick and press [Enter]", "utf8"))
        addresses[client] = client_address
        Thread(target = handle_client, args = (client,)).start()

def handle_client(client):

    name = client.recv(BUFFSIZE).decode("utf8")
    # Close connection if a nickname isn't given before client close the window.
    if name == "/quit":
        client.close()
        return

    # If nickname already exists, type a different nickname
    while name in nicks:
        client.send(bytes(" Sorry, this nick is already taken. Type a different nick.", "utf8"))
        name = client.recv(BUFFSIZE).decode("utf8")
                
    clients[client] = name
    nicks.append(name)
    welcome = ' Welcome %s! If you ever want quit, type /quit to exit.\n' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat." % name
    broadcast(bytes(msg, "utf8"))

    # Receiving messages
    while True:

        msg = client.recv(BUFFSIZE)
        if msg != bytes("/quit", "utf8"):
            broadcast(msg, name + ": ")
        else:
            client.close()
            del clients[client]
            nicks.remove(name)
            broadcast(bytes("%s has left the chat."% name, "utf8"))
            break

# Transmit messages for all clients
def broadcast (msg, prefix = ""):
    
    for sock in clients:
        sock.send(bytes(" » " + prefix, "utf8")+ msg)
        # Show chat on server side, for future log implementation if desired
        print(prefix, msg)

nicks = []
clients = {}
addresses = {}

HOST = ''
PORT = 33000
BUFFSIZE = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)


if __name__ == "__main__":
    # Maximum 20 connections
    SERVER.listen(20)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target = accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
