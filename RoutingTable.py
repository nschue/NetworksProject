

# Individual routes in a routing table
class Route:
    def __init__(self):
        self.networkID = 0
        self.nextHop = ""
        self.cost = 0.0
        self.interface = "WIFI?"

    def update_next_hop(self, next_ip):
        self.nextHop = next_ip

    def update_network_id(self, nework_id):
        self.networkID = nework_id

    def update_cost(self, cost):
        self.cost = cost


# Going to hold routing tables
class RoutingTable:
    def __init__(self):
        self.table = []
        self.nodes = []
        self.neighbors = []

    def create_routing_table(self, nodes, neighbors):
        for node in nodes:
            self.nodes.append(node)
            self.table.append(Route)

        for neighbor in neighbors:
            self.neighbors.append(neighbor)
            self.table[neighbor.nodeID].networkID = neighbor.nodeID


    def print_routing_table(self):
        for route in self.table:
            try:
                print "Target Node: ", route.networkID
            except:
                print "Error, route has no target node."
            try:
                print "Next Hop: ", route.nextHop
            except:
                print "Error, route has no next hop."
            try:
                print "Cost: ", route.cost
            except:
                print "Error, route has no cost."
            try:
                print "Interface: ", route.interface
            except:
                print "Error, route has no interface"





