import socket as csock
import argparse

def lsConnect(lsHostName, lsPort):
    try:
        cs = csock.socket(csock.AF_INET, csock.SOCK_STREAM)
        print("[C]: LS Client Socket created")
    except csock.error as err:
        print('{} \n'.format("socket open error ",err))

    cs.connect((lsHostName, lsPort))
    return cs

def sendQuery(lsSocket):
    hns_file = open("PROJ2-HNS.txt")

    print("[C]: Beginning transmission to LS.")
    for line in hns_file:
        line = line.rstrip()
        if line == "":
            continue
        print("SENDING: " + line)
        lsSocket.send("{:<200}".format(line))
    lsSocket.send("DONE")
    print("DONE")
    hns_file.close()



# Default arg is set to string type=int overrides
parser = argparse.ArgumentParser()
parser.add_argument("lsHostName", help="input host data")
parser.add_argument("lsListenPort", type=int, help="input ls port number")
args = parser.parse_args()

print("[C]: host file name: " + args.lsHostName)
print("[C]: ls socket: " + str(args.lsListenPort))

print("")

lsSocket = lsConnect(args.lsHostName, args.lsListenPort)
sendQuery(lsSocket)

print("")

LSresponse = lsSocket.recv(200).decode('utf-8')
print("[C]: Response received:: " + LSresponse)
lsSocket.close()
exit()