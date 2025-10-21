"""
-------------------------------------------------------
Server.
-------------------------------------------------------
Author:  Daniyal Naqvi & Omar Hamza
ID:      169057430 & 169073034
Email:   naqv7430@wlu.ca & hamz3034@wlu.ca
__updated__ = "2025-10-20"
-------------------------------------------------------
"""

#Imports
import socket
import threading
import os
from datetime import datetime


# Server Configuration
HOST = '127.0.0.1'        # Localhost
PORT = 12345              # Port
MAX_CLIENTS = 3           # Max clients that are allowed
REPO_DIR = os.path.join(os.path.dirname(__file__), 'server_list') # Folder where files are stored

# Global Variables
client_cache = {}         # Stores the clients connection info
client_count = 0          # Number of the connected clients
lock = threading.Lock()   # Makes sure the thread-safe updates

# Handle Client Connection
def handle_client(conn, addr, client_name):
    global client_count
    #Prints the connection/disconnection with the clients name and time of connection
    print(f"[NEW CONNECTION] {client_name} connected from {addr}")
    client_cache[client_name] = {
        'connected': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'disconnected': None
    }
    #Try except to make sure program doesn't crash
    try:
        while True:
            msg = conn.recv(1024).decode()  # Receive the message from the client
            if not msg:
                break  #Break when client disconnects

            #Breaks when client exits
            if msg.lower() == 'exit':
                conn.send("Goodbye!".encode())
                break
            #Shows the status of the connections
            elif msg.lower() == 'status':
                # Return current client cache
                status_info = "\n".join([f"{c}: {v}" for c, v in client_cache.items()])
                conn.send(status_info.encode())
            #Shows the list of files in the server_list
            elif msg.lower() == 'list':
                print(f"[DEBUG] 'list' command received from {client_name}")
                #Checks if the file path exisits in the repository
                if not os.path.exists(REPO_DIR):
                    conn.send("Repository folder not found!".encode())
                else:
                    files = os.listdir(REPO_DIR)
                    print("[DEBUG] Files in repo:", files)
                    if not files:
                        conn.send("No files found in repository.".encode())
                    else:
                        conn.send("\n".join(files).encode())

            elif os.path.isfile(os.path.join(REPO_DIR, msg)):
                # Sends the file data to the client
                with open(os.path.join(REPO_DIR, msg), 'rb') as f:
                    data = f.read()
                    conn.sendall(data)
                print(f"[FILE SENT] {msg} sent to {client_name}")

            else:
                #Print ACK after the clients message 
                conn.send((msg + " ACK").encode())

    except Exception as e:
        print(f"[ERROR] Connection with {client_name} ended unexpectedly: {e}")

    finally:
        #Disconnect
        conn.close()
        print(f"[DISCONNECTED] {client_name}")
        with lock:
            client_cache[client_name]['disconnected'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            client_count -= 1


# -----------------------------
# Start the Server
# -----------------------------
def start_server():
    global client_count

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[LISTENING] Server running on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        with lock:
            if client_count >= MAX_CLIENTS:
                # Reject extra clients
                conn.send("Server full. Try again later.".encode())
                print(f"[REJECTED CONNECTION] from {addr} — server full")
                conn.close()
                continue

            # Accept new client
            client_count += 1
            client_name = f"Client{client_count:02d}"

        # Start a new thread for the client
        thread = threading.Thread(target=handle_client, args=(conn, addr, client_name))
        thread.start()


# Run the Server
if __name__ == "__main__":
    #Print a starting line for clarity
    print("[STARTING] Server is starting...")
    start_server()
