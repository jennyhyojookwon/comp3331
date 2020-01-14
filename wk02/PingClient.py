# PingClient.py
# written by: HyoJoo Kwon (Jenny)
# zID: z5222646
# sends 10 ping requests to the server. 
# Each message contains a payload of data that includes the keyword PING, a sequence number, and a timestamp. 

# python version: 2.7.10
# referred to sample client server resourses from webCMS

from socket import *
import time
import array


# use 127.0.0.1 (i.e., localhost) for host when running your client
serverName = '127.0.0.1'
# pick a port number greater than 1024
serverPort = 10000

# create a socket
clientSocket = socket(AF_INET, SOCK_DGRAM)
# You should have the client wait up to one second for a reply
clientSocket.settimeout(1)

# list to store rtt values for later to compute min, max, average
list = []
sequence = 0
while sequence < 10:
    try:
        # returns the time as a floating point number expressed in seconds since the epoch, in UTC.
        sendTime = time.time()

        # string format : PING sequence_number time CRLF
        # Each message contains a sequence of characters terminated by a carriage return 
        # (CR) character (\r) and a line feed (LF) character (\n)
        ping = 'PING' + str(sequence) + ' ' + str(sendTime) + '\r\n'
        # sendto() calls for UDP
        clientSocket.sendto(ping, (serverName, serverPort))
        # recvfrom() calls for UDP
        reply, serverAddress = clientSocket.recvfrom(2048)
        recieveTime = time.time()
        # The client should send one ping and then wait either for the reply from the server or a timeout before transmitting the next ping.
        time.sleep(1)

    # If one second goes by without a reply from the server, then the client assumes that its packet or the server's reply packet has been lost in the network.
    except timeout:
        print 'Ping to ' + serverName + ', seq = ' + str(sequence) + ', time out'
        sequence += 1
        continue

    # compute RTT, the difference between when the packet was sent and the reply was received
    # read the system time in milliseconds
    rtt = int(round(recieveTime - sendTime, 3) * 1000)

    list.append(rtt)
    #print(list)
    print 'Ping to ' + serverName + ', seq = ' + str(sequence) + ', rtt = ' + str(rtt) + ' ms'
    sequence += 1

# need to report the minimum, maximum and the average RTTs of all packets received successfully at the end of your program's output.
average = sum(list) / len(list)
print '\n----rtt record----\n'
print 'minimum rtt: ' +  str(min(list))
print 'maximum rtt: ' +  str(max(list))
print 'average: ' +  str(sum(list)/len(list))
clientSocket.close()
