import socket
import threading

#the port of communication
QUIT_MSG = "-- guest has DISCONNECTED --"
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostname = socket.gethostbyname(socket.gethostname())
port = 5050
server_socket.bind((hostname, port))
clients_sockets = []
server_socket.listen(5)
print(f"server {hostname}: listening on port {port} ....")

def clients_connections_handler(client_socket, address):
    global clients_sockets
    while True:
        msg = client_socket.recv(1024)
        if (msg) and (msg.decode() != QUIT_MSG):
            print(f"{address}: {msg.decode()} ")
            for sock in clients_sockets:
                sock.send(msg)
        #when connections are  done
        else:
            clients_sockets.remove(client_socket)
            for sock in clients_sockets:
                sock.send(bytes(QUIT_MSG, encoding="utf-8"))
                print("disconnection detected")
            client_socket.close()
            server_socket.close()
            break


while True:
    client_socket, address = server_socket.accept()
    print(f"{address[1]}: is connected...")
    clients_sockets.append(client_socket)

    #creaing a thread for each client_socket connection so many clients will be able to connect at once
    client_thread = threading.Thread(target = clients_connections_handler, args=(client_socket,address))
    #setting a parameter that allows to stop running the program even a thread is still processing
    client_thread.daemon = True
    #starting the thread
    client_thread.start()




