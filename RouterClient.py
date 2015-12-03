from socket import *
import threading

# Global variables
nodes = []
neighbors = []
cost_Matrix = [[float('inf') for x in range(20)] for x in range(20)]


class Node:
    def __init__(self):
        self.nodeIP = ''
        self.nodeID = 0


# Opens a socket to listen other nodes
def node_listen_socket(port):
    global nodes
    listen_socket = socket(AF_INET, SOCK_STREAM)
    print 'Socket Created'
    listen_socket.bind(('', port))
    listen_socket.listen(5)
    print 'Ready to serve...'
    while True:
        # Establish the connection
        connectionSocket, addr = listen_socket.accept()
        try:
            message = connectionSocket.recv(1024)
            # size may need to be adjusted when format of the packet has be finalized
            print message
            # Need to parse message and store information
        except:
            print "Error in createListenSocket"


def server_listen_socket(port):
    global nodes
    listen_socket = socket(AF_INET, SOCK_STREAM)
    print 'Socket Created'
    listen_socket.bind(('', port))
    listen_socket.listen(0)
    print 'Ready to serve...'
    # Establish the connection
    try:
        connection_socket, addr = listen_socket.accept()
        message = connection_socket.recv(1024)
        # size may need to be adjusted when format of the packet has be finalized
        print message
        message = message.split(',')
        message = message.strip('[]')
        for i in range(len(message)/2):
            temp_node = Node()
            temp_node.nodeID = int(message[2 * i])
            temp_node.nodeIP = message[2 * i + 1]
            nodes.append(temp_node)

        # Need to parse message and store information
        # node address information from server
    except:
        print "Error in server_listen_socket"

# Connects to the server to be added to the list of nodes
def connectToServer(TCP_IP, TCP_PORT):
    sock = socket(AF_INET, SOCK_STREAM)
    try:
        sock.connect((TCP_IP, TCP_PORT))
    except:
        print"Error in connectToServer"
        connectToServer(raw_input("Enter Server IP and try again: "), TCP_PORT)


# Function to call when sending out routing table information
# Thinking updateNode function will iterate through the nodes list passing each node into this fuction
def send_to_node(node,TCP_PORT, data):
    sock = socket(AF_INET, SOCK_STREAM)
    try:
        sock.connect((node.nodeIP, TCP_PORT))
        sock.send(data)  # Routing Table will be passed through here
    except:
        print ("Error in send_to_node")


# iterate through each node in the neighbors list to pass the updated routing information to each node
def update_nodes(TCP_PORT, data):
    for node in neighbors:
        send_to_node(node, TCP_PORT, data)
    return


def main():
    global cost_Matrix
    TCP_IP = raw_input("Enter Server IP: ")
    TCP_PORT = 8007
    serverConnectThread = threading.Thread(target=connectToServer(TCP_IP,TCP_PORT))
    serverConnectThread.start()
    server_listen_socket(TCP_PORT) # listens for node information coming from server

    # after server node information has been collected
    print 'I am node: '  # Need to compare client IP with nodeIPs to determine nodeID
    self_ID = 0
    neighbor_input = raw_input('Which nodes am I connecting to (nodeID)? \'-1\' to signal no more neighbors.')
    while neighbor_input != '-1':  # Adds nodes to neighbors by reading nodeID from input
        try:
            neighbors.append(nodes[int(neighbor_input)])
            # Adds neighbor from the nodes list which is filled by the server
        finally:
            neighbor_input = raw_input()
    print 'Neighbor nodes are: '
    for node in neighbors:
        print "Node", node.nodeID
        cost_Matrix[self_ID][node.nodeID] = 1;
    print cost_Matrix
    # need to add distance to neighbors here
    while True:
        pass

# ## Start of the program ### #
main()



