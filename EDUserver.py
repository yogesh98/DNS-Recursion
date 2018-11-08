import sys
import socket as mysoc


def getHostnameFromEntry(entry):
    splitEntry = entry.split(" ")
    entryHostname = splitEntry[0].strip("\n").strip("\r").strip()
    return entryHostname


def EDUserver():
    DNS_Table_Name = sys.argv[1]
    fDNSEDUnames = open(DNS_Table_Name, "r")
    fDNSEDUList = fDNSEDUnames.readlines()
    inputEntries = []
    for entry in fDNSEDUList:
        inputEntries.append(entry.strip("\n"))

    try:
        edu_socket = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
    except mysoc.error as err:
        print('{}\n'.format("EDU socket open error %" % err))

    edu_server_binding = ('', 51239)
    edu_socket.bind(edu_server_binding)
    edu_socket.listen(1)
    hostname = mysoc.gethostname()
    edu_host_ip = (mysoc.gethostbyname(hostname))
    print("%s" % hostname)
    rsockid, addr = edu_socket.accept()

    while True:
        rs_data = rsockid.recv(100)
        if rs_data:
            foundEntry = False
            rs_data = rs_data.strip("\n").strip("\r").strip()
            print("[EDU:] Recieved: %s" % rs_data)

            for entry in inputEntries:
                entryHostname = getHostnameFromEntry(entry)

                if entryHostname == rs_data:
                    foundEntry = True
                    print("[EDU:] Sending: %s" % entry)
                    rsockid.send(entry)
                    break
            if not foundEntry:
                error = rs_data + " - Error:HOST NOT FOUND"
                print("[EDU:] Sending %s" % error)
                rsockid.send(error)


    print("[EDU:] SOCKET CLOSED change made")
    edu_socket.close()
    exit()

EDUserver()
