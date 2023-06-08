import json
import msvcrt
import socket
import os
import sys
import time

import drawingtest

try:
    os.get_terminal_size()
except OSError:
    print("Probably not in terminal... restarting now")
    com = f"start \"{sys.executable}\" \"{sys.argv[0]}\""
    print("running command:", com)
    os.system(com)
    sys.exit(-2)


# IP = "192.168.56.1"
# PORT = 31875
CLIENT_VERSION = "v0.0.2"
NAME = input("name")
CLIENT_UPDATE_FREQUENCY = 0.2


class UnoClient:
    def __init__(self):
        self.running = True
        self.in_game = False
        self.lobby_waiting = ["Alex", NAME, "Joe (sucks at uno)"]

    def render_menu(self):
        scr_w, scr_h = os.get_terminal_size()
        if scr_w < 64 or scr_h < 16:
            print("\033[31mResize!\033[0m Window to small to render correctly, please resize.")
            return

        print()
        print(" Uno!" + " " * (scr_w - 6 - len(CLIENT_VERSION)) + CLIENT_VERSION)
        print()
        print(" In lobby with:")

        for member in self.lobby_waiting:
            print(" -", member)

        print("\n" * (scr_h - 8 - len(self.lobby_waiting)))

        grey = "\033[90m"
        print(f" [ESC] Close  {grey}[y] Chat\033[0m  {grey if len(self.lobby_waiting) <= 1 else ''}[SPACE] Start Game\033[0m")
        print(" " * (scr_w - 10) + "©Alex&Dan")

    def render_board(self):
        scr_w, scr_h = os.get_terminal_size()
        if scr_w < 64 or scr_h < 16:
            print("\033[31mResize!\033[0m Window to small to render correctly, please resize.")
            return

        print()
        print(" Uno!" + " " * (scr_w - 6 - len(CLIENT_VERSION)) + CLIENT_VERSION)
        print()

        print("\n" * (scr_h - 7))

        grey = "\033[90m"
        print(f" [ESC] Close  {grey}[y] Chat\033[0m  {grey if len(self.lobby_waiting) <= 1 else ''}[SPACE] Start Game\033[0m")
        print(" " * (scr_w - 10) + "©Alex&Dan")

    def run(self):
        while self.running:
            time.sleep(CLIENT_UPDATE_FREQUENCY)

            if msvcrt.kbhit():  # key waiting in que
                key = msvcrt.getch()

                if key == b'\x1b':
                    self.running = False

                elif key == b'y':
                    ...

                elif key == b' ' and not self.in_game:
                    self.in_game = True

            if self.in_game:
                self.render_board()
            else:
                self.render_menu()


if __name__ == '__main__':
    drawingtest.main()

    game = UnoClient()
    game.run()