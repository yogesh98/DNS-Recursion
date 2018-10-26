import socket as mysoc


def initSockets():

    # init rs socket
    try:
        rs_socket = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
    except mysoc.error as err:
        print('{}\n'.format("RS socket open error", err))

    rs_addr = mysoc.gethostbyname(mysoc.gethostname())
    rs_port = 51237
    rs_server_binding = (rs_addr,rs_port)
    rs_socket.connect(rs_server_binding)

    # Open necessary files
    fOut = open("RESOLVED.txt", "w+")
    fHostnames = open("PROJ2-HNS.txt", "r")
    fHostnamesList = fHostnames.readlines()

    for line in fHostnamesList:
        # Send each line to RS server
        stripLine = line.rstrip()
        print("[C:] sending to RS:", stripLine)
        rs_socket.send(stripLine)

        # received data from RS
        rs_data = rs_socket.recv(100).strip()
        print("[C:] Received from RS:", rs_data)
        fOut.write("%s\n" % rs_data)

    rs_socket.close()
    exit()


initSockets()
