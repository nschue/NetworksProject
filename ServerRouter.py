import random
import threading
from socket import *

nodes = []


class Node:
    nodeIP = ''
    nodeID = 0
    #def _init_(self):
     #   self.nodeID = random.


# Opens listen socket for nodes to connect
def listenSocket(port, numberOfNodes):
    global nodes

    # TCP/IP socket created
    serverSocket = socket(AF_INET, SOCK_STREAM)
    print 'Socket Created'

    # The socket gets bound to the port
    serverSocket.bind(('localhost', port))
    serverSocket.listen(5) # Listen for connections
    print 'Listening for connections...'
    
    while nodes.lenth() < numberOfNodes:
        # Establish the connection
        connectionSocket, client_IP = serverSocket.accept()
        print 'Connection made'

        # Create a temporary node to hold the IP address of the latest connection
        tempNode = Node()
        tempNode.nodeIP = client_IP[0]
        tempNode.nodeID = len(nodes)

        # Check for duplicate nodes
        for x in nodes:
            if(tempNode.nodeIP == x.nodeIP):
                break

        # Add any new nodes to the global list of nodes
        nodes.append(tempNode)
        connectionSocket.close()
        for x in nodes:
            print 'Node ' + str(x.nodeID) + ': ' + x.nodeIP 



def sendToNode(client_IP,TCP_PORT):
    # TCP/IP socket created
    sock = socket(AF_INET,SOCK_STREAM)
    try:
        sock.connect((client_IP,TCP_PORT))
        print 'Connection from', client_IP

        # Send a node ID number followed by its corresponding IP to the client
        for x in nodes:
            sock.sendall(x.nodeID)
            sock.sendall(x.nodeIP)

    finally:
        sock.close()

def main():
    numberOfNodes = raw_input("How many nodes are in the network? ")
    listenThread = threading.Thread(target=listenSocket(8007, numberOfNodes))
    listenThread.start()
    for node in nodes:
        sendToNode(node.IP, 8007)


main()
