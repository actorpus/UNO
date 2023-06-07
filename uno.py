suits = ["R", "Y", "G", "B", "M"]
pips = []
for i in range(0, 10):
    pips.append(str(i))
pips.extend(["b", "r", "p", "s"])

deck = []
for i in range(0, 4):
    for j in range(1, 13):
        for k in range(0, 2):
            deck.append(str(suits[i]) + str(pips[j]))
    deck.append(str(suits[i]) + str(pips[0]))
    for j in range(12, 14):
        deck.append(str(suits[4]) + str(pips[j]))


# get_status(player_number) -> {your_hand: ["R3"...

# player_move(player_number, card) -> None

NOT_YOUR_GO = 1
BAD_MOVE = 2
VALID_MOVE = 3


def player_safe_return(i: int):
    return max(0, min(10, i))


class Game:
    def __init__(
            self,
            *player_names: str,
            starting_hand_size=7,
    ):
        self.players = player_names
        number_of_players = len(player_names)

        self.hands: list[list[str]] = [
            [] for _ in range(number_of_players)
        ]

        self.deck = self.deck_fill()

        for _ in range(number_of_players):
            self.players.append(Player())

    def get_status(self, player_number):
        self.hand =0

        player_status = {
            "your_hand": self.hands[player_number],
            "player_hands": player_hands,
            "top_card": self.cards_in_play[0],
            "deck_size": player_safe_return(len(self.deck)),
            "cards_in_play_size": player_safe_return(len(self.cards_in_play)),
            "current_turn": self.players[self.current_player],
            "current_pickup_amount": self.current_pickup_amount

        }

        return player_status

    def validate_move(self, player_number, card):
        if card[1] in ["P", "s"]:
            card = "M" + card[1]

        # not your go
        if player_number != self.current_player:
            return NOT_YOUR_GO
        if card not in self.hands[self.current_player]:
            return BAD_MOVE
        # if card[1] == "P" and "MP" not in self.hands[self.turns[0]]:
        if card[1] == "P" and "MP" not in self.hands[self.current_player]:
            return BAD_MOVE
        if card[1] == "s" and "Ms" not in self.hands[self.current_player]:
            return BAD_MOVE

        # valid move
        if card[0] == self.cards_in_play[0][0] and self.current_pickup_amount == 0:
            return VALID_MOVE
        if card[1] == self.cards_in_play[0][1]:
            return VALID_MOVE
        if card[1] == "s" and self.current_pickup_amount == 0:
            return VALID_MOVE
        if card[1] == "P":
            return VALID_MOVE
        if card[1] == "p" and card[0] == self.cards_in_play[0][0]:
            return VALID_MOVE
        # bad move
        # Ms MP
        # Bs BP
        return BAD_MOVE

    # TODO
    def is_game_over(self):
        return False

    def refresh_deck(self):
        self.deck = self.cards_in_play[1:].copy()
        self.cards_in_play = self.cards_in_play[:1]

        random.shuffle(self.deck)

    def player_move(self, card):
        # Ms Rs Ys Gs Bs
        # MP RP YP GP BP
        if card[1] == "s":
            used_card = "Ms"
        elif card[1] == "P":
            used_card = "MP"
        else:
            used_card = card
        self.cards_in_play.insert(0, card)
        self.hands[self.current_player].remove(used_card)
        if card[1] == "p":
            self.current_pickup_amount += 2
        if card[1] == "P":
            self.current_pickup_amount += 4
        if card[1] == "r" and len(self.players) > 2:
            self.turns.reverse()
        else:
            for i in range(0, 2):
                self.turns.append(self.turns.pop(0))
        if card[1] == "b":
            for i in range(0, 2):
                self.turns.append(self.turns.pop(0))
        if card[1] != "r" and card[1] != "b":
            self.turns.append(self.turns.pop(0))

    def player_no_move(self):
        if self.current_pickup_amount == 0:
            self.hands[self.current_player].append(self.deck.pop(0))
        if self.current_pickup_amount > 0:
            for i in range(0,self.current_pickup_amount):
                self.hands[self.current_player].append(self.deck.pop(0))
            self.current_pickup_amount = 0
        self.turns.append(self.turns.pop(0))


def demo():
    # game = Game()
    #
    # player_1_uuid = game.add_player("Alex")
    # player_2_uuid = game.add_player("Dan")

    players = ["Alex", "Dan"]
    game = Game(*players)
    print(game.hands)

    while not game.is_game_over():
        player = players.index(game.get_status(0)["current_turn"])

        print(f"Its {players[player]}'s Turn!")
        status = game.get_status(player)
        print("RAW STATUS", status)
        print(f"The top card is {status['top_card']}")
        print(f"Current pickup stack is {status['current_pickup_amount']}")
        print(f"Your hand is {status['your_hand']}  (dont tell the other person ;) )")

        move = ""
        error = BAD_MOVE

        while error != VALID_MOVE:
            print("Make a move!")
            move = input("> ")

            if not move:
                error = VALID_MOVE
                continue

            if move[0] == "M":
                print("The color please")

                color = ""
                while color not in ["r", "y", "g", "b"]:
                    color = input("> ")

                move = color.upper() + move[1]

            error = game.validate_move(player, move)

            if error == BAD_MOVE:
                print("Bad move!")

        print("Playing move...")
        if move:
            game.player_move(move)
        else:
            game.player_no_move()


if __name__ == '__main__':
    demo()
