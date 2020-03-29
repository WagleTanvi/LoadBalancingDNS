import socket as csock
import argparse

DOMAIN_NAMES = []

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

def sendQuery(lsSocket):
    hns_file = open("PROJ2-HNS.txt")

    print("[C]: Beginning transmission to LS. Sending queries...")
    allLines = ""
    for line in hns_file:
        line = line.rstrip()
        print(line)
        allLines += line + " "
    lsSocket.send(allLines)
    hns_file.close()



# Default arg is set to string type=int overrides
parser = argparse.ArgumentParser()
parser.add_argument("lsHostName", help="input host data")
parser.add_argument("lsListenPort", type=int, help="input ls port number")
args = parser.parse_args()

print("[C]: host file name: " + args.lsHostName)
print("[C]: ls socket: " + str(args.lsListenPort))

print("")
#connect to LS server
lsSocket = lsConnect(args.lsListenPort, args.lsHostName)
print("[C]: Sending to LS: \"Hello LS, this is Client\"")
lsSocket.send("Hello LS, this is Client".encode('utf-8'))
LSresponse = lsSocket.recv(200).decode('utf-8')
print("[C]: Response received from LS::  " + LSresponse)

print("")
sendQuery(lsSocket)



LSresponse = lsSocket.recv(200).decode('utf-8')
print("[C]: Response received:: " + LSresponse)
lsSocket.close()



exit()