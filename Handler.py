from ClientThread import clientThread 
import MergeSort   #Imports mergesort functions 
import json
arrays_old = [] # need two arrays to copy changes to 
arrays_new = [] # and then reset the original

def handler(clientsocket, section, clientaddr, resultArray, length, lock):
    print "Accepted connection from: ", clientaddr
    global arrays_old, arrays_new

    while 1:
        data = clientsocket.recv(1024)
        if not data:
            break
        if data == "request":
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
            
            print "waiting..."
        elif data == "sort":
            
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
                    running = False
                else:
                    print "in else..."
                    arrays_new.append(resultArray)
                    for a in arrays_old:
                        arrays_new.append(a)
                    arrays_old = [] #resetting arrays_old
                    arrays_old = arrays_new[:] #clone arrays_new into arrays_old
                    arrays_new = [] #clearing arrays_new

        elif data == "finish":
            msg = "CLOSE"
            clientsocket.send(msg)
            clientsocket.close()        
        else:
            print data
            msg = "Client requested: %s, unknown command." % data
            clientsocket.send(msg)
    clientsocket.close()
 