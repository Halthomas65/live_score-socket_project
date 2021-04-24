from tkinter import messagebox as ms
from tkinter import Frame, Label, Entry, Button, Toplevel, Tk, Text, Scrollbar, VERTICAL, Listbox
from socket import AF_INET, socket, SOCK_STREAM
import os
from threading import Thread
import sqlite3   
import time
import subprocess as commands
import socket as sk

BUFSIZ = 1024
SERVER = socket(AF_INET, SOCK_STREAM)
#HOST = '127.0.0.1'
HOST = '192.168.1.18'
PORT = 33000
ADDR = (HOST, PORT)
SERVER.bind(ADDR)
class Server:
    clients = {}
    addresses = {}
    string = ''
    def __init__(self, master):
        self.root = master
        
        
        SERVER.listen(5)
        ACCEPT_THREAD = Thread(target=self.accept_incoming_connections)
        ACCEPT_THREAD.start()
        self.GUI()
        self.GUI2()
        self.root.mainloop()
        
        
        ACCEPT_THREAD.join()
        
        SERVER.close()
    def GUI(self):
        self.top = Toplevel()
        self.top.title("Notification!")

        Label(self.top,text='Your IP address: {}'.format(self.get_ip_address()),font='Helvetica 10 bold').pack(side='top')
        Label(self.top,text='Port to host on: {}'.format('33000'),font='Helvetica 10 bold').pack(side='left')
        Label(self.top,text='Remember to notify your IP and Port to Client: ',font='Helvetica 10 bold').pack(side='left')
        start_button = Button(self.top,text='Okay',command = self.top.destroy)
        start_button.pack(side='left',padx=10)
        #HOST = get_ip_address()
        
        #self.top.mainloop()
    def GUI2(self):
        
        self.root.title("Soccer Server")
        scrollbar = Scrollbar(self.root)
        self.list_box = Listbox(self.root, height = 45, width = 80, yscrollcommand = scrollbar.set)
        scrollbar.grid(row = 0,column = 5,ipady = 90)
        self.list_box.grid(row = 0,column = 0,columnspan = 10)
        self.list_box.insert('end', "Waiting for connection")
        
    def get_ip_address(self):
        if os.name == 'posix':
            ip = commands.getoutput("hostname -I")
        elif os.name == 'nt':
            ip = sk.gethostbyname(sk.gethostname())
        else:
            ip = ''
            print('Couldn\'t get local ip')
        return ip

    def accept_incoming_connections(self):
        """Sets up handling for incoming clients."""
        while True:
            self.client, self.client_address = SERVER.accept()
            self.addresses[self.client] = self.client_address
            Thread(target=self.handle_client).start()

    def handle_client(self):  # Takes client socket as argument.
        """Handles a single client connection."""
        self.list_box.insert('end', self.client_address[0] +':' +str(self.client_address[1]) + " has connected")
        while True:
            try:
                data = self.client.recv(BUFSIZ)
                if not data:
                    break
                str_data = data.decode("utf8")
                if str_data=="Register":  #Client register
                    self.list_box.insert('end')
                    UserPass_data = self.client.recv(BUFSIZ)
                    
                    UserPass = UserPass_data.decode("utf8").split(":")

                    with sqlite3.connect('Accounts.db') as db:
                        c = db.cursor()

                    #Find Existing username if any take proper action
                    find_user = ('SELECT username FROM user WHERE username = ?')
                    c.execute(find_user,[(UserPass[0])])        
                    if c.fetchall():
                        self.client.sendall(bytes("Decline","utf8"))      #Register failed  
                    else:
                        self.client.sendall(bytes("Accept","utf8"))    
                        #Create New Account 
                        insert = 'INSERT INTO user(username,password) VALUES(?,?)'
                        c.execute(insert,[(UserPass[0]),(UserPass[1])])
                        db.commit()
                            
                if str_data=="Login":   #Client login
                    self.list_box.insert('end', self.client_address[0] +':' +str(self.client_address[1]) + " has login")
                    UserPass_data = self.client.recv(BUFSIZ)
                    
                    UserPass = UserPass_data.decode("utf8").split(":")

                    with sqlite3.connect('Accounts.db') as db:
                        c = db.cursor()

                    #Find user If there is any take proper action
                    find_user = ('SELECT * FROM user WHERE username = ? and password = ?')
                    c.execute(find_user,[(UserPass[0]),(UserPass[1])])
                    result = c.fetchall()
                    if result:
                        self.client.sendall(bytes("Accept","utf8")) 
                    else:
                        self.client.sendall(bytes("Decline","utf8")) 
                if str_data == "/help":
                    self.client.sendall(bytes("Server: /list all : print all the information about the soccer match at current time. \n"
                    +"/list all date: to list the match at the date input\n" +"/soccer: to view the detail of the match (imcomple)\n" +"/quit : exit the server\n"+ "/clear: clear all text in the box\n", "utf8" ))
                if str_data == "/quit":
                    self.list_box.insert('end', self.client_address[0] +':' +str(self.client_address[1]) + " has quit")

                if str_data == "/list all":
                    self.list_box.insert('end', self.client_address[0] +':' +str(self.client_address[1]) + " /list all")
                    with sqlite3.connect('Soccer.db') as db:
                        c = db.cursor()
                    c.execute('SELECT Time, Team1, Score, Team2, Date FROM match')  
                    data_list = c.fetchall()

                    for row in data_list:
                        data = ""
                        for i in range(len(row)):
                            data += str(row[i]) + "   "
                        data += "/"
                    self.client.sendall(bytes(data,"utf8")) 
                    time.sleep(0.2) # to guarantee that the data is sending not too fast
                    self.client.sendall(bytes("END","utf8"))
                if str_data == "/list all date":
                    self.list_box.insert('end', self.client_address[0] +':' +str(self.client_address[1]) + " /list all date")
                    with sqlite3.connect('Soccer.db') as db:
                        c = db.cursor()
                    
                    msg = self.client.recv(1024)
                    date = msg.decode("utf8")
                    c.execute('SELECT Time, Team1, Score, Team2 FROM match WHERE Date = ?', (date,))

                    data_list = c.fetchall()
                    if data_list:
                        for row in data_list:
                            data = ""
                            for i in range(len(row)):
                                data += str(row[i]) + "   "
                            data += "/"
                            self.client.sendall(bytes(data,"utf8")) 
                        time.sleep(0.2) # to guarantee that the data is sending not too fast
                        self.client.sendall(bytes("END","utf8"))
                    else:
                        self.client.sendall(bytes("Date not exist!", "utf8"))
                    

                if str_data == "/score":
                    self.list_box.insert('end', self.client_address[0] +':' +str(self.client_address[1]) + " /score")
                    with sqlite3.connect('Soccer.db') as db:
                        c = db.cursor()
                    #send the data list to client
                    c.execute('SELECT ID, Time, Team1, Score, Team2, Date FROM match')  
                    data_list = c.fetchall()

                    for row in data_list:
                        data = ""
                        for i in range(len(row)):
                            data += str(row[i]) + "   "
                        data += "/"
                    self.client.sendall(bytes(data,"utf8")) 
                    time.sleep(0.2) # to guarantee that the data is sending not too fast
                    self.client.sendall(bytes("END","utf8"))

                    db.commit()
                    db.close()
                    
                    # with sqlite3.connect('Soccer.db') as db:
                    #     c1 = db.cursor()
                    #get the match's id from client and send the score of that match to client
                    
                    # msg = self.client.recv(BUFSIZ) #Match's id
                    # ID_M = msg.decode("utf8")

                    # self.client.sendall(bytes(data_list,"utf8"))
                    # check = c1.execute('SELECT ID_SCORE FROM detail WHERE ID_SCORE = ? AND ID_M = ?', 'NULL', (ID_M,)) #check if someone score
                    # if check:
                    #     check2 = c1.execute('SELECT ID_YC FROM detail WHERE ID_YC = ? AND ID_M = ?', 'NULL', (ID_M,)) #check if someone got yellow card
                    #     if check2:
                    #         c1.execute('SELECT d.TIME_IN_MATCH, yc.PLAYER_NAME, yc.NOTE FROM detail d JOIN yellow_card yc ON d.ID_YC = yc.ID_YC WHERE d.ID_M = ?', (ID_M,))
                    #     else:
                    #         c1.execute('SELECT d.TIME_IN_MATCH, rc.PLAYER_NAME, rc.NOTE FROM detail d JOIN red_card rc ON d.ID_RC = rc.ID_RC WHERE d.ID_M = ?', (ID_M,))
                    # else:
                        #c1.execute('SELECT d.TIME_IN_MATCH, s.PLAYER_NAME, s.SCORE_CURRENT FROM detail d JOIN score s ON d.ID_SCORE = s.ID_SCORE JOIN match m ON d.ID = m.ID AND d.TEAM = m.Team1 WHERE d.ID_M = ?', (ID_M,))
                        #c1.execute('SELECT d.TIME_IN_MATCH, s.SCORE_CURRENT, s.PLAYER_NAME FROM detail d JOIN score s ON d.ID_SCORE = s.ID_SCORE JOIN match m ON d.ID = m.ID AND d.TEAM = m.Team2 WHERE d.ID_M = ?', (ID_M,))
    
                    # data_list = c1.fetchall()
                    
                    # for row in data_list:
                    #     data_encode = ""
                    #     for i in range(len(row)):
                    #         data_encode += str(row[i]) + "   "
                    #     data_encode += "/"
                        
                    #     self.client.sendall(bytes(data_encode,"utf8"))
                    
                    # time.sleep(0.5) # to guarantee that the data is sending not too fast
                    
                    # db.commit()
                    # db.close()
                    # self.client.sendall(bytes("END","utf8"))

            except:
                break                

        # def broadcast(msg, prefix=""):  # prefix is for name identification.
        #     """Broadcasts a message to all the clients."""

        #     for sock in clients:
        #         sock.send(bytes(prefix, "utf8")+msg)
    # def on_close_window(self):
    #     if ms.askokcancel("Shutdown", "Do you want to shutdown server?"):
    #         self.client.sendall(bytes("/shutdown", "utf8"))
    #         self.list_box.insert('end', "Server is shutting down...")
    #         time.sleep(5.0)
    #         self.root.destroy()
    #         self.client.close()
    #         exit(0)

if __name__ == "__main__":
    # make database and users (if not exists already) table at programme start up
    with sqlite3.connect('Accounts.db') as db:
        c = db.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS user (username TEXT NOT NULL PRIMARY KEY,password TEXT NOT NULL);')
    db.commit()
    db.close()
    
    root = Tk()
    server = Server(root)
    #root.protocol("WM_DELETE_WINDOW", server.on_close_window)
    root.mainloop()

    