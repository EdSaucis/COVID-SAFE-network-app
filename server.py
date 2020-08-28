# Adapted from the following multithreaded server
# http://net-informations.com/python/net/thread.htm

import socket
import threading
import sys
import json
import time

from ServerFunctions import authenticate, newTempID, getUserDetails

def lockout_timer(username):
    global locked_out_users
    global block_duration

    # wait the set time
    time.sleep(block_duration)

    #remove the user from the list
    locked_out_users.remove(username)
    return

def thread_server(connection_client, address_client):
    global credentials_semaphore
    global tempID_semaphore
    global locked_out_users

    # connection successful, send back success
    result = "connection success"
    connection_client.send(result.encode('utf-8'))
    # handle login attempts
    count = 0
    while True:
        # wait for login details to be sent
        message = connection_client.recv(1024).decode('utf-8')
        
        # extract username and password
        message_split = message.split(" ")
        username = message_split[0]
        password = message_split[1]
        
        if username in locked_out_users:
            block_out_message = "Your account has been blocked due to multiple login failures. Please try again later\n"
            connection_client.send(block_out_message.encode('utf-8'))
            continue

        # authenticate username and password
        credentials_semaphore.acquire()
        result = authenticate(username, password)
        credentials_semaphore.release()
        
        
        
        # if incorrect 3 times send back Lockout and the block_duration
        if count == 3:
            result = "Lockout " + str(block_duration)
            connection_client.send(result.encode('utf-8'))
            locked_out_users.append(username)
            lockout_thread = threading.Thread(target=lockout_timer, args=(username,))
            lockout_thread.start()
            count = 0
            continue
            
        # send back login result
        connection_client.send(result.encode('utf-8'))

        # if authentication not successful
        if result != "login_success\n":
            error_split = result.split(" ")
            # if password incorrect, increment count
            if error_split[1] == "incorrect":
                count += 1
        else:
            print("Logging in ", username, "...")
            break

    # if success start loop to await console commands
    while True:
        # receive a command from the client
        print("Waiting for command...")
        message = connection_client.recv(1024).decode('utf-8')
        
        # start upload of client contact log
        if message == "upload":
            
            # send start_upload indicator
            result = "start_upload"
            connection_client.send(result.encode('utf-8'))
            
            # receive each line of the contact log and print its user
            print("users in contact with ", username, ":")
            while True:
                line = connection_client.recv(1024).decode('utf-8')
                
                # if contact log finished, exit loop 
                if line == "end": 
                    print("upload success")
                    break

                # print the username of the tempID
                tempID_semaphore.acquire()
                print(getUserDetails(line))
                tempID_semaphore.release()

                # send next
                next_message = "next"
                connection_client.send(next_message.encode('utf-8'))

        # download a new tempID and send to user
        elif message == "download":
            print("Downloading tempID for ", username, "...")

            # get a new tempID
            tempID_semaphore.acquire()
            result = newTempID(username)
            tempID_semaphore.release()

            # send the tempID to the client
            connection_client.send(result.encode('utf-8'))

        # logout the user
        elif message == "logout":
            print("logging out ", username)

            # exit the thread when user logs out
            return


########MAIN#####################################

credentials_semaphore = threading.Semaphore()
tempID_semaphore = threading.Semaphore()

locked_out_users = []

hostname = socket.gethostname()
server_host = socket.gethostbyname(hostname)
print("Server set up on:",server_host)

# for local host server uncomment the following line and remove the above two lines
# server_host = 'localhost'

# need to set up check for valid port
server_port = int(sys.argv[1])
# need to set up check for valid block_duration
block_duration = int(sys.argv[2])
# create a socket
# AF_INET - address family, server_hostv4
# SOCK_STREAM - TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# REUSEADDR set to 1 on socket to ensure reuse is set up before being bound
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# bin socket to host and port
server_socket.bind((server_host, server_port))
# start listening for connections
server_socket.listen(5)




while True:
    
    # run new thread for every connection
    try:
        connection_client, address_client = server_socket.accept()
        # create new thread
        new_thread = threading.Thread(target=thread_server, args=(connection_client, address_client))
        # run new thread
        new_thread.start()
        print("connection success")
    
    # close program when keyboard interrupt
    except KeyboardInterrupt:
        break








    
    

