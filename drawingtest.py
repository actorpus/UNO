import os
import random
import sys
import time

if __name__ == '__main__':
    try:
        os.get_terminal_size()
    except OSError:
        print("Probably not in terminal... restarting now")
        com = f"start \"{sys.executable}\" \"{sys.argv[0]}\""
        print("running command:", com)
        os.system(com)
        sys.exit(-2)


def main():
    scr_w, scr_h = os.get_terminal_size()

    disp = [False for _ in range(scr_w * scr_h)]
    leftovers = [_ for _ in range(scr_w * scr_h)]
    print("\033[32m", end="")
    for _ in range(scr_w * scr_h // 2):
        p = random.choice(leftovers)

        disp[p] = True

        o = ""

        for _ in disp:
            if _:
                o += str(random.randint(0, 1))
                # o += "#"
            else:
                o += " "

        print(end=o, flush=True)

        # time.sleep(0.01)
    print("\033[0m", end="")

    UPSIDEDOWN_NUMBERS = "0", "|", "↊", "↋", "ߤ", "5", "9", "L", "8", "6"

    def draw_card(color: int, card: int, card_type: int) -> str:
        if not (40 <= color <= 44):
            raise "bad color"

        if card_type == 0:
            top = f" {card}"
            bottom = f"{UPSIDEDOWN_NUMBERS[card]} "

        return f"""
    █\033[{color}m▀▀▀▀▀▀▀▀▀▀▀\033[0m█
    █\033[{color}m \033[1m{top}\033[0;{color}m        \033[0m█
    █\033[{color}m      ▄▄▄▄ \033[0m█
    █\033[{color}m   ▄\033[47m▀▀    █\033[0m█
    █\033[{color}m ▄\033[47m▀\033[47;32m      \033[47;37m▄\033[{color}m▀\033[0m█
    █\033[{color}m▄\033[47m▀\033[47;32m      \033[47;37m▄\033[{color}m▀ \033[0m█
    █\033[{color}m█\033[47m    ▄▄\033[{color}m▀   \033[0m█
    █\033[{color}m ▀▀▀▀      \033[0m█
    █\033[{color}m        \033[1m{bottom}\033[0;{color}m \033[0m█
    █\033[{color}m▄▄▄▄▄▄▄▄▄▄▄\033[0m█
    """.strip()

    for _ in range(41, 45):
        for __ in range(0, 10):
            print(_, __)
            print(draw_card(_, __, 0))
            time.sleep(0.02)

    time.sleep(0.1)

    # print("""
    # █▀▀▀▀▀▀▀█
    # █ █▀▀▀▀▀▀█
    # █ █ █▀▀▀▀▀▀▀█
    # █ █ █       █
    # █ █ █       █
    # █ █ █  X5   █
    # █▄█ █       █
    #   █▄█       █
    #     █▄▄▄▄▄▄▄█
    # """)

    # print("""
    # █▀▀▀▀█
    # █ █▀▀▀▀█
    # █ █ █▀▀▀▀█
    # █ █ █    █
    # ▀▀█ █    █
    #   ▀▀█    █
    #     ▀▀▀▀▀▀
    # """)

    NUMBERS = [
        "█  \n█  \n▀  "
        "▀▀█\n█▀▀\n▀▀▀",
        "▀▀█\n▀▀█\n▀▀▀",
        "█ █\n▀▀█\n  ▀",
        "█▀▀\n▀▀█\n▀▀▀",
        "█▀▀\n█▀█\n▀▀▀",
        "▀▀█\n  █\n  ▀",
        "█▀█\n█▀█\n▀▀▀",
        "█▀█\n▀▀█\n▀▀▀"
    ]

    def draw_cards(nbr: int) -> str:
        if nbr >= 10:
            return f"█▀▀▀▀▀█    \n█ █▀▀▀▀▀█  \n█ █ █▀▀▀▀▀█\n█ █ █     █\n▀▀█ █     █\n  ▀▀█     █\n    ▀▀▀▀▀▀▀"

        elif nbr >= 3:
            h1, h2, h3 = NUMBERS[nbr - 2].split("\n")

            return f"█▀▀▀▀▀█    \n█ █▀▀▀▀▀█  \n█ █ █▀▀▀▀▀█\n█ █ █ {h1} █\n▀▀█ █ {h2} █\n  ▀▀█ {h3} █\n    ▀▀▀▀▀▀▀"

        elif nbr == 2:
            return "           \n  █▀▀▀▀▀█  \n  █ █▀▀▀▀▀█\n  █ █ ▀▀█ █\n  █ █ █▀▀ █\n  ▀▀█ ▀▀▀ █\n    ▀▀▀▀▀▀▀"

        elif nbr == 1:
            return "           \n           \n    █▀▀▀▀▀█\n    █ █   █\n    █ █   █\n    █ ▀   █\n    ▀▀▀▀▀▀▀"

        else:
            return "           \n           \n           \n           \n           \n           \n          "

    c_w, c_h = os.get_terminal_size()

    for h in reversed(list(range(15))):
        print(f"Dans:   ({str(h):2s})")
        print("           ")
        print(draw_cards(h))
        print("\n" * (c_h - 11))
        time.sleep(0.06)
