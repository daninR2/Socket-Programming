import socket
import threading
import os
from datetime import datetime

# Basic setup
HOST = '127.0.0.1'  # Localhost (your computer)
PORT = 12345
MAX_CLIENTS = 3
REPO_DIR = './server_list'

client_cache = {}  # Stores info about connected clients
client_count = 0
lock = threading.Lock()  # Prevents data conflicts between threads

def handle_client(conn, addr, client_name):
    """Handle messages from a connected client."""
    print(f"[NEW CONNECTION] {client_name} connected from {addr}")
    client_cache[client_name] = {'connected': datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'disconnected': None}

    while True:
        try:
            msg = conn.recv(1024).decode()
            if not msg:
                break

            if msg.lower() == 'exit':
                conn.send("Goodbye!".encode())
                break
            elif msg.lower() == 'status':
                status_info = "\n".join([f"{c}: {v}" for c, v in client_cache.items()])
                conn.send(status_info.encode())
            elif msg.lower() == 'list':
                print("[DEBUG] Received 'list' request from client")
                files = os.listdir(REPO_DIR)
                print("[DEBUG] Files in repo:", files)
                conn.send("\n".join(files).encode())
            elif os.path.isfile(os.path.join(REPO_DIR, msg)):
                with open(os.path.join(REPO_DIR, msg), 'rb') as f:
                    data = f.read()
                    conn.sendall(data)
            else:
                conn.send((msg + " ACK").encode())
        except:
            break

    # Disconnect
    client_cache[client_name]['disconnected'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn.close()
    print(f"[DISCONNECTED] {client_name}")
    with lock:
        global client_count
        client_count -= 1

def start_server():
    """Main server loop."""
    global client_count
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[LISTENING] Server running on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        with lock:
            if client_count >= MAX_CLIENTS:
                conn.send("Server full. Try again later.".encode())
                conn.close()
                continue
            client_count += 1
        client_name = f"Client{client_count:02d}"
        threading.Thread(target=handle_client, args=(conn, addr, client_name)).start()

if __name__ == "__main__":
    print("[STARTING] Server is starting...")
    start_server()
