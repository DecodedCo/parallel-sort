# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2015, Decoded Ltd dev@decoded.com

from ClientThread import clientThread 
import MergeSort   #Imports mergesort functions 
import json
import time

arrays_old = [] # need two arrays to copy changes to 
arrays_new = [] # and then reset the original

def handler(clientsocket, section, clientaddr, resultArray, length, lock, clientCount):
    print "Accepted connection from: ", clientaddr
    global arrays_old, arrays_new, start_time

    while 1:
        data = clientsocket.recv(1024)
        if not data:
            break
        if data == "request":
            start_time = time.time() #reset the timer
            msg = "REQUEST"
            clientsocket.send(msg)
            #passing section directly from handler
            #recursively keep sorting...
            arrays_old.append(clientThread(clientsocket, section, clientaddr, resultArray, length))
            '''
            when the program starts
            if splits the values into groups of 5.
            These get sorted and pairs get merged together
            this then gets merged with the next one
            * What should happen is the pairs should get merged on threads

            '''
            if(len(arrays_old) == clientCount):
                processData()
            else:
                print "waiting..."
        elif data == "sort":
            
            processData()

        elif data == "finish":
            msg = "CLOSE"
            clientsocket.send(msg)
            clientsocket.close()        
        else:
            print data
            msg = "Client requested: %s, unknown command." % data
            clientsocket.send(msg)
    clientsocket.close()

def processData():
    global arrays_old, arrays_new
    running = True
    index = 0
    while running:
        #merge neighbouring arrays
        print "index: " + str(index)
        resultArray = MergeSort.merge(arrays_old[index], arrays_old[index+1])

        arrays_old.pop(0) #remove i
        arrays_old.pop(0) #remove i + 1
       
        if len(arrays_old) == 0 and all(b >= a for a, b in zip(resultArray, resultArray[1:])):
            print "sorted!!"
            f = open("sorted.txt","w")
            json.dump(resultArray,f)
            f.close()
            time_taken = time.time() - start_time
            print "Sorting completed in ", time_taken, " seconds"
            running = False
        else:
            print "in else..."
            arrays_new.append(resultArray)
            for a in arrays_old:
                arrays_new.append(a)
            arrays_old = [] #resetting arrays_old
            arrays_old = arrays_new[:] #clone arrays_new into arrays_old
            arrays_new = [] #clearing arrays_new
 
