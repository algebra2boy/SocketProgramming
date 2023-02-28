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
        message         = f"{message} {connectionID}"
    except: 
        raise Exception("it is not a a good port number or connection ID")
    

    # open a socket on a specific port as a server for UDP
    clientSocket = socket(AF_INET, SOCK_DGRAM)

    # send message to the server using the client socket 
    clientSocket.sendto(message.encode(), (serverIP, serverPort))

    # read reply data from socket 
    newMessage, serverAddress = clientSocket.recvfrom(4096)
    print(newMessage.decode())
    # close the socket 
    clientSocket.close()
    


if __name__ == "__main__":
   main()