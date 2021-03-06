from tkinter import Tk, Frame, Scrollbar, Label, END, Entry, Text, VERTICAL, Button, StringVar, W, Toplevel, Listbox
import socket
import threading
from tkinter import messagebox as ms
import sqlite3
import time
import tkinter.simpledialog as sd
class GUI:
    client_socket = None
    last_received_message = None

    def __init__(self, master):
        self.root = master
        self.chat_transcript_area = None
        self.name_widget = None
        self.enter_text_widget = None
        self.join_button = None
        # Some Usefull variables
        self.username = StringVar()
        self.password = StringVar()
        self.n_username = StringVar()
        self.n_password = StringVar()
        self.ipaddr = ''
        self.port = ''
        top = Frame()
        Label(top, text="The ip address would be default and the port will be 33000 if you do not input the new ones", font=("Serif", 12), padx = 150, pady = 5).pack(side='right')
        top.pack()
        self.getUserInput()
        top.pack_forget()
        self.initialize_socket()
        
        #Create Widgets (Login, Register)
        self.widgets()
        
    def getUserInput(self):
        self.ipaddr = None
        self.ipaddr = sd.askstring('User Input','Enter IP address')
        if self.ipaddr:
            pass
        else:
            self.ipaddr = '127.0.0.1'
        
        self.port = None
        self.port = sd.askstring('User Input','Enter Port')
        if self.port:
            pass
        else:
            self.port = 33000
    def initialize_socket(self):
        
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # remote_ip = '192.168.1.19'
        # remote_port = 33000
        
        self.client_socket.connect((self.ipaddr, int(self.port)))
  
        #self.client_socket.connect((self.ipaddr.get(), remote_port))
    def initialize_gui(self):
        self.root.title("Socket Soccer")
        self.root.resizable(0, 0)
        self.display_command_box()
        self.display_command_entry_box()

    def display_command_box(self):
        frame = Frame()
        Label(frame, text='Command Box:', font=("Serif", 12)).pack(side='top', anchor='w')
        self.chat_transcript_area = Text(frame, width=60, height=10, font=("Serif", 12))
        scrollbar = Scrollbar(frame, command=self.chat_transcript_area.yview, orient=VERTICAL)
        self.chat_transcript_area.config(yscrollcommand=scrollbar.set)
        self.chat_transcript_area.bind('<KeyPress>', lambda e: 'break')
        self.chat_transcript_area.pack(side='left', padx=10)
        scrollbar.pack(side='right', fill='y')
        frame.pack(side='top')
        
    def display_command_entry_box(self):
        frame = Frame()
        Label(frame, text='Enter command:', font=("Serif", 12)).pack(side='top', anchor='w')
        self.enter_text_widget = Text(frame, width=60, height=1, font=("Serif", 12))
        self.enter_text_widget.pack(side='left', pady=5)
        self.enter_text_widget.bind('<Return>', self.send)
        frame.pack(side='top')

    def clear_text(self): # To remove text, avoid duplicate in chat box
        self.enter_text_widget.delete(1.0, 'end')

    def send(self, event):
        senders_name = self.username.get().strip() + ": " # strip() = print
        data = self.enter_text_widget.get(1.0, 'end').strip()
        message = (senders_name + data).encode('utf-8')
        self.chat_transcript_area.insert('end', message.decode('utf-8') + '\n') #To see text in chat box
        self.chat_transcript_area.yview(END)
        self.client_socket.send(message)
        self.clear_text()
        
        if data == "/help":
            self.client_socket.sendall(bytes("/help", "utf8"))
            msg = self.client_socket.recv(1024)
            self.chat_transcript_area.insert('end', msg.decode('utf-8') + '\n')
            self.chat_transcript_area.yview(END)
        if data == "/quit":
            self.client_socket.sendall(bytes("/quit", "utf8"))   
            self.root.destroy()
            self.client_socket.close()
            exit(0)              
        if data == "/list all": #li???t k?? danh s??ch
            self.client_socket.sendall(bytes("/list all", "utf8")) #H??m g???i ?????n server chu???i /list all ???????c t??ch th??nh t???ng byte theo ki???u utf8
            self.print_list() #In danh s??ch tr???n ?????u nh???n ???????c t??? server
        if data == "/list all date": #li???t k?? danh s??ch ch???n theo ng??y
            self.client_socket.sendall(bytes("/list all date", "utf8")) #gi???ng tr??n

            self.top = Toplevel() #T???o m???t c??i c???a s??? 
            self.top.title("Date") #Ti??u ????? cho c???a s???
            self.entry_field = Entry(self.top) #ch??? ????? nh???p data
            self.entry_field.grid(row = 1, column = 0, columnspan = 4) #t???o k??ch c??? cho c??i khung c???a s???
            send_button = Button(self.top, text = "Send",command = self.send_date) #t???o c??i n??t Send v???i khi b???m v??o n??t th?? g???i h??m send_date
            send_button.grid(row = 2, column = 1) #T???o k??ch c??? cho c??i n??t Send

            quit_button = Button(self.top, text = "Quit", command = self.top.destroy) #nh?? tr??n m?? n??t Quit 
            quit_button.grid(row = 2, column = 2)

        if data == "/score":
            self.client_socket.sendall(bytes("/score", "utf8"))           
            self.top = Toplevel()
            self.top.title("Score")
            self.scrollbar = Scrollbar(self.top) #t???o thanh k??o
            self.list_box = Listbox(self.top, height = 30, width = 55, yscrollcommand = self.scrollbar.set) #t???o c??i khung ????? hi???n th???
            self.scrollbar.grid(row = 0,column = 5,ipady = 90)
            self.list_box.grid(row = 0,column = 0,columnspan = 4)

            #msg = self.client_socket.recv(1024) #receive the data for the list box from server
            data = ""
            while True: 
                msg = self.client_socket.recv(1024)
                data_decode = msg.decode("utf8")
                if data_decode == "END":
                    break
                data += data_decode

            l = data.split("/")
            
            self.list_box.insert('end', "ID    / Time    / Team1    / Score    / Team2    / Date\n")
            for i in range(len(l)): 
                self.list_box.insert('end', l[i] + '\n')

            #send the match's ID to server
            self.entry_field = Entry(self.top) 
            #self.entry_field.bind("<Return>", self.send_score)
            self.entry_field.grid(row = 1, column = 0, columnspan = 4)
            send_button = Button(self.top, text = "Send",command = self.send_score)
            send_button.grid(row = 2, column = 1)

            quit_button = Button(self.top, text = "Quit", command = self.top.destroy)
            quit_button.grid(row = 2, column = 2)


        if data == "/clear":
            self.chat_transcript_area.delete(1.0,'end')

    def on_close_window(self):
        if ms.askokcancel("Quit", "Do you want to quit?"):
            self.client_socket.sendall(bytes("/quit", "utf8"))
            self.root.destroy()
            self.client_socket.close()
            exit(0)

    #Login Function
    def login(self):
        
        self.client_socket.sendall(bytes("Login","utf8"))
        self.client_socket.sendall(bytes(self.username.get() + ":" + self.password.get(), "utf8"))
        msg = self.client_socket.recv(1024)
        
        data=msg.decode("utf8")

        if data=="Accept": 
            self.logf.pack_forget()  #to remove previous UI login
            self.head.pack_forget()
            self.initialize_gui()
        else:           
            ms.showerror('Username Not Found!', 'Please login again.')            
            
    def new_user(self):
        self.client_socket.sendall(bytes("Register","utf8"))
        self.client_socket.sendall(bytes(self.n_username.get()+ ":" + self.n_password.get(), "utf8"))

        msg = self.client_socket.recv(1024)

        data = msg.decode("utf8")

        if data == "Accept": 
            ms.showinfo('Success!','Account Created!')
            self.log()
        else:           
            ms.showerror('Error!','Username Taken Try a Diffrent One.')    

        #Frame Packing Methords
    def log(self):
        self.username.set('')
        self.password.set('')
        self.crf.pack_forget()
        self.head['text'] = 'LOGIN'
        self.logf.pack()
    def cr(self):
        self.n_username.set('')
        self.n_password.set('')
        self.logf.pack_forget()
        self.head['text'] = 'REGISTER'
        self.crf.pack()
        
    #Draw Widgets
    def widgets(self):
        self.head = Label(self.root,text = 'LOGIN',font = ('',35),pady = 10)
        self.head.pack()
        self.logf = Frame(self.root,padx =10,pady = 10) #Login frame
        Label(self.logf,text = 'Username: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        Entry(self.logf,textvariable = self.username,bd = 5,font = ('',15)).grid(row=0,column=1)
        Label(self.logf,text = 'Password: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        Entry(self.logf,textvariable = self.password,bd = 5,font = ('',15),show = '*').grid(row=1,column=1)
        Button(self.logf,text = ' Login ',bd = 3 ,fg = 'blue', font = ('',15),padx=5,pady=5,command=self.login).grid()
        Button(self.logf,text = ' Register ',bd = 3 ,fg = 'green', font = ('',15),padx=5,pady=5,command=self.cr).grid(row=2,column=1)
        Button(self.logf,text = ' Exit ',bd = 3 ,fg = 'red', font = ('',15),padx=5,pady=5,command=self.on_close_window).grid(row=2,column=2)
        self.logf.pack()
        
        self.crf = Frame(self.root,padx =10,pady = 10) #Create account frame
        Label(self.crf,text = 'Username: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        Entry(self.crf,textvariable = self.n_username,bd = 5,font = ('',15)).grid(row=0,column=1)
        Label(self.crf,text = 'Password: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        Entry(self.crf,textvariable = self.n_password,bd = 5,font = ('',15),show = '*').grid(row=1,column=1)
        Button(self.crf,text = 'Register',bd = 3 ,fg = 'green',font = ('',15),padx=5,pady=5,command=self.new_user).grid()
        Button(self.crf,text = 'Go to Login',bd = 3 ,fg = 'blue', font = ('',15),padx=5,pady=5,command=self.log).grid(row=2,column=1)

    def print_list(self): #
        data = ""
        while True: 
            msg = self.client_socket.recv(1024)
            data_decode = msg.decode("utf8")
            if data_decode == "END":
                break
            data += data_decode

        l = data.split("/")
        
        self.chat_transcript_area.insert('end', "Time    / Team1    / Score    / Team2     / Date\n")
        for i in range(len(l)): 
            self.chat_transcript_area.insert('end', l[i] + '\n')

    def send_score(self): #
        data = self.entry_field.get()
        self.client_socket.sendall(bytes(str(data), "utf8"))
        #msg = self.client_socket.recv(1024)
        
        #get the detail of that match from server
        data = ""
        while True: 
            msg = self.client_socket.recv(1024)
            data_decode = msg.decode("utf8")
            if data_decode == "END":
                break
            data += data_decode

        l = data.split("/")
            
        self.chat_transcript_area.insert('end', "Time    / Team1    / Score | Yellow card | Red card    / Team2\n")
        for i in range(len(l)): 
            self.chat_transcript_area.insert('end', l[i] + '\n')

        self.top.destroy()
    def send_date(self): #
        data = self.entry_field.get()
        self.client_socket.sendall(bytes(str(data), "utf8"))

        data = ""
        while True: 
            msg = self.client_socket.recv(1024)
            data_decode = msg.decode("utf8")
            if data_decode == "Date not exist!":
                self.chat_transcript_area.insert('end', "Input date not exist, please input another!\n")
                break
            if data_decode == "END":
                break
            data += data_decode
        if data:
            l = data.split("/")
            self.chat_transcript_area.insert('end', "Time    / Team1    / Score   / Team2\n")
            for i in range(len(l)): 
                self.chat_transcript_area.insert('end', l[i] + '\n')
            self.top.destroy()
        else:
            self.top.destroy()
if __name__ == '__main__':
    root = Tk()
    gui = GUI(root)
    root.protocol("WM_DELETE_WINDOW", gui.on_close_window)
    root.mainloop()