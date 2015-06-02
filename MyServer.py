import socket
import sys, os
from thread import *
import threading
 
import MergeSort   #Imports mergesort functions 
import random 
import time 

#breaks down array into n sections where n is the number of processors 
def breakarray(array, n): 


    sectionlength = len(array)/n    #length of each section 

    result = [] 

    for i in range(n):

        if i < n - 1:
            result.append( array[ i * sectionlength : (i+1) * sectionlength ] )
        #include all remaining elements for the last section 
        else:
            result.append( array[ i * sectionlength : ] )

    return result


HOST = ''   # Symbolic name meaning all available interfaces

try:
    PORT = int(sys.argv[1])
except:
    PORT = 5003

lock = threading.Lock() #stop our threads updating our result array simultaneously and breaking

#Create an array to be sorted 
arraylength = 1000000   #Length of array to be sorted 
print 'Length of array is', arraylength 
array = range(arraylength)  #Creates array 
resultarray = []
random.shuffle(array)    #Jumbles up array 

#Specify info on processors/computers 
procno = 4  #number of processors
process = 0 #how many processes have we launched

print 'Number of processors:', procno 

sections = breakarray(array, procno)    #splits array into sections for every client 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
#Start listening on socket
s.listen(10)
print 'Socket now listening on port ' + str(PORT)
 
#Function for handling connections. This will be used to create threads
def clientthread(conn, process, addr):
    #Sending message to connected client
    #infinite loop so that function do not terminate and thread do not end.
    global resultarray
    global procno

    while True:
        
        arraystring = repr(sections[process])
        conn.sendall(arraystring)

        stringback = ''

        while True:
            dataBack = conn.recv(4096)
            stringback += dataBack
            if ']' in dataBack:
                break
        break

    print 'Merging into existing array'
    myarray = eval(stringback)
    print 'Received back from ' + addr[0] + ':' + str(addr[1]), len(myarray)
    lock.acquire()
    resultarray = MergeSort.merge(resultarray, myarray)
    lock.release()
    print "Length of resultarray: ", len(resultarray)
    print "Length of original array: ", len(array)
    conn.close()
    if len(resultarray) >= len(array):
        time_taken = time.time() - start_time
        print (repr(resultarray))[-1000:]    
        print "Array sorted in ", time_taken
        os._exit(1)


#now keep waiting for more clients.
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    print 'Starting thread for process number: ', process
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_time = time.time()
    start_new_thread(clientthread ,(conn,process,addr))
    process += 1

exit()


