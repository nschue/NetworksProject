from socket import *

class Node:
    nodeIP = ''
    nodeID = 0

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


def connectToServer(TCP_IP,TCP_PORT):
    sock = socket(AF_INET,SOCK_STREAM)
    sock.connect((TCP_IP,TCP_PORT))

def main():
    TCP_IP = '76.183.92.14'
    TCP_PORT = 8007

    connectToServer(TCP_IP,TCP_PORT)
    while True:
        pass



main()



