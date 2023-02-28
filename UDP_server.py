from socket import * # socket interface API
import sys # command line arguments 
from datetime import datetime

usedConnectionID = []

def isUsed(connectionID) -> bool: 
    return connectionID in usedConnectionID

def main():
    argv = sys.argv

    if len(argv) !=3:
        raise Exception("missing command line arguments")

    try: 
        serverIP   = argv[1]
        serverPort = int(argv[2])
    except: 
        raise Exception("it is not a a good port number")

    # open a socket on a specific port as a server for UDP
    serverSocket = socket(AF_INET, SOCK_DGRAM)

    # bind the port number 
    serverSocket.bind(("", serverPort))

    # Receive a request which consists of a HELLO and a connectionID.
    while True: 
        # receve the message and address from the client 
        message, clientAddress = serverSocket.recvfrom(4096)
        
        decoded_message = message.decode()

        message, connectionID = decoded_message.split(" ")[0], decoded_message.split(" ")[1]

        if not isUsed(connectionID):
            response = f"OK {connectionID} {clientAddress[0]} {clientAddress[1]}"
            usedConnectionID.append(connectionID)
        else: 
            response = f"RESET {connectionID}"

        # send the message back to the client 
        serverSocket.sendto(response.encode(), clientAddress)

    



if __name__ == "__main__":
   main()