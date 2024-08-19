import socket
import threading
import os
import sys

asciiart = r"""
 ____  _____ ____ ____  _____ _____ ____ ___  __  __ __  __ 
/ ___|| ____/ ___|  _ \| ____|_   _/ ___/ _ \|  \/  |  \/  |
\___ \|  _|| |   | |_) |  _|   | || |  | | | | |\/| | |\/| |
 ___) | |__| |___|  _ <| |___  | || |__| |_| | |  | | |  | |
|____/|_____\____|_| \_\_____| |_| \____\___/|_|  |_|_|  |_|
"""

def serverAuth(recivedPasswd):

    if recivedPasswd == passwd:
        okMsg = "CONNECTIONACCEPTED"
        conn.send(okMsg.encode())
        return(True)
    elif recivedPasswd == "":
        print("emptly message")
        return(False)
    else:
        incorrectMsg = "That was the wrong password ! ! !"
        conn.send(incorrectMsg.encode())
        return(False)
        
def clientAuth():
    waitForAuth = conn.recv(1024).decode()
    print(waitForAuth)
    if waitForAuth != "CONNECTIONACCEPTED":
        print(r"Connection Failed (Bad password attempt)")
    else:
        return(True)
        
def write():
    while True:
        write_message = str(input(""))
        if write_message == "exit.session":
            print("You exited the session")
        else:
            conn.send(write_message.encode())        

def receive():
    while True:
        try:
            rece_message = conn.recv(1024).decode()
            if rece_message == "exit.session":
                print("\nPerson ended the chat session")
                sys.exit()
            else:
                print("Received: ",rece_message)
        except:
            print("Oops.. An error ;-;")
            conn.close()
            break

if __name__ == '__main__':

    os.system('cls' if os.name == 'nt' else 'clear')
    print(asciiart)
    asking = int(input("Are you trying to connect or host?\nConnect (1)\nHost (2)\nChoose 1 or 2 :"))
    
    if asking == 1:
        host = str(input("IP Address of the Host: "))
        port = int(input("Port Number: "))
        passwd = str(input("Enter server password: "))  
        
        if passwd == "":
            print("cant deal w this rn just empty password")
            sys.exit()
        
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((host, port))
        
        data = f"{passwd}".encode()
        conn.send(data)
        
        if clientAuth() == True:
            receive_thread = threading.Thread(target=receive)
            receive_thread.start()
            
            write_thread = threading.Thread(target=write)
            write_thread.start()
            
    if asking == 2:
        host = str(input("IP Address for the Host: "))
        port = int(input("Port number : "))
        passwd = str(input("Enter password for server: "))
        
        os.system('cls' if os.name == 'nt' else 'clear')
        print(asciiart, "\nHost: {}\nPort: {}\nPassword: {}\n".format(host,port,passwd))
        
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.bind((host, port))
        conn.listen(1)
        print("\n--- Listening ---\n")
    
        conn, addr = conn.accept()
        recivedPasswd = conn.recv(1024).decode()
        print("Client from", addr, "Is connecting...")
        checkAuth = serverAuth(recivedPasswd)
        
        if checkAuth != True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(asciiart, "\nHost: {}\nPort: {}\nPassword: {}\n".format(host,port,passwd))
            print("Client from", addr, "Didnt have the right Auth")
            conn.close()
        
        if checkAuth == True:
            receive_thread = threading.Thread(target=receive)
            receive_thread.start()
            
            write_thread = threading.Thread(target=write)
            write_thread.start()