import socket
import threading
from tkinter import *
import tkinter as tk
from tkinter import messagebox
from pynput.keyboard import Key, Listener

#socket defining sending and receiving functions
messages = []

QUIT_MSG = "-- guest has DISCONNECTED --"
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST_NAME = socket.gethostbyname(socket.gethostname())
PORT = 5050
client_socket.connect((HOST_NAME, PORT))
print(f"You are connected to {HOST_NAME}")


def send_msg():
    msg = input_entry.get()
    client_socket.send(bytes(msg, encoding="utf-8"))
    messages.append(msg)
    output.insert(tk.END , f"You: {msg} \n")
    output.tag_add("here", "1.0", END)
    output.tag_config("here", foreground="blue")
    
    input_entry.delete(0, END)



def receive_msg():
    global messages
    global guest_quit
    guest_quit = False
    while True:
        #creating a thread so you can receive and send messages at the same time.
        #the sending process will work at the background
        received_msg = client_socket.recv(1024).decode()
        if received_msg:
            print(received_msg)
            if received_msg != QUIT_MSG:
                print(messages)
                if not(received_msg in messages):
                    output.insert(tk.END, f"guest: {received_msg} \n")
                    output.tag_add("here", "2.0", END)
                    output.tag_config("here", foreground="blue")
                messages = []
                print(messages)
            else:
                guest_quit = True
                output.insert(tk.END, QUIT_MSG)
                but['state'] = tk.DISABLED
                client_socket.close()
                break
        else:
            break        


#tkinter styling part
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to leave the chat?"):
        if not(guest_quit):
            client_socket.send(bytes(QUIT_MSG, encoding="utf-8"))
        client_socket.close()
        wn.destroy()


wn = Tk()
wn.title("Guest")
wn.geometry('520x445')
wn.resizable(width=False, height=False)
wn.configure(background='cyan2')

C = Canvas(wn, bg="blue", height=100, width=300)
filename = PhotoImage(file = "bg_pic2.jpg")
background_label = Label(wn, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

input_entry = Entry(wn, width=70)
input_entry.place(x=20, y=405)

output = tk.Text(wn, width = 60, height = 22, bd = 2)
output.place(x=20,y=10)




but = Button(wn, text="Send", bd=3, command=send_msg, background ="#C0C0C0", activebackground = "#E0E0E0")
but.place(x=460,y=400)

receive_thread = threading.Thread(target = receive_msg, daemon=True)
receive_thread.start()

def key_listener():
    with Listener(on_press=lambda key: send_msg() if str(key) == "Key.enter" else print("")) as listener:
        listener.join()

listener_thread =threading.Thread(target=key_listener, daemon = True)
listener_thread.start()


wn.protocol("WM_DELETE_WINDOW", on_closing)

tk.mainloop()
