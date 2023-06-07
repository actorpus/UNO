import json
import msvcrt
import socket
import os
import sys
import drawingtest

try:
    os.get_terminal_size()
except OSError:
    print("Probably not in terminal... restarting now")
    com = f"start \"{sys.executable}\" \"{sys.argv[0]}\""
    print("running command:", com)
    os.system(com)
    sys.exit(-2)


# s -> c game state change {
#    your_hand: ["b+2", "b4", "y4", "rB"]
#    player_hands: {
#        "dan": 4
#        "jimmy": 69
#    }
#    top_card: "b4"
#    deck_size: 4
#    draw_size: 68
# }
# c -> s yeah fam i gotchu
#
# s -> c your go
# c -> s i choose y+2
# s -> c chill wait               *
#
# s -> c your go
# c -> s nah mate i pickup
# s -> c chill wait
#
# *)
# s -> c Nah fam thats wrong
# c -> s Ight fam i gotcha i choose b+2
# s - > chill wait


IP = "192.168.56.1"
PORT = 31875
CLIENT_VERSION = "v0.0.1"
NAME = input("name")
CLIENT_UPDATE_FREQUENCY = 0.2


class UnoClient:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((IP, PORT))

        self.send_magic_start()

        self.lobby_waiting = ["Nobody :("]
        self.running = True
        self.in_game = False

    def send_magic_start(self):
        self.server.send(len(CLIENT_VERSION).to_bytes(1, 'big'))
        self.server.send(CLIENT_VERSION.encode())
        self.server.send(len(NAME).to_bytes(1, 'big'))
        self.server.send(NAME.encode())

    def handle_packet(self, packet):
        if packet == b"PING":
            self.server.send(b"PONG")

        if packet == b"PGUD":  # pre game update
            update = int.from_bytes(self.server.recv(2), 'big')
            update = self.server.recv(update).decode()
            update = json.loads(update)

            self.lobby_waiting = update

    def run(self):
        while self.running:
            self.server.settimeout(CLIENT_UPDATE_FREQUENCY)
            try:
                data = self.server.recv(4)

            except TimeoutError:
                self.server.settimeout(None)

            else:
                self.server.settimeout(None)
                if data:
                    self.handle_packet(data)

            if msvcrt.kbhit():  # key waiting in que
                key = msvcrt.getch()

                if key == b'\x1b':
                    self.running = False

                elif key == b'y':
                    ...

                elif key == b' ' and not self.in_game and len(self.lobby_waiting) > 1:
                    ...

            scr_w, scr_h = os.get_terminal_size()
            if scr_w < 64 or scr_h < 16:
                print("\033[31mResize!\033[0m Window to small to render correctly, please resize.")
                continue

            print()
            print(" Uno!" + " " * (scr_w - 6 - len(CLIENT_VERSION)) + CLIENT_VERSION)
            print()
            print(" In lobby with:")

            for member in self.lobby_waiting:
                print(" -", member)

            print("\n" * (scr_h - 8 - len(self.lobby_waiting)))

            grey = "\033[90m"
            print(f" [ESC] Close  {grey}[y] Chat\033[0m  {grey if len(self.lobby_waiting) <= 1 else ''}[SPACE] Start Game\033[0m")
            print(" " * (scr_w - 12) + "웃 ©Alex&Dan")


if __name__ == '__main__':
    drawingtest.main()

    game = UnoClient()
    game.run()
