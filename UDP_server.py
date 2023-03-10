from socket import * # socket interface API
import sys # command line arguments 
from datetime import datetime
import time

connectionIDs = {}

def isUsed(connectionID) -> bool: 
    '''
        Check whether the connectionID is in the list
        Return: (bool) True if the connection is there, false otherwise
    '''
    return connectionID in connectionIDs

def main():
    argv = sys.argv

    if len(argv) !=3:
        raise Exception("missing command line arguments")
        
    serverIP   = argv[1]
    try: 
        serverPort = int(argv[2])
    except: 
        raise Exception("port number is not an integer")

    # open a socket on a specific port as a server for UDP
    serverSocket = socket(AF_INET, SOCK_DGRAM)

    # bind the port number 
    serverSocket.bind((serverIP, serverPort))

    # Receive a request which consists of a HELLO and a connectionID.
    while True: 

        # do not receive any requests from any clients for two minutes (server exit timeout)
        serverSocket.settimeout(120)

        try:
            # receve the message and address from the client 
            message, clientAddress = serverSocket.recvfrom(4096)

            # check connection ID more than 30 seconds
            for connectID in list(connectionIDs): 
                if time.time() - connectionIDs[connectID] >= 30:
                    connectionIDs.pop(connectID)
            
            decoded_message = message.decode()

            message, connectionID = decoded_message.split(" ")[0], decoded_message.split(" ")[1]

            if not isUsed(connectionID):
                response = f"OK {connectionID} {clientAddress[0]} {clientAddress[1]}"

                # keep track of the intial timer
                connectionIDs[connectionID] = time.time()

            else: 
                response = f"RESET {connectionID}"

            # send the message back to the client 
            serverSocket.sendto(response.encode(), clientAddress)
        # error such that the server does not recieve any reply within 120 minutes
        except timeout:
            serverSocket.close()
            exit()
            
if __name__ == "__main__":
   main()