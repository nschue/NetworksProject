import random
import threading
from socket import *

nodes = []


class Node:
    nodeIP = ''
    nodeID = 0
    #def _init_(self):
     #   self.nodeID = random.


#Opens listen socket for nodes to connect
def listenSocket(port):
    global nodes
	
    # TCP/IP socket created
    serverSocket = socket(AF_INET, SOCK_STREAM)
    print 'Socket Created'
	
    # The socket gets bound to the port
    serverSocket.bind(('localhost', port))
    serverSocket.listen(5) # Listen for connections
    print 'Listening for connections...'
    
    while True:
        # Establish the connection
        connectionSocket, client_IP = serverSocket.accept()
        print 'Connection made'
		
        # Create a temporary node to hold the IP address of the latest connection
        tempNode = Node()
        tempNode.nodeIP = client_IP[0]
        tempNode.nodeID = len(nodes)
		
        #Check for duplicate nodes
        for x in nodes:
            if(tempNode.nodeIP == x.nodeIP):
			    break
				
        # Add any new nodes to the global list of nodes
        nodes.append(tempNode)
        for x in nodes:
            print 'Node ' + str(x.nodeID) + ': ' + x.nodeIP 
			
        try:
            print 'Connection from', client_IP
            # Send a node ID number followed by its corresponding IP to the client
            for x in nodes:
                connectionSocket.sendall(x.nodeID)
                connectionSocket.sendall(x.nodeIP)

        finally:
            connectionSocket.close()


def main():
    listenThread = threading.Thread(target=listenSocket(8007))
    listenThread.start()

main()
