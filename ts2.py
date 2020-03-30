
import socket
import argparse

DNS_TABLE = []
HEADER_VALUES = ["hostname", "ip", "flag"]
def set_up_dns_table():
    f = open("PROJ2-DNSTS2.txt", "r")
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
        if row["hostname"].lower() == queried_host.lower(): # case insensitive 
            return row["hostname"] + " " + row["ip"] + " " + row["flag"]
    
    return None

def lsConnect(port):
    try:
        ss=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[TS2]: Server socket created")
    except socket.error as err:
        print('{} \n'.format("socket open error ",err))

    server_binding=('',port)
    ss.bind(server_binding)
    ss.listen(1)
    host=socket.gethostname()
    print("[TS2]: Server host name is: " + host)
    localhost_ip=(socket.gethostbyname(host))
    print("[TS2]: Server IP address is  " + localhost_ip)

    print("")
    tssockid,addr=ss.accept()
    print ("[TS2]: Got a connection request from a LS at " + addr[0] + " " + str(addr[1]))
    #print("[TS2]: Sending to LS: \"Hello LS, this is TS2\"")
    #tssockid.send("Hello LS, this is TS2".encode('utf-8'))
    # request = tssockid.recv(200).decode('utf-8')
    # print("[TS2]: Response Received from LS:: " + request)
    # print("[TS2]: Sending to LS: \"Finished transmitting\"")
    # tssockid.send("Finished transmitting".encode('utf-8'))


    # TODO: uncomment after initial setup
    while 1:
        request = tssockid.recv(200).decode('utf-8')
        print("[TS2]: Message received:: " + request)
        if request == "DONE": 
            break
        response = find_ip(request.strip())
        if response != None:
            response =  "{:<200}".format(response)
            print("[TS2]: Response Sent:: " + response)
            tssockid.send(response.encode('utf-8'))


    ss.close()
    exit()

parser = argparse.ArgumentParser()

# Default arg is set to string type=int overrides
parser.add_argument("ts2ListenPort", type=int, help="input a port number")
args = parser.parse_args()
print("[TS2]: Listening on port " + str(args.ts2ListenPort) + "...")
set_up_dns_table()
lsConnect(args.ts2ListenPort)