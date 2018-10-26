import sys
import socket as mysoc

def COMserver():

    fDNSCOMnames = open("PROJ2-DNSCOM.txt", "r")
    fDNSCOMList = fDNSCOMnames.readlines()
    inputEntries = []
    for entry in fDNSCOMList:
        inputEntries.append(entry.strip("\n"))

    try:
        com_socket=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
    except mysoc.error as err:
        print('{}\n'.format("COM socket open error",err))

    com_server_binding=('', 51238)
    com_socket.bind(com_server_binding)
    com_socket.listen(1)
    hostname = mysoc.gethostname()
    com_host_ip = (mysoc.gethostbyname(hostname))
    print("%s" % hostname)
    csockid,addr=com_socket.accept()

    while True:
        rs_data = csockid.recv(100)
        foundEntry = False
        if not rs_data:
            break
        rs_data = rs_data.strip("\n")
        rs_data = rs_data.strip("\r")
        print("[COM:] Recieved: %s" % rs_data)

        for entry in inputEntries:
            splitEntry = entry.split(" ")
            entryHostname = splitEntry[0].strip("\n")
            entryHostname = splitEntry[0].strip("\r")
            entryHostname = splitEntry[0].strip()
            flag = splitEntry[-1]
            flag = flag.strip()

            if entryHostname == rs_data:
                foundEntry = True
                print("[COM:] Sending: %s" % entry)
                csockid.send(entry)
            elif flag == 'NS':
                if foundEntry == False:
                    print("[COM:] Sending NS")
                    csockid.send(entry)

    print("[COM:] SOCKET CLOSED")
    com_socket.close()
    exit()

COMserver()
