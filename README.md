# parallel-sort
Parallel Sort Processing Example in Python (for Raspberry Pi eventually)

Edit the procno variable in MyServer.py to specify the number of processors you want to use.

Run with python MyServer.py PORT (or leave PORT blank to default to 5003

Then on client machines (or locally) run python MyClient.py PORT SERVER (or leave both blank to default to 5003 / 127.0.0.1, if specifying an address you must specify a port).

Repeat loading clients until enough have been created to meet the number of processors set in MyServer.py
