import socket as mysoc
import sys

#TODO: Fix Com and Edu server not recv anything after first
def getHostnameFromEntry(entry):
    splitEntry = entry.split(" ")
    entryHostname = splitEntry[0].strip("\n").strip("\r").strip()
    return entryHostname


def getFlagFromEntry(entry):
    splitEntry = entry.split(" ")
    flag = splitEntry[-1]
    flag = flag.strip()
    return flag

def getComOrEdu(entry):
    entryHostname = getHostnameFromEntry(entry)
    return entryHostname[len(entryHostname)-3:].strip()


def getIpFromDNS(entry):
    splitEntry = entry.split(" ")
    serverIP = splitEntry[1].strip("\n").strip("\r").strip()
    return serverIP


def RSserver():
    DNS_Table_Name = sys.argv[3]
    fDNSRSnames = open(DNS_Table_Name, "r")
    fDNSRSList = fDNSRSnames.readlines()
    inputEntries = []

    for entry in fDNSRSList:
        inputEntries.append(entry.strip("\n"))
    try:
        rs_socket = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
    except mysoc.error as err:
        print('{}\n'.format("RS socket open error", err))

    rs_server_binding = ('', 51237)
    rs_socket.bind(rs_server_binding)
    rs_socket.listen(1)
    hostname = mysoc.gethostname()
    print("%s" % hostname)
    rs_host_ip = (mysoc.gethostbyname(hostname))
    csockid,addr=rs_socket.accept()
    print("accepted")

    eduConnected = False
    comConnected = False

    while True:
        client_data = csockid.recv(100)
        foundEntry = False
        if not client_data:
            break
        client_data = client_data.strip("\n").strip("\r").strip()
        print("[RS:] Recieved: %s" % client_data)

        for entry in inputEntries:
            entryHostname = getHostnameFromEntry(entry)

            if entryHostname == client_data:
                foundEntry = True
                print("[RS:] Sending: %s" % entry)
                csockid.send(entry)
                break
        if not foundEntry:
            if getComOrEdu(client_data) == 'com':
                comTLDIp = sys.argv[1]
                if not comConnected:
                    try:
                        com_socket = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
                    except mysoc.error as err:
                        print('{}\n'.format("com TLD socket open error %s" % err))
                    com_addr = mysoc.gethostbyname(comTLDIp)
                    com_port = 51238
                    com_server_binding = (com_addr, com_port)
                    com_socket.connect(com_server_binding)
                    comConnected = True

                com_socket.send(client_data)
                print("[RS:] sending to com: %s" % client_data)
                com_data = com_socket.recv(100).strip()
                if com_data:
                    print("[RS:] received %s from com, sending to client" % com_data)
                    csockid.send(com_data)

            elif getComOrEdu(client_data) == 'edu':
                eduTLDIp = sys.argv[2]
                if not eduConnected:
                    try:
                        edu_socket = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
                    except mysoc.error as err:
                        print('{}\n'.format("com TLD socket open error", err))
                    edu_addr = mysoc.gethostbyname(eduTLDIp)
                    edu_port = 51239
                    edu_server_binding = (edu_addr, edu_port)
                    edu_socket.connect(edu_server_binding)
                    eduConnected = True

                edu_socket.send(client_data)
                print("[RS:] sending to edu: %s" % client_data)
                edu_data = edu_socket.recv(100).strip()
                if edu_data:
                    print("[RS:] received %s from edu, sending to client" % edu_data)
                    csockid.send(edu_data)
            else:
                error = client_data + " - Error:HOST NOT FOUND"
                print("[RS:] Sending %s" % error)
                csockid.send(error)
    com_socket.send("**//TERMINATE//**")
    com_socket.close()
    edu_socket.send("**//TERMINATE//**")
    edu_socket.close()
    rs_socket.close()
    exit()


RSserver()
