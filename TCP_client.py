from socket import * # socket interface API
import sys # command line arguments 
from datetime import datetime

def main():
    argv = sys.argv

    if len(argv) < 5:
        raise Exception("missing command line arguments")
    elif len(argv) > 5:
        raise Exception("excessive command line arguments")

    # reading the argument from the terminal
    messageHELLO    = argv[1]
    serverIP        = argv[2]

    # vallidating port # and connection ID
    try: 
        serverPort      = int(argv[3])
        connectionID    = int(argv[4])
    except: 
        raise Exception("Port number or connection ID is not integer")
    
    numOfTries = 0
    while numOfTries < 3:
        # open a socket on a specific port as a server for TCP
        clientSocket = socket(AF_INET, SOCK_STREAM)

        # the client does not receive a reply within 15 seconds
        clientSocket.settimeout(15)
        try:
            
            message  = f"{messageHELLO} {connectionID}"

            # connect to the server
            try: 
                clientSocket.connect((serverIP, serverPort))
            except ConnectionRefusedError: 
                print(f"Connection Failure on {datetime.now()}")
                clientSocket.close()
                exit()
                
            # send message to the server using the client socket 
            clientSocket.send(message.encode())

            # read reply data from socket 
            newMessage = clientSocket.recv(4096)
            
            # either OK or RESET
            newMessage    = newMessage.decode().split(" ")
            statusMessage = newMessage[0]

            # respond to different response
            if statusMessage == "OK":
                print(f"Connection established {connectionID} {newMessage[2]} {newMessage[3]} on {datetime.now()}")
                clientSocket.close()
                exit()
            elif statusMessage == "RESET": 
                clientSocket.close()
                print(f"Connection Error {connectionID} on {datetime.now()}")
                numOfTries += 1
                connectionID = input("Enter a new connection ID: ")
        # error such that client does not reply within 15 minutes
        except timeout:
            print(f"Connection Error {connectionID} on {datetime.now()}")
            clientSocket.close()
            numOfTries += 1
            connectionID = input("Enter a new connection ID: ")
    print(f"Connection Failure on {datetime.now()}")

if __name__ == "__main__":
   main()