# COMP3331

COVIDSafe app

Running the program
1. Start up the server from new terminal:
python3 server.py <server_port > <block_duration>
- server_port: the port number of the server being set up
- block_duration: the amount of time that a user will be locked out of the program
after failing login more than three times.

2. Start up a client (can be done multiple at the same time):
python3 client.py <server_ip> <server_port> <client_udp_port>
- server_ip: the ip address of the server being connected to
- server_port: the port number of the server being connected to
- client_udp_port: the port number of the UDP being set up

3. Login the user. A list of usernames and passwords are stored in credentials.txt. If a username and password are valid, the program will be entered.

4. Run client commands
a. “Download_tempID”: generates and downloads a new tempID to the client,
adding it to the list of tempIDs.txt. (no tempID is set when logging in, so this
needs to be run first for a successful beacon to be sent)
b. “Upload_contact_log”: sends the current contact log to the server where it
prints all the phone numbers of contacts
c. “Beacon <ip_address> <udp_port>”: sends a beacon to a client through a
UDP with IP address and port number.
d. “logout”: logs out the client. Client must be logged out before server can shut
with Keyboard Interrupt
