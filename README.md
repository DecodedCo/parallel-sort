# parallel-sort
Parallel Sort Processing Example in Python (for Raspberry Pi eventually)

* On the server, call `python tcpServer.py [port] [number of clients] [array size]`
	* port will default to `55555`
	* number of clients will default to `2`
	* The array size will default to `100000`
* On the client connect to the server with `python tcpClient.py [port] [host]`

#### When running:

* Each client needs to request data:

```
>>request
```

* When each client has finished their processing, *one* of the clients needs to call `sort`:

```
>>sort
```
The server will then start sorting the data it has. See TODO for more details on this

### TODO:

* The final sort could be threaded back to the clients.
* Sort should only be possible when all of the data has been returned. Currently this could potentially cause a race condition