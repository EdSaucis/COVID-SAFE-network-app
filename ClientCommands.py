import sys
from datetime import datetime

# Take in the login details from the console
def loginDetails():
    # take in username from terminal
    sys.stdout.write("Username: ")
    username = str(input())

    sys.stdout.write("Password: ")
    password = input()

    result = username + " " + password
    return result

#tempID comes in the form:
# tempID start_date start_time end_date end_time
def check_tempID(tempID):
    # split tempID to find just the start datetime and end datetime
    split_tempID = tempID.split(' ')
    start_time = str(split_tempID[2] + ' ' + split_tempID[3])
    end_time = str(split_tempID[4] + ' ' + split_tempID[5])

    # change string into datetime object to compare with current datetime
    start_datetime = datetime.strptime(start_time, '%d/%m/%Y %H:%M:%S')
    end_datetime = datetime.strptime(end_time, '%d/%m/%Y %H:%M:%S')

    # current datetime
    now = datetime.now()
    print("Current time is:\n", now.strftime("%d/%m/%Y %H:%M:%S"))

    # if current time is between the start time and end time
    # return True
    if now >= start_datetime and now <= end_datetime:
        return True

    return False


def delete_line(tempID):
    fname = 'z5015224_contactlog.txt'
    contact_log = open(fname)
    output = []
    for line in contact_log:
        if not tempID in line:
            output.append(line)

    contact_log.close()
    contact_log = open(fname, 'w')
    contact_log.writelines(output)
    contact_log.close()
    return