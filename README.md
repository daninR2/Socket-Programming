# CP372 – Socket Programming Assignment (Fall 2025) - Daniyal Naqvi & Omar Hamza

## 📌 Overview
This project implements a simple **client-server communication system** using Python sockets (TCP).  
The goal is to demonstrate networking concepts such as multi-client handling, message exchange, and file transfers.

The project consists of:
- `Server.py` – runs a multi-threaded server that handles multiple clients.
- `Client.py` – connects to the server and enables interaction via a CLI.
- `Report.pdf` – documentation of the implementation, challenges, and improvements.

---

## ⚙️ Features
- **Multi-client server:** Handles up to 3 concurrent clients.
- **Automatic client naming:** Clients are assigned names in the format `Client01`, `Client02`, etc.
- **Message exchange:** Clients send messages to the server, which echoes them back with `ACK`.
- **Status check:** Clients can send `status` to retrieve active session details.
- **Graceful exit:** Clients can disconnect using the `exit` command, freeing resources.
- **File repository access:**
  - `list` → Lists available files on the server.
  - `<filename>` → Requests file transfer from the server.
- **Error handling:** Handles invalid file requests and disconnections properly.

---

## 🚀 How to Run
### 1. Start the server
```bash
python Server.py
