import socket
import threading
import json
from game.tank import Tank

class Server:
    def __init__(self, host="192.168.117.206", port=1234):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))
        self.tanks = []
        self.lock = threading.Lock()

    def start(self):
        self.sock.listen()
        print(f"Server started on {self.host}:{self.port}")

        # Server loop
        while True:
            # Wait for a new connection
            conn, addr = self.sock.accept()
            print(f"New connection from {addr}")

            # Create a new tank and add it to the collection
            with self.lock:
                tank = Tank(50, 350)
                self.tanks.append((tank, conn))

            # Start a new thread to handle updates from the client
            client_thread = threading.Thread(target=self.handle_client, args=(conn, tank))
            client_thread.start()

    def stop(self):
        self.sock.close()
        print("Server stopped")

    def handle_client(self, conn, addr):
        with self.lock:
            tank = Tank(50, 350)
            self.tanks.append(tank)
            client_id = len(self.tanks)

        print(f"New connection from {addr}, assigned ID {client_id}")

        while True:
            data = conn.recv(1024).decode()
            if not data:
                print(f"Client {client_id} disconnected")
                with self.lock:
                    self.tanks.remove(tank)
                break

            if data.startswith("UPDATE"):
                _, tank_id, x_str, y_str = data.split()
                tank_id = int(tank_id)
                x = float(x_str)
                y = float(y_str)
                print(f"Updating tank {tank_id} position to ({x}, {y})")

                # Find the tank with the specified ID and update its position
                with self.lock:
                    for t in self.tanks:
                        if t.id == tank_id:
                            t.x = x
                            t.y = y
                            break

        conn.close()