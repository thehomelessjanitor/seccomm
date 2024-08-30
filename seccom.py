'''
seccom.py project
Made in and for Python3
Version 3.12.# 64-bit

Version 0.2
Author: thehomelessjanitor / Alex
Status: Work in progress
Discription:
    A script that ultilises a p2p TCP socket connection to create a secure connection for 2 people to communicate.

Script is for educational reasons, its not built to be used in a real world critical senario
Its not reliable and just a simple project (/^o^\)

User will need to download the requests module for grabbing the hosts public IP address, not nessasary but nice

______________________________
|                            |
|         get flags          |
|   send connection request  |
|____________________________|
|             |
|             v
|_____________________________
|                            |
|   negotiate ssl for socket |
|     get pubkey from host   |
|     send encrypted passwd  |
|____________________________|

'''

try:
    import sys                      # Shouldnt be too much of an issue, is native to python
    sys.tracebacklimit = 0          # Get rid of gross error messages
    import socket                   # Used for initiating and handling the connections between the 2 clients through layers 3 & 4
    import threading                # Used for running both the recive and write functions
    from requests import get        # Used for getting the public IP address of the host
    import argparse                 # To be able to grab flags the user will enter into the script
    import ssl                      # Enable session layer security
    import rsa                      # Encrypt the strings of text sent, secures the connection at layer 7

except ModuleNotFoundError:
    print("[-]      Nessasary modules not found, do you want to install them? The script wont work without them.")
    print("[-]      Will install (if not already installed) socket, threading, requests, argparse, ssl, rsa")    
    yn = input("[*]    (y/N: )")
    yn.lower()
    if yn not in ("y", "n", "yes", "no", "ye"):
        print("Oops, Invalid input, quitting.")
        exit()
    else:
        print("goodnight, ill make this some other time")

# ---   --- Driver Code ---    --- #

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='example:   seccom.py --port 5678 -p strongPassword --host')
    
    parser.add_argument("-ip", dest="ip", help="If you are not hosting, you need a desination", type=str)
    parser.add_argument("--port", dest="port", help="Port number for the server, Default is 4444", type=int)
    parser.add_argument("-p", "--password", dest="password", help="Password for the server", type=str, required=True)
    parser.add_argument("--host", help="Host a connection", action="store_const", dest="isHosting", default=False)
    
    ip = parser.ip
    port = parser.port
    passwd = parser.password
    host = parser.isHosting
    
    # Above defines the available flags the user can use to modify their connection
    
    if port == None:
        port = 4444     # Sets the default port to 4444, will check if a valid port number was set later
        
    if host == None:
        host = True     # Used for standard sake, because the default value in the parser is False if the flag is
                        # used it will return None, just in case of future error setting to True negates this possibility
    
    asciiart = r"""
     ____  _____ ____  ____ ___  __  __ __  __ 
    / ___|| ____/ ___/ ____/ _ \|  \/  |  \/  |
    \___ \|  _|| |   | |  | | | | |\/| | |\/| |
     ___) | |__| |___| |__| |_| | |  | | |  | |
    |____/|_____\____ \____\___/|_|  |_|_|  |_|"""

    # Defining functions

    def serverAuth(recivedPasswd):              # Compaires the password given from connecting user and
        if recivedPasswd == passwd:             # set password by host
            okMsg = "CONNECTIONACCEPTED"
            conn.send(okMsg.encode())
            return(True)                    

        else:
            incorrectMsg = "That was the wrong password ! ! !"
            conn.send(incorrectMsg.encode())
            conn.close()
            return(False)

    def clientAuth(passwd):
        passwd = conn.recv(1024).decode()       # If the user got the accepted message then
        if passwd == "CONNECTIONACCEPTED":      # the threads will start
            return True
        
        else:
            conn.close()
            return False
    
    def send_message():         # When the user types something into the terminal it will
        message = input("You: ")
        while True:             # encode the message to send
            
            if len(message) != 0:               # check to not infinitely print nothing
                message = str.encode(message)
                conn.send(message)
                print("You: ", message)
                message = input("You: ")

    def get_message():                          # Constantly checking if new data has been sent
        while True:
            
            data = conn.recv(1024).decode()
            if len(data) != 0:                  # check to not infinitely print nothing
                print("Some guy: ", data)
    
    
    def run():                                  # Thread function to run both the send_message function
        while True:                             # and get_message function
            
            get_message_thread = threading.Thread(target=get_message)
            send_message_thread = threading.Thread(target=send_message)

            get_message_thread.start()
            send_message_thread.start()
                 
    print(asciiart)
    
    if host == True:
        
        hostIp = socket.gethostbyname(socket.gethostname())             # grab device ip
        publicIp = get('https://api.ipify.org').content.decode('utf8')  # grab public ip 
        
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # start socket connection on ipv4 and set it to stream
        conn.bind((hostIp, port))       # state that the connection will use the hosts IP and specified port
        conn.listen(1)                  # start listening for connections
        
        print("\n--- Listening ---\n")
        print("Tell them this\n[*]   ip: {} port: {} password: {}".format(publicIp, port, passwd))
        
        conn, addr = conn.accept()      # will start 3 way handshake when someone connects
        
        print("[+]  Client from", addr, "Is connecting...")
        
        recivedPasswd = conn.recv(1024).decode()
        
        if serverAuth(recivedPasswd) == True:
            run()
        else:
            pass            # incorrect auth handled in the function
            
    if host == False:
        
        hostIp = socket.gethostbyname(socket.gethostname())         # grab device ip
        
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # start socket connection with ipv4 and stream
        conn.connect((ip, port))        # try to connect to host
        
        print("\n--- Connecting ---\n")
        
        data = f"{passwd}".encode()
        conn.send(data)
        
        if clientAuth(passwd) == True:
            print("[+]     Connection sucessful")
            run()
        else:
            pass        # incorrect auth handled in the function