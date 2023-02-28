from socket import * # socket interface API
import sys # command line arguments 
from datetime import datetime



def main():
    argv = sys.argv

    if len(argv) != 5:
        raise Exception("missing or excessive command line arguments")

    message         = argv[1]
    serverIP        = argv[2]

    # these must be integers
    try: 
        serverPort      = int(argv[3])
        connectionID    = int(argv[4])
    except: 
        raise Exception("it is not a a good port number or connection ID")
    
    numOfTries = 0
    while numOfTries < 3:
        # open a socket on a specific port as a server for UDP
        clientSocket = socket(AF_INET, SOCK_DGRAM)

        # the clienr does not receive a reply within 15 seconds
        clientSocket.settimeout(15)
        try:
            
            message  = f"{message} {connectionID}"
            # send message to the server using the client socket 
            clientSocket.sendto(message.encode(), (serverIP, serverPort))

            # read reply data from socket 
            newMessage, serverAddress = clientSocket.recvfrom(4096)
            
            # either OK or RESET
            newMessage    = newMessage.decode().split(" ")
            statusMessage = newMessage[0]

            print(newMessage)
            if statusMessage == "OK":
                # Connection established connectionID IP port
                print(f"Connection established {connectionID} {newMessage[2]} {newMessage[3]} on {datetime.now()}")
                clientSocket.close()
                exit()
            else: 
                print(f"Connection Error {connectionID} on {datetime.now()}")
                numOfTries += 1
                clientSocket.close()
        except timeout:
            # close the socket 
            clientSocket.close()
            print(f"Connection Error {connectionID} on {datetime.now()}")
            numOfTries += 1
            connectionID = input("Enter a new connection ID")
    


if __name__ == "__main__":
   main()