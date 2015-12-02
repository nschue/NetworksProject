from socket import *
import threading

# Global variables
nodes = []
neighbors = []
cost_matrix = [[0 for x in range(20)] for x in range(20)]


class Node:
    def __init__(self):
        self.nodeIP = ''
        self.nodeID = 0


# Opens a socket to listen other nodes
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
            message = connectionSocket.recv(1024)
            # size may need to be adjusted when format of the packet has be finalized
            print message
            # Need to parse message and store information
            # Two possible types of messages, routing table updates from other nodes,
            # node address information from server
        except:
            print "Error in createListenSocket"


# Connects to the server to be added to the list of nodes
def connectToServer(TCP_IP, TCP_PORT):
    sock = socket(AF_INET, SOCK_STREAM)
    try:
        sock.connect((TCP_IP,TCP_PORT))
    except:
        print"Error in connectToServer"


# Function to call when sending out routing table information
# Thinking updateNode function will iterate through the nodes list passing each node into this fuction
def sendToNode(node,TCP_PORT, data):
    sock = socket(AF_INET, SOCK_STREAM)
    try:
        sock.connect((node.nodeIP, TCP_PORT))
        sock.send(data)  # Routing Table will be passed through here
    except:
        print ("Error in sendToNode")
    return


# iterate through each node in the neighbors list to pass the updated routing information to each node
def updateNodes(TCP_PORT, data):
    for node in neighbors:
        sendToNode(node, TCP_PORT, data)
    return


def main():
    TCP_IP = raw_input("Enter Server IP: ")
    TCP_PORT = 8007
    serverConnectThread = threading.Thread(target=connectToServer(TCP_IP,TCP_PORT))
    serverConnectThread.start()
    # listen for information from server
    # after server node information has been collected
    print 'I am node: '
    neighbor_input = raw_input('Which nodes am I connecting to (nodeID)? \n\'-1\' to signal no more neighbors.')
    while neighbor_input != '-1':
        try:
            neighbors.append(nodes[int(neighbor_input)])  # Adds neighbor from the nodes list which is filled by the server
        finally:
            neighbor_input = raw_input()
    print 'Neighbor nodes are: '
    for node in neighbors:
        print "Node", node.nodeID

    while True:
        pass

# ## Start of the program ### #
main()



