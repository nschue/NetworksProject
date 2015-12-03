class node:
    def __init__(self, ID=None, dist = None, fro = None):
        self.ID   = ''
        self.dist = [0]*20
        self.fro  = [0]*20


def dvr(number_nodes, costmat):
    rt = [0]*10

    for i in range(10):
        rt.insert(i, node('ID', 0, 0))

    print 'Number of nodes: ',number_nodes
    number_nodes=int(number_nodes)

    for i in range(number_nodes):
        for j in range(number_nodes):
            costmat[i][i]=0
            rt[i].dist[j]=costmat[i][j]
            rt[i].fro[j]=j

    for i in range(number_nodes):
        for j in range(number_nodes):
            for k in range(number_nodes):
                if rt[i].dist[j]>costmat[i][k]+rt[k].dist[j]:
                    rt[i].dist[j]=rt[i].dist[k]+rt[k].dist[j]
                    rt[i].fro[j]=k

    for i in range(number_nodes):
        for j in range(number_nodes):
            costmat[i][j] = rt[i].dist[j]
    return costmat


