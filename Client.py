import socket
import os

HOST = '127.0.0.1'
PORT = 12345

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print(f"Connected to {HOST}:{PORT}")

    # --- Check for "Server full" message immediately after connecting ---
    client.settimeout(1.0)  # Wait briefly to see if server sends anything
    try:
        initial_msg = client.recv(1024).decode()
        if "Server full" in initial_msg:
            print(initial_msg)
            client.close()
            return  # Exit gracefully
    except socket.timeout:
        pass  # No message means connection is fine
    client.settimeout(None)  # Back to normal blocking mode

    # --- Main loop ---
    while True:
        msg = input("Enter message: ")
        client.send(msg.encode())

        if msg.lower() == 'exit':
            data = client.recv(1024).decode()
            print("Server:", data)
            break

        # Receive data from server
        data = client.recv(4096)

        # If user asked for a file (e.g., filename.txt)
        if '.' in msg:
            filename = "downloaded_" + msg
            with open(filename, 'wb') as f:
                f.write(data)
            print(f"File '{msg}' downloaded and saved as '{filename}'")
        else:
            # Normal text reply
            print("Server:", data.decode())

    client.close()

if __name__ == "__main__":
    start_client()
