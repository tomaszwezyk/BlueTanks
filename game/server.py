import socket
import time
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

        # Start the thread for sending updates to clients
        send_updates_thread = threading.Thread(target=self.send_tank_updates)
        send_updates_thread.start()

        # Server loop
        while True:
            # Wait for a new connection
            conn, addr = self.sock.accept()
            print(f"New connection from {addr}")

            # Create a new tank and add it to the collection
            with self.lock:
                tank = Tank(50, 350)
                tank.connection = conn
                #self.tanks.append(tank)

            # Start a new thread to handle updates from the client
            client_thread = threading.Thread(target=self.handle_client, args=(conn, tank))
            client_thread.start()

    def stop(self):
        self.sock.close()
        print("Server stopped")

    def handle_client(self, conn, addr):
        #with self.lock:
        #    tank = Tank(50, 350)
        #    tank.connection = conn
        #    self.tanks.append(tank)
            #client_id = len(self.tanks)

        print(f"New connection from {addr}")

        while True:
            data = conn.recv(1024).decode()
            if not data:
                break

            if data.startswith("UPDATE"):
                _, tank_id, x_str, y_str = data.split()
                x = float(x_str)
                y = float(y_str)
                print(f"Updating tank {tank_id} position to ({x}, {y})")

                found = False
                # Find the tank with the specified ID and update its position
                for t in self.tanks:
                    if str(t.uuid) == tank_id:
                        t.x = x
                        t.y = y
                        found = True
                        break
                if not found:
                    print(f"Adding new Tank: "+str(tank_id))
                    t = Tank(x,y,tank_id)
                    t.connection = conn
                    self.tanks.append(t)

        conn.close()

    def send_tank_updates(self):
        while True:
            # Build a message containing the positions of all tanks
            tanks_str = ""
            with self.lock:
                for tank in self.tanks:
                    tanks_str += f"UPDATE {tank.uuid} {tank.x} {tank.y}\n"
            message = f"TANKS\n{tanks_str}\n"

            # Send the message to all connected clients
            for tank in self.tanks:
                    #print("sending TANKS positions to"+ str(tank.uuid))
                    tank.connection.sendall(message.encode())
                #except:
                    # If there is an error receiving the data or updating the position, remove the connection from the list
                #    self.tanks.remove((tank))
                #    print("Client disconnected")

            # Wait a bit before sending the next update
            time.sleep(0.1)