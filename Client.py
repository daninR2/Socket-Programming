import socket

HOST = '127.0.0.1'
PORT = 12345

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print(f"Connected to {HOST}:{PORT}")

    while True:
        msg = input("Enter message: ")
        client.send(msg.encode())
        data = client.recv(4096)
        print("Server:", data.decode())

        if msg.lower() == 'exit':
            break

    client.close()

if __name__ == "__main__":
    start_client()
