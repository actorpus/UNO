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

# validate_move(player_number, card) -> {
#   0: not your go
#   1: bad choise
#   2: valid move
# }


class Game:
    def __init__(self, number_of_players: int, player_names: list[str]):
        self.players = []

        for _ in range(number_of_players):
            self.players.append(Player())

    def get_status(self, player_number):
        self.hand =0


class Player:
    def __init__(self, hand, hand_length):
        self.hand = hand
        self.length = hand_length


class Player:
    def __init__(self, name, fitness):
        self.username = name
        self.fitness = fitness
        self.health = 100

    def stats(self):
        return f"{self.username} is {self.fitness} fit and has {self.health} health"

    def damage(self):
        self.health = self.health - 10