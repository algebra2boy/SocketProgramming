## Project description

This project is used for learning the socket programming using the socket API from python. 
UDP and TCP are being studied and the topics of timeout. 


## Execution
```python
How to run the client:
$ python3 your_client.py HELLO Server_IP Server_Port ConnectionID

How to run the server: 
$ python3 your_server.py Server_IP Server_Port
```

## Server response
server will keep a list of in-use connectionID and two types of response that the server will respond
- OK: If the connectionID specified by the client is not in use, your server adds the connectionID to its list of in-use IDs and responds with an OK message
    - the server includes the client IP address and client port number in its return message. Thus, the server message looks like “OK ConnectionID Client_IP Client_Port”
    - Example would be "OK 9876 192.168.0.10 12345"
- Reset: If the connectionID specified by the client is in use, your server responds with a RESET message. The RESET message starts with the string “RESET” and echoes back the client-provided connectionID.
    -  the server message is “RESET ConnectionID”.
    -  For example, "RESET 9876"


## Time out

Client Side
- If the client receives an OK message, it prints out a “Connection established” message, indicating the connectionID, its IP address, its port number, and the current timestamp. Then, the client exits gracefully after closing any open sockets.
-  If the client doesn’t receive a reply within **15** seconds, it should timeout and follow the protocol below 
- Suppose the client receives a RESET message or timeouts after **15** seconds. In that case, it prints out a “Connection Error” message with the connection ID and the current timestamp, and asks the user to enter a new connection ID. Then, it retries to establish a connection again with a newly created socket and with this newly entered connection ID to the same server. After **three** tries to establish a connection without success to the same server, the client prints a “Connection Failure” message with the current timestamp and exits gracefully after closing any open sockets.
    - Connection Error print out example: “Connection Error 2678 on 2023- 01-16 06:06:06.123456”
    - After three tries, print out: “Connection Failure on 2023-01-16 06:06:06.123456”


Server Side: 
- waiting for a connection request but does not receive any requests from any clients for **two** minutes, your server should timeout and exit gracefully after closing any open sockets.
- ConnectionID Timeout: your server should timeout and remove connectionIDs that have been in its connectionID list for more than **30** seconds




