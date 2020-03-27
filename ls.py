import socket
import argparse
import time
DNS_TABLE = []
HEADER_VALUES = ["hostname", "ip", "flag"]
def set_up_dns_table():
    f = open("PROJI-DNSRS.txt", "r")
    for line in f:
        line = line.strip("\n") # remove extra new lines
        line_info = line.split(" ") # split line by spaces

        # create dictionary of values and add to array 
        combined_info = zip(HEADER_VALUES, line_info) 
        DNS_TABLE.append(dict(combined_info))

    f.close()

def find_ip(queried_host):
    # check if the IP is in the table 
    for row in DNS_TABLE:
        if row["hostname"].lower() == queried_host.lower():  # case insensitive
            return row["hostname"] + " " + row["ip"] + " " + row["flag"]+ "\n"
    
    # if not in the table find the NS host name and return 
    for row in DNS_TABLE:
        if row["flag"] == "NS":
            return row["hostname"] +" - "+ row["flag"]+ "\n"


# helper function. returns socket single connection with ts
def tsConnect(tsHostName,tsPort):
    # Establishing connection with TS
    # Commented out to test code between client and RS only
    # TODO: if condition here if RServer returns "TSHostName - NS"
    try:
        ts = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[LS]: TS Client Socket created")
    except socket.error as err:
        print('{} \n'.format("socket open error ",err))
    tsaddr = tsHostName
    ts.connect((tsaddr, tsPort))
    return ts

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

    print("\n")
    csockid,addr=ssls.accept()
    print ("[LS]: Got a connection request from a client at " + addr[0] + " " + str(addr[1]))
    request = csockid.recv(200).decode('utf-8')
    print("[LS]: Response Received from Client:: " + request)
    print("[LS]: Sending to Client: \"Hello Client, this is LS\"")
    csockid.send("Hello Client, this is LS")

    print("\n")

    # LS then forwards the query to _both_ TS1 and TS2. However, at most one of TS1 and TS2 contain the IP address for this hostname.
    # Only when a TS server contains a mapping will it respond to LS; otherwise, that TS sends nothing back.
    ts1Socket = tsConnect(ts1Hostname, ts1ListenPort)
    ts1Request = ts1Socket.recv(200).decode('utf-8')
    print("[LS]: Response Received from TS1:: " + request)
    print("[LS]: Sending to TS1: \"Hello TS1, this is LS\"")
    ts1Socket.send("Hello TS1, this is LS")
    ts1Request = ts1Socket.recv(200).decode('utf-8')
    print("[LS]: Response Received from TS1:: " + request)

    print("\n")

    ts2Socket = tsConnect(ts2Hostname, ts2ListenPort)
    ts2Request = ts2Socket.recv(200).decode('utf-8')
    print("[LS]: Response Received from TS2:: " + request)
    print("[LS]: Sending to TS2: \"Hello TS2, this is LS\"")
    ts2Socket.send("Hello TS2, this is LS")
    ts2Request = ts2Socket.recv(200).decode('utf-8')
    print("[LS]: Response Received from TS2:: " + request)

    #if the LS does not receive a response from either TS within a time interval of 5 seconds (OK to wait slightly longer),
    #the LS must sendthe client the message: Hostname -Error:HOST NOT FOUND where the Hostname is the client-requested host name.




    # TODO: uncomment after initial setup might not need it in ls. only in ts
    # while 1:
    #     request = csockid.recv(200).decode('utf-8')
    #     print("[LS]: Message received:: " + request)
    #     if request == "DONE": 
    #         break
    #     response = find_ip(request.strip())
    #     response =  "{:<200}".format(response)
    #     print("[LS]: Response Sent:: " + response)
    #     csockid.send(response.encode('utf-8'))

    print("\n")
    print("[LS]: Sending to Client: \"Finished transmitting\"")
    csockid.send("Finished Transmitting".decode('utf-8'))

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