# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2015, Decoded Ltd dev@decoded.com

#Function for handling connections. 
#This will be used to create threads
import MergeSort   #Imports mergesort functions 

def clientThread(conn, section, addr, resultArray, length):
    #Sending message to connected client
    #infinite loop so that function do not terminate and thread do not end.
    global procno

    while True:
        
        print "sending..."
        arraystring = repr(section)
        conn.sendall(arraystring)
        print "data sent!"
        stringback = ''

        while True:
            dataBack = conn.recv(4096)
            stringback += dataBack
            if ']' in dataBack:
                break
        break

    print 'Merging into existing array'
    threadArray = eval(stringback)
    print 'Received back from ' + addr[0] + ':' + str(addr[1]), len(threadArray)
    return threadArray
