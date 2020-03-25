import socket as csock
import argparse
import time

DOMAIN_NAMES = []

def read_domain_names():
    address_file = open("PROJI-HNS.txt", "r")
    arr = address_file.readlines()
    return arr

def lsConnect(lsPort, lsHostName):

    # Establishing Connection with RS
    # TODO: Server lookup addr. Check if RServer has the data or TServer does
    try:
        cs = csock.socket(csock.AF_INET, csock.SOCK_STREAM)
        print("[C]: LS Client Socket created")
    except csock.error as err:
        print('{} \n'.format("socket open error ",err))
    
    # addr = csock.gethostbyname(csock.gethostname())
    addr = lsHostName

    cs.connect((addr, lsPort))

    return cs

def tsConnect(tsHostName,tsPort ):
    # Establishing connection with TS
    # Commented out to test code between client and RS only
    # TODO: if condition here if RServer returns "TSHostName - NS"
    try:
        tcs = csock.socket(csock.AF_INET, csock.SOCK_STREAM)
        print("[C]: TS Client Socket created")
    except csock.error as err:
        print('{} \n'.format("socket open error ",err))
    addr = tsHostName
    tcs.connect((addr, tsPort))
    return tcs

parser = argparse.ArgumentParser()

# Default arg is set to string type=int overrides
parser.add_argument("lsHostName", help="input host data")
parser.add_argument("lsListenPort", type=int, help="input ls port number")
parser.add_argument("tsListenPort", type=int, help="input ts port number")
args = parser.parse_args()
print("[C]: host file name: " + args.lsHostName)
print("[C]: ls socket: " + str(args.lsListenPort))
print("[C]: ts socket: " + str(args.tsListenPort))

#connect to LS server
lsSocket = lsConnect(args.lsListenPort, args.lsHostName)

# get host name for TS by sending invalid query 
garbage_content = "garbagevalue"
garbage_content =  str("{:<200}".format(garbage_content))
lsSocket.send(garbage_content.encode('utf-8'))
LSresponse = lsSocket.recv(200).decode('utf-8')
print("[C]: Response received::  "+LSresponse)
tsHost_arr = LSresponse.split("-")
tsHostName = tsHost_arr[0].strip()
if tsHostName == "localhost":
    tsHostName = args.lsHostName

# connect to TS server
tsSocket = tsConnect(tsHostName, args.tsListenPort)

address_file = open("PROJI-HNS.txt", "r")
output_file = open("RESOLVED.txt", "w")


fileInfo = ""
for line in address_file:
    line =  str("{:<200}".format(line))
    print("[C]: Response sent::  "+line)
    lsSocket.send(line.encode('utf-8'))
    LSresponse = lsSocket.recv(200).decode('utf-8')
    print("[C]: Response recieved::  "+LSresponse)
    if "NS" in LSresponse:
        print("[C]: Sending to TS ...  ")
        print("[C]: Response sent to TS::  "+line)
        tsSocket.send(line.encode('utf-8'))
        TSresponse = tsSocket.recv(200).decode('utf-8')
        print("[C]: Response received from TS::  "+TSresponse)
        fileInfo = fileInfo + TSresponse.strip() + "\n" 
        # output_file.write(TSresponse.strip()+"\n")
    else:
        fileInfo = fileInfo + LSresponse.strip() + "\n"
        # output_file.write(LSresponse.strip()+"\n")
fileInfo = fileInfo[:-1]
output_file.write(fileInfo)

lsSocket.send("DONE".encode('utf-8'))
lsSocket.close()
tsSocket.send("DONE".encode('utf-8'))
tsSocket.close()
exit()