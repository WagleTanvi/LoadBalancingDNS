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
    
def clientConnect(port):
    try:
        ss=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[LS]: Server socket created")
    except socket.error as err:
        print('{} \n'.format("socket open error ",err))

    server_binding=('',port)
    ss.bind(server_binding)
    ss.listen(1)
    host=socket.gethostname()
    print("[LS]: Server host name is: " + host)
    localhost_ip=(socket.gethostbyname(host))
    print("[LS]: Server IP address is  " + localhost_ip)
    csockid,addr=ss.accept()
    print ("[LS]: Got a connection request from a client at " + addr[0] + " " + str(addr[1]))
    csockid.send("hello from ls")
    request = csockid.recv(200).decode('utf-8');
    print("[LS]: Response from client: " + request)
    request = csockid.recv(200).decode('utf-8');
    print("[LS]: Response from client: " + request)

    # TODO: uncomment after initial setup
    # while 1:
    #     request = csockid.recv(200).decode('utf-8')
    #     print("[LS]: Message received:: " + request)
    #     if request == "DONE": 
    #         break
    #     response = find_ip(request.strip())
    #     response =  "{:<200}".format(response)
    #     print("[LS]: Response Sent:: " + response)
    #     csockid.send(response.encode('utf-8'))

    ss.close()
    exit()

parser = argparse.ArgumentParser()

# Default arg is set to string type=int overrides
parser.add_argument("lsListenPort", type=int, help="input a port number")
args = parser.parse_args()
print("[LS]: Listening on port " + str(args.lsListenPort) + "...")
# set_up_dns_table()
clientConnect(args.lsListenPort)