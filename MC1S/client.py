import socket
import threading

# Replace with the server's IP address and port
server_ip = '127.0.0.1'  # Server IP
server_port = 12346  # Server Port

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

def receive():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except:
            print("Connection was lost!")
            client_socket.close()
            break

def write():
    while True:
        message = f'{input("")}'  # Removed the 'Client:' prefix for custom naming
        client_socket.send(message.encode('utf-8'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

