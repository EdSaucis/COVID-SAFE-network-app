import random
import sys
import datetime
from datetime import datetime, timedelta

# attempt login of username with password
def authenticate(username, password):
    
    user_found = findUser(username)
    password_found = checkPassword(username, password)
    
    # if username and password match return success
    if user_found:
        if password_found:
            return "login_success\n"
        # if username matches and password doesn't return "error: incorrect password"
        else:
            return "error: incorrect password\n"
    # if username does not match, return "error: user not found"
    else:
        return "error: user not found\n"


# generate a newTempID and return it
def newTempID(username):
    # generate a random 20 digit integer
    newID = random.randrange(0, 99999999999999999999, 2)
    
    ## TODO CHECK: find date and time right now
    current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    ## TODO: find date and time in 15 minutes
    expiry_datetime = (datetime.now() + timedelta(minutes=15)).strftime("%d/%m/%Y %H:%M:%S")

    ## TODO CHECK: Write to list
    newline = username + " " + str(newID) + " " + str(current_datetime) + " " + str(expiry_datetime)
    
    with open('tempIDs.txt', 'a') as append_file:
        append_file.write(newline)
        append_file.write("\n")
    return newline

# return username for given temp_ID
def getUserDetails(client_temp_ID):
    read_tempIDs = open('tempIDs.txt').readlines()
    for line in read_tempIDs:
        # Check if tempIDs and dates match
        split_line = line.split(" ", 1)
        current_tempID = split_line[1]
        if checkTempID(client_temp_ID, current_tempID):
            # send back user details
            username = split_line[0]
            return username
    # if no details found
    return "Untracked TempID"


# check credentials for username
# return true if found, false if not
def findUser(username):
    read_credentials = open('credentials.txt').readlines()
    for line in read_credentials:
        ## extract username
        user = line.split(" ")
        # if the user exists in the credentials file
        if user[0] == username:
            return True
    
    return False

# check credentials if username and password match
def checkPassword(username, password):
    read_credentials = open('credentials.txt').readlines()
    for line in read_credentials:
        ## TODO extract username
        pw = line.replace("\n","").split(" ")
        current_user = pw[0]
        current_password = pw[1]
        # if the user exists in the credentials file
        if current_user == username and current_password == password:
            return True
    
    return False
            
# check if two tempIDs match
def checkTempID(clientTempID, currentTempID):
    if clientTempID == currentTempID:
        return True
    else:
        return False