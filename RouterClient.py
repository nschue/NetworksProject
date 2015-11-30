from socket import *
import threading

class Node:
    nodeIP = ''
    nodeID = 0

#Opens a socket to listen other nodes
def createListenSocket(port):
    global nodes
    listenSocket = socket(AF_INET, SOCK_STREAM)
    print 'Socket Created'
    listenSocket.bind(('', port))
    listenSocket.listen(5)
    print 'Ready to serve...'
    while True:
        # Establish the connection
        connectionSocket, addr = listenSocket.accept()
        try:
            message = connectionSocket.recv(1024) #size may need to be adjusted when format of the packet format has be finalized
            print message
            #Need to parse message and store information
            #Two possible types of messages, routing table updates from other nodes, node address information from server

#Connects to the server to be added to the list of nodes
def connectToServer(TCP_IP,TCP_PORT):
    sock = socket(AF_INET,SOCK_STREAM)
    sock.connect((TCP_IP,TCP_PORT))


def sendToNode():


def main():
    TCP_IP = '76.183.92.14'
    TCP_PORT = 8007
    serverConnectThread = threading.Thread(target=connectToServer(TCP_IP,TCP_PORT))
    serverConnectThread.start()

    while True:
        pass



main()



