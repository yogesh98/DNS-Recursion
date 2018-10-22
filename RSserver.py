import socket as mysoc


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

    fDNSRSnames = open("PROJ2-DNSRS.txt", "r")
    fDNSRSList = fDNSRSnames.readlines()
    inputEntries = []

    comServerPosition = -1
    eduServerPosition = -1
    entryPos = 0
    for entry in fDNSRSList:
        inputEntries.append(entry.strip("\n"))

        entryHostname = getHostnameFromEntry(entry)
        flag = getFlagFromEntry(entry)
        comOrEdu = getComOrEdu(entry)

        if flag == 'NS':
            if comOrEdu == 'com':
                comServerPosition = entryPos
            elif comOrEdu == 'edu':
                eduServerPosition = entryPos
        entryPos += 1

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
            entryHostname = getHostnameFromEntry(entry)
            flag = getFlagFromEntry(entry)

            if entryHostname == client_data:
                foundEntry = True
                print("[RS:] Sending: %s" % entry)
                csockid.send(entry)
                break
        if foundEntry == False:
            # TODO: send client_data to TLD, wait for data back
            # TODO: send received data from TLD to client
            if getComOrEdu(client_data) == 'com':
                comTLDIp = getIpFromDNS(inputEntries[comServerPosition])
                try:
                    com_socket = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
                except mysoc.error as err:
                    print('{}\n'.format("com TLD socket open error", err))
                com_addr = mysoc.gethostbyname(comTLDIp)
                com_port = 51238
                com_server_binding = (com_addr, com_port)
                com_socket.connect(com_server_binding)
            elif getComOrEdu(client_data) == 'edu':
                eduTLDIp = getIpFromDNS(inputEntries[eduServerPosition])
                try:
                    edu_socket = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
                except mysoc.error as err:
                    print('{}\n'.format("com TLD socket open error", err))
                edu_addr = mysoc.gethostbyname(eduTLDIp)
                edu_port = 51239
                edu_server_binding = (edu_addr, edu_port)
                edu_socket.connect(edu_server_binding)


    rs_socket.close()
    exit()


RSserver()
