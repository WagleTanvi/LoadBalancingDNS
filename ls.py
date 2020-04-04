import socket
import argparse
import time
import select 


# helper function. returns socket single connection with ts
def tsConnect(tsHostName,tsPort):
    try:
        ts = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[LS]: TS Client Socket created")
    except socket.error as err:
        print('{} \n'.format("socket open error ",err))
    ts.connect((tsHostName, tsPort))
    return ts

def sendTS(hostname, ts1Socket, ts2Socket, ts1Hostname, ts2Hostname):
    ts1Socket.send("{:<200}".format(hostname))
    ts2Socket.send("{:<200}".format(hostname))
    while 1:
        try:
            inputready,outputready,exceptready = select.select([ts1Socket, ts2Socket], [], [],5)
        except select.error, e:
            break
        except socket.error, e:
            break
        if not inputready:
            print("Timed out")
            return hostname + " - Error:HOST NOT FOUND"
        for s in inputready:
            data = s.recv(1024)
            if data:
                data = data.strip()
                # if s == ts1Socket:
                #     data+= " "+ts1Hostname
                #     print(data)
                # else: 
                #     data+= " "+ts2Hostname
                #     print(data)
                return data

# TODO: ts parameters must be added
def clientConnect(lsListenPort, ts1Hostname, ts1ListenPort, ts2Hostname, ts2ListenPort):
    try:
        ssls=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[LS]: Server socket created")
    except socket.error as err:
        print('{} \n'.format("socket open error ",err))

    server_binding=('',lsListenPort)
    ssls.bind(server_binding)
    ssls.listen(1)
    host=socket.gethostname()
    print("[LS]: Server host name is: " + host)
    localhost_ip=(socket.gethostbyname(host))
    print("[LS]: Server IP address is  " + localhost_ip)

    print("")

    ts1Socket = tsConnect(ts1Hostname, ts1ListenPort)
    ts2Socket = tsConnect(ts2Hostname, ts2ListenPort)
    ts1Socket.setblocking(1)
    ts2Socket.setblocking(1)

    csockid,addr=ssls.accept()
    print ("[LS]: Got a connection request from a client at " + addr[0] + " " + str(addr[1]))

    print("[LS]: Receiving queries from Client...")

    # TODO: Send hostnames to TS1 and TS2
    # LS then forwards the query to _both_ TS1 and TS2. However, at most one of TS1 and TS2 contain the IP address for this hostname.
    # Only when a TS server contains a mapping will it respond to LS; otherwise, that TS sends nothing back.

    #if the LS does not receive a response from either TS within a time interval of 5 seconds (OK to wait slightly longer),
    #the LS must sendthe client the message: Hostname -Error:HOST NOT FOUND where the Hostname is the client-requested host name.
    
    while(1):
        hostname = csockid.recv(200).strip()
        if(hostname == "DONE"):
            break
        print("[LS]: RECEIVED: " + hostname)
        response = sendTS(hostname,ts1Socket, ts2Socket, ts1Hostname, ts2Hostname)
        response =  "{:<200}".format(response)
        print("[LS]: SENT: " + response)
        csockid.send(response.encode('utf-8'))

    ts2Socket.send("DONE")
    ts1Socket.send("DONE")
    print("")

    ts1Socket.close()
    ts2Socket.close()

    ssls.close()
    exit()


parser = argparse.ArgumentParser()

# Default arg is set to string type=int overrides
parser.add_argument("lsListenPort", type=int, help="input a port number")
parser.add_argument("ts1Hostname", help="input ts1Hostname")
parser.add_argument("ts1ListenPort", type=int, help="input ts1Hostname port number")
parser.add_argument("ts2Hostname", help="input ts2Hostname")
parser.add_argument("ts2ListenPort", type=int, help="input ts2Hostname port number")
args = parser.parse_args()
print("[LS]: Listening on port " + str(args.lsListenPort) + "...")
print("[LS]: ts1Hostname: " + args.ts1Hostname)
print("[LS]: ts1ListenPort: " + str(args.ts1ListenPort))
print("[LS]: ts2Hostname: " + args.ts2Hostname)
print("[LS]: ts2ListenPort: " + str(args.ts2ListenPort))
# set_up_dns_table()
clientConnect(args.lsListenPort, args.ts1Hostname, args.ts1ListenPort, args.ts2Hostname, args.ts2ListenPort)