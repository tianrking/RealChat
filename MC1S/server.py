import socket
import threading

# Server settings
server_ip = '0.0.0.0'  # Listening on all network interfaces
server_port = 12346
clients = []

def client_thread(conn, addr):
    print(f"New connection from {addr}")
    while True:
        try:
            message = conn.recv(1024).decode('utf-8')
            if message:
                print(f"Message from {addr}: {message}")
                # Send message along with the sender's address
                broadcast(f"{addr[0]}:{addr[1]} says: {message}", conn)
            else:
                remove(conn)
        except:
            continue

def broadcast(message, connection):
    for client in clients:
        if client != connection:
            try:
                client.send(message.encode('utf-8'))
            except:
                remove(client)

def remove(connection):
    if connection in clients:
        clients.remove(connection)

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen(100)

    while True:
        conn, addr = server_socket.accept()
        clients.append(conn)
        threading.Thread(target=client_thread, args=(conn, addr)).start()

    server_socket.close()

if __name__ == "__main__":
    main()

