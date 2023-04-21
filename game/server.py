import socket
import threading
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
                self.tanks.append(tank)

            # Handle updates from client
            threading.Thread(target=self.handle_client, args=(conn, tank)).start()

    def stop(self):
        self.sock.close()
        print("Server stopped")

    def handle_client(self, conn, tank):
        # Receive and apply updates to tank position
        while True:
            data = conn.recv(1024)
            if not data:
                break
            x, y = data.decode().split(",")
            tank.x = int(x)
            tank.y = int(y)

        # Remove tank from collection and close connection
        with self.lock:
            self.tanks.remove(tank)
        conn.close()
