"""
-------------------------------------------------------
Client.
-------------------------------------------------------
Author:  Daniyal Naqvi & Omar Hamza
ID:      169057430 & 169073034
Email:   naqv7430@wlu.ca & hamz3034@wlu.ca
__updated__ = "2025-10-20"
-------------------------------------------------------
"""

#Imports
import socket
import os

#Set local host and port
HOST = '127.0.0.1'
PORT = 12345

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print(f"Connected to {HOST}:{PORT}")

    #Check if the server is full
    client.settimeout(1.0)  # Wait  to see if server sends anything
    try:
        initial_msg = client.recv(1024).decode()
        #Print message if the server is full
        if "Server full" in initial_msg:
            print(initial_msg)
            client.close()
            return  #Exit 
    except socket.timeout:
        pass  #Pass if the server is open
    client.settimeout(None) 

    #Main loop
    while True:
        msg = input("Enter message: ")
        client.send(msg.encode())

        if msg.lower() == 'exit':
            data = client.recv(1024).decode()
            print("Server:", data)
            break

        # Receive data from the server
        data = client.recv(4096)

        #If user asked for a file (e.g., Daniyal.txt)
        if '.' in msg:
            filename = "downloaded_" + msg
            with open(filename, 'wb') as f:
                f.write(data)
            print(f"File '{msg}' downloaded and saved as '{filename}'")

            #Try to read and display the file contents (for text files)
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    contents = f.read()
                print(contents)
            except Exception as e:
                #Print the error trapped message
                print("(File saved but not printable — likely binary data)")

        else:
            try:
                print("Server:", data.decode())
            except UnicodeDecodeError:
                print("(Received non-text data)")

    client.close()

if __name__ == "__main__":
    start_client()
