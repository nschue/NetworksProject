import random
import threading
from socket import *

nodes = []


class Node:
    nodeIP = ''
    nodeID = 0
    #def _init_(self):
     #   self.nodeID = random.



def listenSocket(port):
    global nodes
    serverSocket = socket(AF_INET, SOCK_STREAM)
    print 'Socket Created'
    serverSocket.bind(('', port))
    serverSocket.listen(5)
    print 'Ready to serve...'
    while True:
        # Establish the connection
        connectionSocket, addr = serverSocket.accept()
        tempNode = Node()
        tempNode.nodeIP = addr[0]
        tempNode.nodeID = len(nodes)
        nodes.append(tempNode)
        for x in nodes:
            print 'Node ' + str(x.nodeID) + ': ' + x.nodeIP



def main():
    listenThread = threading.Thread(target=listenSocket(8007))
    listenThread.start()

main()