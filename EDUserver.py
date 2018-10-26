import sys
import socket as mysoc

def EDUserver():

    fDNSEDUnames = open("PROJ2-DNSEDU.txt", "r")
    fDNSEDUList = fDNSEDUnames.readlines()
    inputEntries = []
    for entry in fDNSEDUList:
        inputEntries.append(entry.strip("\n"))

    try:
        edu_socket=mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
    except mysoc.error as err:
        print('{}\n'.format("EDU socket open error",err))

    edu_server_binding=('', 51239)
    edu_socket.bind(edu_server_binding)
    edu_socket.listen(1)
    hostname = mysoc.gethostname()
    edu_host_ip = (mysoc.gethostbyname(hostname))
    csockid,addr=edu_socket.accept()

    while True:
        rs_data = csockid.recv(100)
        foundEntry = False
        if not rs_data:
            break
        rs_data = rs_data.strip("\n")
        rs_data = rs_data.strip("\r")
        print("[EDU:] Recieved: %s" % rs_data)

        for entry in inputEntries:
            splitEntry = entry.split(" ")
            entryHostname = splitEntry[0].strip("\n")
            entryHostname = splitEntry[0].strip("\r")
            entryHostname = splitEntry[0].strip()
            flag = splitEntry[-1]
            flag = flag.strip()

            if entryHostname == rs_data:
                foundEntry = True
                print("[EDU:] Sending: %s" % entry)
                csockid.send(entry)
            elif flag == 'NS':
                if foundEntry == False:
                    print("[EDU:] Sending NS")
                    csockid.send(entry)

    print("[EDU:] SOCKET CLOSED change made")
    edu_socket.close()
    exit()

EDUserver()
