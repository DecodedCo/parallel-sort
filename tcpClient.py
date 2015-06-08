from socket import *
import MergeSort 
import sys
def process(clientsocket, data):
    #sort the data
    print "sorting data"
    array = eval(data)   
    print 'Data received, sorting array of length ', len(array) 

    array = MergeSort.mergesort(array) 
    print 'Array sorted, sending data...' 
        
    data = repr(array) 
    clientsocket.sendall(data)

if __name__ == '__main__':

    try:
        port = int(sys.argv[1])
    except:
        port = 55555

    try:
        host = sys.argv[2]
    except:
        host = 'localhost'

    arraystring = ''  
    buf = 1024
 
    addr = (host, port)
 
    clientsocket = socket(AF_INET, SOCK_STREAM)
 
    clientsocket.connect(addr)
 
    while 1:
        data = raw_input(">> ")
        if not data:
            break
        else:
            clientsocket.send(data)
            data = clientsocket.recv(buf)
            if not data:
                break
            elif data == "MAXIMUM": #data is comming...
                print "Maximum number of clients reached. Exiting"
                clientsocket.close()
                sys.exit() 
            elif data == "REQUEST": #data is comming...
                print "data is coming..."
                #receive data from server
                while ']' not in arraystring:
                    dataIn = clientsocket.recv(4096)
                    arraystring += dataIn
                    if ']' in dataIn:    #When end of data is received
                        # print arraystring
                        process(clientsocket, arraystring)
                        arraystring = ''
                        break
    
    clientsocket.close()