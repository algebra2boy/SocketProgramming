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
    
    # reading the argument from the terminal
    serverIP   = argv[1]
    try: 
        serverPort = int(argv[2])
    except: 
        raise Exception("port number is not an integer")

    # open a welcoming socket on a specific port as a server for TCP
    serverSocket = socket(AF_INET, SOCK_STREAM)

    # bind the port number 
    serverSocket.bind((serverIP, serverPort))

    # listen to connection
    serverSocket.listen(1)

    # Receive a request which consists of a HELLO and a connectionID.
    while True: 
        serverSocket.settimeout(120)

        # accept the client connection
        try: 
            connectionSocket, clientAddress = serverSocket.accept()
        except TimeoutError:
            break
        else:
            # do not receive any requests from any clients for two minutes (server exit timeout)
            try:
                # receve the message and address from the client 
                message = connectionSocket.recv(4096)

                # check connection ID more than 30 seconds
                for connectID in list(connectionIDs): 
                    if time.time() - connectionIDs[connectID] >= 30:
                        connectionIDs.pop(connectID)

                decoded_message = message.decode()

                message, connectionID = decoded_message.split(" ")[0], decoded_message.split(" ")[1]

                # set up the response and send the message back to the client 
                if not isUsed(connectionID):
                    response = f"OK {connectionID} {clientAddress[0]} {clientAddress[1]}"

                    # keep track of the intial timer
                    connectionIDs[connectionID] = time.time()
                else: 
                    response = f"RESET {connectionID}"
                connectionSocket.send(response.encode())
            # server does not receive the response from the client within 2 minutes
            except timeout:
                connectionSocket.close()
                exit()
    serverSocket.close()
            
if __name__ == "__main__":
   main()