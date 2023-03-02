import Foundation

var connectionIDs = [String: TimeInterval]()

func isUsed(connectionID: String) -> Bool {
    return connectionIDs.keys.contains(connectionID)
}

func main() throws {
    let arguments = CommandLine.arguments
    
    if arguments.count != 3 {
        throw NSError(domain: "Missing command line arguments", code: 0, userInfo: nil)
    }
    
    let serverIP = arguments[1]
    guard let serverPort = Int32(arguments[2]) else {
        throw NSError(domain: "Port number is not an integer", code: 0, userInfo: nil)
    }
    
    // open a socket on a specific port as a server for TCP
    let serverSocket = try! ServerSocket(port: serverPort, address: serverIP)
    
    // listen to connection
    try! serverSocket.listen()
    
    // Receive a request which consists of a HELLO and a connectionID.
    while true {
        do {
            // accept the client connection
            let connectionSocket = try serverSocket.accept()
            // do not receive any requests from any clients for two minutes (server exit timeout)
            connectionSocket.readTimeout = 120
            
            for (connectionID, lastConnectionTime) in connectionIDs {
                if Date().timeIntervalSince1970 - lastConnectionTime >= 10 {
                    connectionIDs.removeValue(forKey: connectionID)
                    print("it is 10 seconds already, \(connectionID) is being removed")
                }
            }
            
            // receive the message and address from the client
            let data = try connectionSocket.read()
            let message = String(data: data, encoding: .utf8)!
            let messageComponents = message.split(separator: " ")
            let message = String(messageComponents[0])
            let connectionID = String(messageComponents[1])
            
            let clientAddress = try connectionSocket.peerHostname()
            
            if !isUsed(connectionID: connectionID) {
                let response = "OK \(connectionID) \(clientAddress) \(connectionSocket.peerPort)"
                print(clientAddress)
                
                // keep track of the initial timer
                connectionIDs[connectionID] = Date().timeIntervalSince1970
                print(connectionIDs)
                
                // send the message back to the client
                try connectionSocket.write(response.data(using: .utf8)!)
            } else {
                let response = "RESET \(connectionID)"
                // send the message back to the client
                try connectionSocket.write(response.data(using: .utf8)!)
            }
        } catch let error as SocketError {
            if error.kind == .timeout {
                throw error
            } else {
                print("Error: \(error)")
            }
        }
    }
}

do {
    try main()
} catch let error as NSError {
    print(error.localizedDescription)
}
