# parallel-sort
Parallel Sort Processing Example in Python (for Raspberry Pi eventually)

* On the server, call `python tcpServer.py [port] [number of clients] [array size]`
	* port will default to `55555`
	* number of clients will default to 2
	* The array size will default to 100000
* On the client connect to the server with `python tcpClient.py [port] [host]`

### TODO:

* The final sort could be threaded back to the clients.