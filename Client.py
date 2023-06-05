import json
import socket
import os
import sys

try:
    os.get_terminal_size()
except OSError:
    print("Probably not in terminal... restarting now")
    com = f"start \"{sys.executable}\" \"{sys.argv[0]}\""
    print("running command:", com)
    os.system(com)
    sys.exit(-2)

# connect to server
# wait
#
# c -> s eyo fam my named "dan"
# s -> c eyo fam i gotchu
#
# s -> c pre game change {
#   waiting_players: [alex, dan]
#
#
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
# s -> c you there brudda?
# c -> s yeah mans i here
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


IP = "169.254.217.82"
PORT = 31875
CLIENT_VERSION = "v0.0.1"
NAME = input("name")
CLIENT_UPDATE_FREQUENCY = 0.2


def handle_packet(packet):
    global lobby_waiting

    if packet == b"PING":
        server.send(b"PONG")

    if packet == b"PGUD":  # pre game update
        update = int.from_bytes(server.recv(2), 'big')
        update = server.recv(update).decode()
        update = json.loads(update)

        lobby_waiting = update


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((IP, PORT))

server.send(len(CLIENT_VERSION).to_bytes(1, 'big'))
server.send(CLIENT_VERSION.encode())
server.send(len(NAME).to_bytes(1, 'big'))
server.send(NAME.encode())


lobby_waiting = ["Nobody :("]


while True:
    server.settimeout(CLIENT_UPDATE_FREQUENCY)
    try:
        data = server.recv(4)

    except TimeoutError:
        server.settimeout(None)

    else:
        server.settimeout(None)
        if data:
            handle_packet(data)

    scr_w, scr_h = os.get_terminal_size()
    if scr_w < 32 or scr_h < 16:
        print("\033[31mResize!\033[0m Window to small to render correctly, please resize.")
        continue

    print("Uno!" + " " * (scr_w - 4 - len(CLIENT_VERSION)) + CLIENT_VERSION)
    print()
    print("In lobby with:")

    for member in lobby_waiting:
        print("-", member)

    print("\n" * (scr_h - 5 - len(lobby_waiting)))
