import socket as mysoc
import sys


def initSockets():

    # init rs socket
    try:
        rs_socket = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
    except mysoc.error as err:
        print('{}\n'.format("RS socket open error %s" % err))

    RS_host_name = sys.argv[1]
    rs_addr = mysoc.gethostbyname(RS_host_name)
    rs_port = 51237
    rs_server_binding = (rs_addr,rs_port)
    rs_socket.connect(rs_server_binding)

    # Open necessary files
    fOut = open("RESOLVED.txt", "w+")
    DNS_Table_Name = sys.argv[2]
    fHostnames = open(DNS_Table_Name, "r")
    fHostnamesList = fHostnames.readlines()

    for line in fHostnamesList:
        # Send each line to RS server
        stripLine = line.rstrip()
        print("[C:] sending to RS: %s" % stripLine)
        rs_socket.send(stripLine)

        # received data from RS
        rs_data = rs_socket.recv(100).strip()
        print("[C:] Received from RS: %s" % rs_data)
        fOut.write("%s\n" % rs_data)

    rs_socket.close()
    exit()


initSockets()
