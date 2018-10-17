import sys
import socket as mysoc

def RSserver():

    fDNSRSnames = open("PROJ2-DNSRS.txt", "r")
    fDNSRSList = fDNSRSnames.readlines()
    inputEntries = []
    for entry in fDNSRSList:
        inputEntries.append(entry.strip("\n"))

    try:
        rs_socket = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
    except mysoc.error as err:
        print('{}\n'.format("RS socket open error", err))

    rs_server_binding=('', 51237)
    rs_socket.bind(rs_server_binding)
    rs_socket.listen(1)
    hostname = mysoc.gethostname()
    rs_host_ip = (mysoc.gethostbyname(hostname))
    csockid,addr=rs_socket.accept()

    while True:
        client_data = csockid.recv(100)
        foundEntry = False
        if not client_data:
            break
        client_data = client_data.strip("\n")
        client_data = client_data.strip("\r")
        print("[RS:] Recieved: %s" % client_data)

        for entry in inputEntries:
            splitEntry = entry.split(" ")
            entryHostname = splitEntry[0].strip("\n")
            entryHostname = splitEntry[0].strip("\r")
            entryHostname = splitEntry[0].strip()
            flag = splitEntry[-1]
            flag = flag.strip()

            if entryHostname == client_data:
                foundEntry = True
                print("[RS:] Sending: %s" % entry)
                csockid.send(entry)
                break
            if flag == 'NS':
                if foundEntry == False:
                    # TODO: Forward to appropriate TLDS server (com or edu)
                    # TODO: Wait for data from TLDS server
                    # TODO: Send data back to client
                    pass


    rs_socket.close()
    exit()

RSserver()
