import json
import socket
import threading
import time
import datetime
import uno

CLIENT_UPDATE_FREQUENCY = 0.1
CLIENT_HEART_BEAT = 5
CLIENT_TTL = 30  # time before abandoning
SERVER_PORT = 31875
SERVER_VERSION = "v0.0.2"


class MasterServer:
    def __init__(self):
        self.clients: list[Client] = []
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.self_ip = socket.gethostbyname(socket.gethostname())
        print(" [ \033[32mMS    \033[0m ] Discovered my ip.", self.self_ip)

        self.game_running = False
        self.current_game: uno.Game | None = None

    def run(self):
        print(" [ \033[32mMS    \033[0m ] Starting server on port", SERVER_PORT)
        self.server_sock.bind((self.self_ip, SERVER_PORT))
        self.server_sock.listen(16)

        while True:
            client, address = self.server_sock.accept()
            print(f" [ \033[32mMS    \033[0m ] New connection from {address}")

            port = f"{str(address[1]):5s}"

            client_o = Client(client, port, self)
            client_o.start()

            time.sleep(0.5)

            self.clients.append(client_o)
            self.update_clients_pregame()

    def update_clients_pregame(self):
        for client in self.clients:
            client.send_pregame_update()

    def start_game(self):
        if self.game_running: return
        self.game_running = True

        self.current_game = uno.Game(
            *[
                client.name for client in self.clients
            ]
        )

        for i, client in enumerate(self.clients):
            client.send_game_update(i)


class Client(threading.Thread):
    def __init__(self, sock, port, master_server):
        super(Client, self).__init__()
        self.port = port
        self.alive_bookmark = time.time()
        self.last_ping_send = time.time()
        self.sock: socket.socket = sock
        self.alive = True
        self.name = "N00B"
        self.server: MasterServer = master_server
        self.lock = threading.Lock()

    def send_pregame_update(self):
        print(f" [ \033[34mC{self.port}\033[0m ] Updating lobby information")
        self.sock.send(b"PGUD")
        data = json.dumps([_.name for _ in self.server.clients]).encode()

        self.sock.send(len(data).to_bytes(2, 'big'))
        self.sock.send(data)

        self.sock.send(int.to_bytes(
            0b00000000,
            1, 'big'))

    def send_game_update(self, i):
        status = self.server.current_game.get_status(i)



    def death_spiral(self):
        self.alive = False
        self.sock.close()
        self.server.clients.remove(self)
        self.server.update_clients_pregame()
        print(f" \033[31m[ \033[34mC{self.port}\033[0m \033[31m]\33[0m Closing thread")

    def handle_packet(self, packet):
        if packet == b"PONG":
            self.alive_bookmark = time.time()
            print(f" [ \033[34mC{self.port}\033[0m ] Ponged")
            return

        elif packet == b"STRT":
            print(f" [ \033[34mC{self.port}\033[0m ] Started the game!")
            self.server.start_game()

    def run(self) -> None:
        print(f" [ \033[34mC{self.port}\033[0m ] Client Proses alive")

        version_length = int.from_bytes(self.sock.recv(1), 'big')
        version = self.sock.recv(version_length).decode()

        if version != SERVER_VERSION:
            print(f" [ \033[34mC{self.port}\033[0m ] Client is using the wrong version")
            return self.death_spiral()

        name_length = int.from_bytes(self.sock.recv(1), 'big')

        if name_length > 10:
            print(f" [ \033[34mC{self.port}\033[0m ] Client chose a stupid name (length)")
            return self.death_spiral()

        self.name = self.sock.recv(name_length).decode()
        print(f" [ \033[34mC{self.port}\033[0m ] Chose the name \"{self.name}\"")

        while self.alive:
            self.sock.settimeout(CLIENT_UPDATE_FREQUENCY)
            try:
                data = self.sock.recv(4)
            except TimeoutError:
                self.sock.settimeout(None)
            except ConnectionResetError:
                print(f" [ \033[34mC{self.port}\033[0m ] Connection reset.")
                return self.death_spiral()
            except ConnectionAbortedError:
                print(f" [ \033[34mC{self.port}\033[0m ] Connection aborted.")
                return self.death_spiral()
            else:
                self.sock.settimeout(None)
                if data:
                    self.handle_packet(data)

            t = time.time()

            if t - self.alive_bookmark > CLIENT_HEART_BEAT and t - self.last_ping_send > 2:
                print(f" [ \033[34mC{self.port}\033[0m ] Pinging")
                self.sock.send(b"PING")
                self.last_ping_send = time.time()

            if t - self.alive_bookmark > CLIENT_TTL:
                formatted_time = datetime.datetime.fromtimestamp(t).strftime('%H:%M:%S:%f')[:-3]
                print(f" [ \033[34mC{self.port}\033[0m ] Time of death, {formatted_time}")
                return self.death_spiral()


if __name__ == '__main__':
    server = MasterServer()
    server.run()
