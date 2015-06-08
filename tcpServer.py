import socket
import thread
import random 
import threading
from Handler import handler
import MergeSort   #Imports mergesort functions 

#breaks down array into n sections where n is the number of processors 
def breakArray(array, n): 

    sectionlength = len(array)/n    #length of each section 

    result = [] 

    for i in range(n):
        if i < n - 1: # n - 1 as the last client will take any left over data aswell
            result.append( array[ i * sectionlength : (i+1) * sectionlength ] )
        #include all remaining elements for the last section 
        else:
            result.append( array[ i * sectionlength : ] )
    return result

def errorReturn(conn, message):
    print message
    arraystring = repr(message)
    conn.send(arraystring)
    conn.close()

#main
if __name__ == "__main__":
    
    #get port
    try:
        port = int(sys.argv[1])
    except:
        port = 55555
    #get thread count
    try:
        clientCount = int(sys.argv[2])
    except:
        clientCount = 2

    print "port: " + str(port) + " clients: " + str(clientCount)
    host = 'localhost'
    
    buf = 1024
 
    addr = (host, port)
 
    #setup the socket
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #request reuse of socket
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    #request the kernel to bind to the address immediately
    serversocket.bind(addr)
    
    # 2 queued connections - on the off chance that two connections happen simultaneously
    serversocket.listen(2)  

    lock = threading.Lock() #stop our threads updating our result array simultaneously and breaking

    print "Setting up data for processing..."
    resultArray = []
    #Create an array to be sorted 
    arraylength = 1000000   #Length of array to be sorted 
    print 'Length of array is', arraylength 
    array = range(arraylength)  #Creates array 
    random.shuffle(array)    #Jumbles up array 
    # clientCount = 5 # temporary - needs to be counted...
    print 'Number of processors:', clientCount 

    #pieces of array to be passed to the clients
    sections = breakArray(array, clientCount)    #splits array into sections for every client 
 
    i = 0 # number of connections
    while 1:
        print "Server is listening for connections\n"
        if i == clientCount:
            print "maximum number of clients reached"
            clientsocket, clientaddr = serversocket.accept()
            thread.start_new_thread(errorReturn, (clientsocket, "MAXIMUM clients: "+str(clientCount)))
        else:
            clientsocket, clientaddr = serversocket.accept()
            thread.start_new_thread(handler, (clientsocket, sections[i], clientaddr, resultArray, len(array), lock))
            i += 1
            
    serversocket.close()

