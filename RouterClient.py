from socket import *
from threading import Thread
import json
import traceback
from DVR import *
from RoutingTable import *

# Global variables
nodes = []
neighbors = []
cost_Matrix = []
self_id = 0
routing_Table = RoutingTable()  # Going to be a list of routes


class Node:
    def __init__(self):
        self.nodeIP = ''
        self.nodeID = 0
        self.cost = 0.0


# Opens a socket to listen other nodes
def node_listen_socket(port):
    global nodes
    listen_socket = socket(AF_INET, SOCK_DGRAM)
    listen_socket.bind(('', port))
    while True:
        try:
            message, address = listen_socket.recvfrom(4096)
            # size may need to be adjusted when format of the packet has be finalized
            print str(address)
            # print message
            message = json.loads(message)
            print message
            # Need to parse message and store information
            update_thread = Thread(target=update_routing_table, args=(address[0], message, port,))
            update_thread.start()
        except:
            print "Error in createListenSocket"
            traceback.print_exc()


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
        message = message.strip("[]")
        message = message.replace("'", "")
        message = message.split(',')
        print message

        for i in range(len(message)/2):
            temp_node = Node()
            temp_node.nodeID = int(message[2 * i])
            temp_node.nodeIP = message[2 * i + 1]
            nodes.append(temp_node)
        listen_socket.close()
        print'Leaving server_listen_socket'
        # Need to parse message and store information
        # node address information from server
    except:
        print "Error in server_listen_socket"
        traceback.print_exc()


# Connects to the server to be added to the list of nodes
def connectToServer(TCP_IP, TCP_PORT):
    sock = socket(AF_INET, SOCK_STREAM)
    try:
        sock.connect((TCP_IP, TCP_PORT))
    except:
        print"Error in connectToServer"
        traceback.print_exc()
        connectToServer(raw_input("Enter Server IP and try again: "), TCP_PORT)


# Function to call when sending out routing table information
# Thinking updateNode function will iterate through the nodes list passing each node into this fuction
def send_to_node(node, udp_port, routing_table):
    sock = socket(AF_INET, SOCK_DGRAM)
    global nodes

    route_table_list = []
    for i in range(len(nodes)):
        route = []
        route.append(routing_table.table[i].networkID)
        route.append(routing_table.table[i].nextHop)
        route.append(routing_table.table[i].cost)
        route.append(routing_table.table[i].interface)
        route_table_list.append(route)
    try:
        sock.sendto(json.dumps(route_table_list), (node.nodeIP, udp_port))  # Routing Table will be passed through here
    except:
        print ("Error in send_to_node")
        traceback.print_exc()


# iterate through each node in the neighbors list to pass the updated routing information to each node
def update_nodes(udp_port, data):
    for node in neighbors:
        send_to_node(node, udp_port, data)
    return


# Updates current routing table with new data
def update_routing_table(node_ip, neighbor_routing_table, udp_port):
    global cost_Matrix
    global self_id
    global routing_Table
    next_hops = []
    node_ip_list = []

    # Finds nodeID
    for node in nodes:
        node_ip_list.append(node.nodeIP)
    update_node_id = node_ip_list.index(node_ip)

    # Populate cost matrix with new costs
    for i in range(len(nodes)):
        cost_Matrix[update_node_id][i]= neighbor_routing_table[i][2]
    dvr_cost_Matrix, next_hops = dvr(len(nodes), cost_Matrix)

    for i in range(len(next_hops)):
        routing_Table.table[i].nextHop = nodes[next_hops[i]].nodeIP
        routing_Table.table[i].cost = dvr_cost_Matrix[self_id][i]

    # if cost to any nodes have changed from self.node send an update to neighbors
    if dvr_cost_Matrix[self_id] != cost_Matrix[self_id]:
        update_nodes(udp_port, routing_Table)
    cost_Matrix = dvr_cost_Matrix

    print "New cost matrix"
    print cost_Matrix


def main():
    global cost_Matrix
    global self_id
    global routing_Table
    global nodes
    global neighbors

    TCP_IP = raw_input("Enter Server IP: ")
    TCP_PORT = 8007
    UDP_PORT = 520

    serverConnectThread = Thread(target=connectToServer(TCP_IP,TCP_PORT))
    serverConnectThread.start()
    server_listen_socket(TCP_PORT)  # listens for node information coming from server
    node_listen_thread = Thread(target=node_listen_socket, args=(UDP_PORT,))
    node_listen_thread.start()

    cost_Matrix = [[float('inf') for x in range(len(nodes))] for x in range(len(nodes))]

    # after server node information has been collected
    # Need to compare client IP with nodeIPs to determine nodeID
    self_id = int(raw_input("Enter clients nodeID: "))
    neighbor_input = raw_input('Which nodes am I connecting to (nodeID)? \'-1\' to signal no more neighbors.')
    while neighbor_input != '-1':  # Adds nodes to neighbors by reading nodeID from input
        try:
            neighbors.append(nodes[int(neighbor_input)])
            # Adds neighbor from the nodes list which is filled by the server
        finally:
            neighbor_input = raw_input()
    for i in range(len(nodes)):
        routing_Table.table.append(Route())

    for i in range(len(nodes)):
        routing_Table.table[i].networkID = i
        routing_Table.table[i].cost = 0.0
        routing_Table.table[i].interface = 'Wifi'

    for neighbor in neighbors:
        routing_Table.table[neighbor.nodeID].networkID = neighbor.nodeID
        routing_Table.table[neighbor.nodeID].nextHop = neighbor.nodeIP
        routing_Table.table[neighbor.nodeID].cost = float(raw_input("Enter cost for node " + str(neighbor.nodeID) + ':'))

    # Generate initial cost_Matrix
    for node in neighbors:
        cost_Matrix[self_id][node.nodeID] = routing_Table.table[node.nodeID].cost
    cost_Matrix[self_id][self_id] = 0.0
    routing_Table.print_routing_table()
    print cost_Matrix

    update_nodes(UDP_PORT, routing_Table) # Pass initial routing table to neighbors

    #update_routing_table(nodes[self_id].nodeIP, routing_Table, UDP_PORT)

    while True:
        pass

# ## Start of the program ### #
main_thread = Thread(main())



