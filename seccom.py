'''
seccom.py project

Version 0.2
Author: thehomelessjanitor / Alex
Status: Work in progress
Discription:
    A script that ultilises a p2p TCP socket connection to create a secure connection for 2 people to communicate.

Script is for educational reasons, its not built to be used in a real world critical senario
Its not reliable and just a simple project (/^o^\)
'''

import socket
import threading
from requests import get
import argparse

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
    
    if port == None:
        port = 4444
        
    if host == None:
        host = True
    
    asciiart = r"""
     ____  _____ ____  ____ ___  __  __ __  __ 
    / ___|| ____/ ___/ ____/ _ \|  \/  |  \/  |
    \___ \|  _|| |   | |  | | | | |\/| | |\/| |
     ___) | |__| |___| |__| |_| | |  | | |  | |
    |____/|_____\____ \____\___/|_|  |_|_|  |_|
    """

    def serverAuth(recivedPasswd):
        if recivedPasswd == passwd:
            okMsg = "CONNECTIONACCEPTED"
            conn.send(okMsg.encode())
            return(True)
        
        else:
            incorrectMsg = "That was the wrong password ! ! !"
            conn.send(incorrectMsg.encode())
            conn.close()
            return(False)

    def clientAuth(passwd):
        passwd = conn.recv(1024).decode()
        if passwd == "CONNECTIONACCEPTED":
            return True
        
        else:
            conn.close()
            return False
    
    def send_message():
        while True:
            message = input()
            
            if len(message) != 0:
                message = str.encode(message)
                conn.send(message)
                print("You: ", message)

    def get_message():
        while True:
            
            data = conn.recv(1024).decode()
            if len(data) != 0:
                print("Some guy: ", data)
    
    
    def run():
        while True:
            
            get_message_thread = threading.Thread(target=get_message)
            send_message_thread = threading.Thread(target=send_message)

            get_message_thread.start()
            send_message_thread.start()
                 
    print(asciiart)
    
    if host == True:
        
        hostIp = socket.gethostbyname(socket.gethostname())
        publicIp = get('https://api.ipify.org').content.decode('utf8')
        
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.bind((hostIp, port))
        conn.listen(1)
        
        print("\n--- Listening ---\n")
        print("Tell them this\n[*]   ip: {} port: {} password: {}".format(publicIp, port, passwd))
        
        conn, addr = conn.accept()
        
        print("Client from", addr, "Is connecting...")
        
        recivedPasswd = conn.recv(1024).decode()
        
        if serverAuth(recivedPasswd) == True:
            run()
        else:
            conn.close()
            
    if host == False:
        
        hostIp = socket.gethostbyname(socket.gethostname())
        
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((ip, port))
        
        print("\n--- Connecting ---\n")
        
        data = f"{passwd}".encode()
        conn.send(data)
        
        if clientAuth(passwd) == True:
            run()
        else:
            conn.close()