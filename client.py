import socket as csock
import argparse

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






parser = argparse.ArgumentParser()

# IMPORTANT: Commented out all TS server connections

# Default arg is set to string type=int overrides
parser.add_argument("lsHostName", help="input host data")
parser.add_argument("lsListenPort", type=int, help="input ls port number")

args = parser.parse_args()
print("[C]: host file name: " + args.lsHostName)
print("[C]: ls socket: " + str(args.lsListenPort))


print("\n")
#connect to LS server
lsSocket = lsConnect(args.lsListenPort, args.lsHostName)

# get host name for TS by sending invalid query 
# garbage_content = "garbagevalue"
# garbage_content =  str("{:<200}".format(garbage_content))
# lsSocket.send(garbage_content.encode('utf-8'))

print("[C]: Sending to LS: \"Hello LS, this is Client\"")
lsSocket.send("Hello LS, this is Client".encode('utf-8'))
LSresponse = lsSocket.recv(200).decode('utf-8')
print("[C]: Response received from LS::  " + LSresponse)



# fileInfo = ""
# for line in address_file:
#     line =  str("{:<200}".format(line))
#     print("[C]: Response sent::  "+line)
#     lsSocket.send(line.encode('utf-8'))
#     LSresponse = lsSocket.recv(200).decode('utf-8')
#     print("[C]: Response recieved::  "+LSresponse)
#     if "NS" in LSresponse:
#         print("[C]: Sending to TS ...  ")
#         print("[C]: Response sent to TS::  "+line)
#         tsSocket.send(line.encode('utf-8'))
#         TSresponse = tsSocket.recv(200).decode('utf-8')
#         print("[C]: Response received from TS::  "+TSresponse)
#         fileInfo = fileInfo + TSresponse.strip() + "\n" 
#         output_file.write(TSresponse.strip()+"\n")
#     else:
#         fileInfo = fileInfo + LSresponse.strip() + "\n"
#         output_file.write(LSresponse.strip()+"\n")
# fileInfo = fileInfo[:-1]
# output_file.write(fileInfo)

LSresponse = lsSocket.recv(200).decode('utf-8')
print("[C]: Response received:: " + LSresponse)
lsSocket.close()

exit()