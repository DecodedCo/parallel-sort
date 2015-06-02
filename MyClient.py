import socket   #for sockets
import sys  #for exit
import MergeSort 
 
try:
    #create an AF_INET, STREAM socket (TCP)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    sys.exit();
 
print 'Socket Created'

try:
	remote_ip = str(sys.argv[2])
except:
	remote_ip = '127.0.0.1'

try:
	port = int(sys.argv[1])
except:
	port = 5003
 
 
#Connect to remote server
s.connect((remote_ip , port))
 
print 'Socket Connected to' + remote_ip

arraystring = ''

#Now receive data and process

while True:
	dataIn = s.recv(4096)
	arraystring += dataIn
	if ']' in dataIn:	 #When end of data is received
		break

#sort the data
array = eval(arraystring)	
print 'Data received, sorting array of length ', len(array) 

array = MergeSort.mergesort(array) 
print 'Array sorted, sending data...' 
	
arraystring = repr(array) 
s.sendall(arraystring)

s.close()