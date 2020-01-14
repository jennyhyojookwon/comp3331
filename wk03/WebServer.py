# coding: utf-8

# COMP3331 week03 exercise4: A simple Web Server
# Author: HyoJoo Kwon (z5222646)


# how to create a socket, bind it to a specific address and port, 
# as well as send and receive an HTTP packet. 
# You will develop a web server that handles one HTTP request at a time.


# (i) create a connection socket when contacted by a client (browser).
# (ii) receive HTTP request from this connection. Your server should only process GET request. You may assume that only GET requests will be received.
# (iii) parse the request to determine the specific file being requested.
# (iv) get the requested file from the server's file system.
# (v) create an HTTP response message consisting of the requested file preceded by header lines.
# (vi) send the response over the TCP connection to the requesting browser.
# (vii) If the requested file is not present on the server, the server should send an HTTP “404 Not Found” message back to the client.
# (viii) the server should listen in a loop, waiting for next request from the browser.


# refererred to TCPServer.py
from socket import *

# other than 80 and 8080, and > 1024
serverPort = 10000
# This line creates the server’s socket.
serverSocket = socket(AF_INET, SOCK_STREAM)		
# The above line binds (that is, assigns) the port number 10000 to the server’s socket.
serverSocket.bind(('localhost', serverPort))	
# The serverSocket then goes in the listen state to listen for client connection requests. 					
serverSocket.listen(1)		
								
print "The server is ready to receive\n"						

while 1:
    # When a client knocks on this door, the program invokes the accept( ) method for serverSocket, 
    # which creates a new socket in the server, called connectionSocket, dedicated to this particular client. 
    # The client and server then complete the handshaking, creating a TCP connection between the client’s clientSocket 
    # and the server’s connectionSocket. With the TCP connection established, the client and server can now send bytes 
    # to each other over the connection. With TCP, all bytes sent from one side not are not only guaranteed to arrive 
    # at the other side but also guaranteed to arrive in order
    connectionSocket, addr = serverSocket.accept()			

    try:
		# wait for data to arrive from the client
        data = connectionSocket.recv(1024)				
        # parse the request to determine the specific file being requested.
        request = data.split()[1];	
        # print "Request: ", request, '\n'
        # remove slash					
        fileName = request.replace('/', '')					
        print fileName, '\n'	

        # open file
        file = open(fileName)		
        # read file					
        output = file.read()	
        # send HTTP header response						
        connectionSocket.send('HTTP/1.1 200 OK\n\n')
        # send HTTP text reponse		
        connectionSocket.send(output)					
        connectionSocket.close()
	# IO Exception
    except IOError:
        connectionSocket.send('HTTP/1.1 404 File not found\n\n')
        # sending a custom error message in the body of your response.
        connectionSocket.send('404 not found')
        connectionSocket.close()