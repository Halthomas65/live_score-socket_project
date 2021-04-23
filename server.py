from tkinter import messagebox as ms
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import sqlite3   
import time
clients = {}
addresses = {}

HOST = '127.0.0.1'
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

def main():
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
        
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        addresses[client] = client_address
        Thread(target=handle_client, args=(client, client_address)).start()

def handle_client(client, client_address):  # Takes client socket as argument.
    """Handles a single client connection."""

    while True:
        try:
            data = client.recv(BUFSIZ)
            if not data:
                break
            str_data = data.decode("utf8")
            if str_data=="Register":  #Client register
                UserPass_data = client.recv(BUFSIZ)
                
                UserPass = UserPass_data.decode("utf8").split(":")

                with sqlite3.connect('Accounts.db') as db:
                    c = db.cursor()

                #Find Existing username if any take proper action
                find_user = ('SELECT username FROM user WHERE username = ?')
                c.execute(find_user,[(UserPass[0])])        
                if c.fetchall():
                    client.sendall(bytes("Fail","utf8"))      #Register failed  
                else:
                    client.sendall(bytes("Accept","utf8"))    
                    #Create New Account 
                    insert = 'INSERT INTO user(username,password) VALUES(?,?)'
                    c.execute(insert,[(UserPass[0]),(UserPass[1])])
                    db.commit()
                        
            if str_data=="Login":   #Client login
                UserPass_data = client.recv(BUFSIZ)
                
                UserPass = UserPass_data.decode("utf8").split(":")

                with sqlite3.connect('Accounts.db') as db:
                    c = db.cursor()

                #Find user If there is any take proper action
                find_user = ('SELECT * FROM user WHERE username = ? and password = ?')
                c.execute(find_user,[(UserPass[0]),(UserPass[1])])
                result = c.fetchall()
                if result:
                    client.sendall(bytes("Accept","utf8")) 
                else:
                    client.sendall(bytes("Fail","utf8")) 
            if str_data == "/help":
                client.sendall(bytes("Server: /list all : print all the information about the soccer match at current time. \n"+
                "/quit : exit the server", "utf8" ))
            if str_data == "/quit":
                print("%s:%s has quit" % client_address)
            if str_data == "/list all":
                with sqlite3.connect('Soccer.db') as db:
                    c = db.cursor()
                c.execute('SELECT Time, Team1, Score, Team2 FROM match')  
                data_list = c.fetchall()

                for row in data_list:
                    data = ""
                    for i in range(len(row)):
                        data += str(row[i]) + "   "
                    data += "/"
                client.sendall(bytes(data,"utf8")) 
                time.sleep(0.2) # to guarantee that the data is sending not too fast
                client.sendall(bytes("END","utf8"))
        except:
            break                

    # def broadcast(msg, prefix=""):  # prefix is for name identification.
    #     """Broadcasts a message to all the clients."""

    #     for sock in clients:
    #         sock.send(bytes(prefix, "utf8")+msg)


if __name__ == "__main__":
    # make database and users (if not exists already) table at programme start up
    with sqlite3.connect('Accounts.db') as db:
        c = db.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS user (username TEXT NOT NULL PRIMARY KEY,password TEXT NOT NULL);')
    db.commit()
    db.close()
    main()