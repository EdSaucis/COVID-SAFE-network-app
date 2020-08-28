import socket
import threading
import sys
import time

#rom socket import socket, AF_INET, SOCK_STREAM
from ClientCommands import loginDetails, check_tempID, delete_line

def remove_tempID(tempID):
    # wait three minutes
    time.sleep(180)
    contactlog_semaphore.acquire()
    # remove the tempID from the contact log
    delete_line(tempID)

    contactlog_semaphore.release()
    return

def beacon_receive():
    global receiveBeaconSocket
    global t_lock
    global contactlog_semaphore

    while True:
        recv_tempID, receiveAddress = receiveBeaconSocket.recvfrom(1024)
        print("Receiving Beacon:")
        if recv_tempID.decode('utf-8') == "":
            print("No tempID received\n\nEnter command:")
            continue

        print(recv_tempID.decode('utf-8'))
        #check if tempID is valid
        if check_tempID(recv_tempID.decode('utf-8')):
            print("The beacon is valid.\n\nEnter command:")
            split_tempID = recv_tempID.decode('utf-8').split(' ', 1)
            append_tempID = split_tempID[1]
            
            #add tempID to the contact log
            contactlog_semaphore.acquire()
            with open('z5015224_contactlog.txt', 'a') as append_file:
                append_file.write(append_tempID)
                append_file.write("\n")
            contactlog_semaphore.release()
            #start 3 minute timer
            remove_thread = threading.Thread(target=remove_tempID, args=(append_tempID,))
            remove_thread.start()
        else:
            print("The beacon is invalid.\n\nEnter command")

    return



contactlog_semaphore = threading.Semaphore()

server_IP = sys.argv[1]
server_port = int(sys.argv[2])
client_udp_port = int(sys.argv[3])

t_lock=threading.Condition()
#we will use two sockets, one for sending and one for receiving
receiveBeaconSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sendBeaconSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiveBeaconSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
receiveBeaconSocket.bind((server_IP, client_udp_port))

recv_thread=threading.Thread(target=beacon_receive)
recv_thread.daemon=True
recv_thread.start()

tempID = ""
command_mode = True

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_IP, server_port))

message = client_socket.recv(1024).decode()

while True:
    command_mode = True
    if message != "connection success":
        # end program
        command_mode = False
        break
    
    # get login from terminal
    login = loginDetails()

    # send login details
    client_socket.send(login.encode('utf-8'))
    login_success = client_socket.recv(1024).decode('utf-8')
    login_split = login_success.split(" ")

    if login_success == "login_success\n":
        print(login_success)
        break

    elif login_split[0] == "Lockout":
        lockout_time = login_split[1]
        print("Lockout for " + lockout_time + "\n")

    else:
        print(login_success)

while command_mode:
    
    print("Enter command: ")
    data = str(input())
    
    # download the tempID
    if data == "Download_tempID":
        
        # send request for tempID
        message = "download"
        client_socket.send(message.encode('utf-8'))
        
        # receive tempID
        result = client_socket.recv(1024).decode('utf-8')
        
        # save tempID locally
        tempID = str(result)

        # write tempID on terminal to show success
        print("TempID is: ",tempID)

    # upload the contact log
    elif data == "Upload_contact_log":
        # send upload to request upload
        message = "upload"
        client_socket.send(message.encode('utf-8'))

        # receive start_upload signal
        start_upload_message = client_socket.recv(1024).decode('utf-8')

        read_credentials = open("z5015224_contactlog.txt").readlines()
        for line in read_credentials:
            client_socket.send(line.encode('utf-8'))
            next_message = client_socket.recv(1024).decode('utf-8')

        print("Upload success")
        
        end_message = "end"
        client_socket.send(end_message.encode('utf-8'))

    # logout the client
    elif data == "logout":

        message = "logout"

        # remove tempID from contact log
        contactlog_semaphore.acquire()
        delete_line(tempID)
        contactlog_semaphore.release()

        # send logout request to server
        client_socket.send(message.encode('utf-8'))
        break
    
    else:
        data_split = data.split(' ')
        if data_split[0] == "Beacon" and len(data_split) == 3:
            try:
                dest_IP = data_split[1]
                dest_port = int(data_split[2])
                send_tuple = (dest_IP, dest_port)
                sendBeaconSocket.sendto(tempID.encode('utf-8'), send_tuple)
                print("Sending beacon\n")
                
            except:
                print("Incorrect addresses")

            continue
            
        # print error message to console
        message = "Unknown command: " + data
        print(message)
        client_socket.send(message.encode('utf-8'))

client_socket.close()

