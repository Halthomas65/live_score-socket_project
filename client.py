from tkinter import Tk, Frame, Scrollbar, Label, END, Entry, Text, VERTICAL, Button, StringVar, W, Toplevel, Listbox
import socket
import threading
from tkinter import messagebox as ms
import sqlite3
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
        self.initialize_socket()
        #Create Widgets (Login, Register)
        self.widgets()
        

    def initialize_socket(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_ip = '127.0.0.1'
        remote_port = 33000
        self.client_socket.connect((remote_ip, remote_port))

    def initialize_gui(self):
        self.root.title("Socket Soccer")
        self.root.resizable(0, 0)
        self.display_command_box()
        self.display_command_entry_box()

    

    # def listen_for_incoming_messages_in_a_thread(self):
    #     thread = threading.Thread(target=self.receive_message_from_server, args=(self.client_socket,))
    #     thread.start()

    # def receive_message_from_server(self, so):
    #     while True:
    #         buffer = so.recv(256)
    #         if not buffer:
    #             break
    #         message = buffer.decode('utf-8')
    #         # self.chat_transcript_area.insert('end', message + '\n')
    #         # self.chat_transcript_area.yview(END)
    #         if "joined" in message:
    #             user = message.split(":")[1]
    #             message = user + " has joined"
    #             self.chat_transcript_area.insert('end', message + '\n')
    #             self.chat_transcript_area.yview(END)
    #         else:
    #             self.chat_transcript_area.insert('end', message + '\n')
    #             self.chat_transcript_area.yview(END)

    #     so.close()

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
        if data == "/list all":
            self.client_socket.sendall(bytes("/list all", "utf8"))
            self.print_list()
        if data == "/score":
            #self.client_socket.sendall(bytes("/score", "utf8"))

            top = Toplevel()
            top.title("Score")
            self.scrollbar = Scrollbar(top)
            self.list_box = Listbox(top, height=30, width=55, yscrollcommand = self.scrollbar.set)
            self.scrollbar.grid(row=0,column=5,ipady=90)
            self.list_box.grid(row=0,column=0,columnspan=4)

            # entry_field = Entry(top)
            # #entry_field.bind("<Return>", send)
            # entry_field.grid(row=1,column=0,columnspan=4)
            # send_button = Button(top, text="Send",command=lambda :city(entry_field.get(),msg_list,top1))
            # send_button.grid(row=2,column=1)

            # quit_button= Button(top1,text="Quit",command=top1.destroy)
            # quit_button.grid(row=2,column=2)
            # entry_field.grid(row=1,column=0,columnspan=4)
            # send_button = Button(top1, text="Send",command=lambda :city(entry_field.get(),msg_list,top1))
            # send_button.grid(row=2,column=1)

            # quit_button= Button(top1,text="Quit",command=top1.destroy)
            # quit_button.grid(row=2,column=2)

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

    def print_list(self):
        data = ""
        while True: 
            msg = self.client_socket.recv(1024)
            data_decode = msg.decode("utf8")
            if data_decode == "END":
                break
            data += data_decode

        l = data.split("/")
        
        self.chat_transcript_area.insert('end', "Time    / Team1    / Score    / Team2\n")
        for i in range(len(l)): 
            self.chat_transcript_area.insert('end', l[i] + '\n')

if __name__ == '__main__':
    root = Tk()
    gui = GUI(root)
    root.protocol("WM_DELETE_WINDOW", gui.on_close_window)
    root.mainloop()