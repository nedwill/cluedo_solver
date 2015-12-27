#Simple Cluedo variation in Python to develop an alg. to crush my sister.
#Buying this game for me was a mistake.
#Written in Python 3 after bug hunting. Wow its code base is cleaner.

from random import sample

SUSPECTS = frozenset(["scarlett", "plum", "peacock", "green", "mustard", "white"])
WEAPONS = frozenset(["candlestick", "dagger", "leadpipe", "revolver", "rope", "spanner"])
ROOMS = frozenset(["kitchen", "ballroom", "conservatory", "billiard",
                   "library", "study", "hall", "lounge", "dining"])

NUM_OPPONENTS = 4

class Card:
    suspect = 0
    weapon = 1
    room = 2

    def __init__(name, _type):
        assert type in [0, 1, 2]
        self.name = name
        self._type = _type

def get_item(s):
    assert(len(s) == 1)
    return list(s)[0]

#all players must implement witness_personal, witness_other, and do_turn

#random.choice doesn't work on frozen sets...
def choice(fset):
    return sample(fset, 1)[0]

class Bot:
    def __init__(self, suspect_cards, weapon_cards, room_cards):
        self.suspect_cards = suspect_cards
        self.weapon_cards = weapon_cards
        self.room_cards = room_cards

    #def witness_personal(self, cards_requested, player_responded, card_shown):
    #    pass

    def witness_other(self, player_requested, cards_requested, player_responded, card_shown):
        pass

    def do_turn(self, game_state):
        suspect_guesses = SUSPECTS - self.suspect_cards
        weapon_guesses = WEAPONS - self.weapons
        room_guesses = ROOMS - self.rooms
        win_conditions = [
            len(suspect_guesses) == 1,
            len(weapon_guesses) == 1,
            len(room_guesses) == 1
        ]
        if len(suspect_guesses) == 1:
            suspect_guess = Card(choice(suspect_guesses), Card.suspect)
        else:
            suspect_guess = Card(choice(SUSPECTS), Card.suspect)
        if len(weapon_guesses) == 1:
            weapon_guess = Card(choice(weapon_guesses), Card.weapon)
        else:
            weapon_guess = Card(choice(WEAPONS), Card.weapon)
        if len(room_guesses) == 1:
            room_guess = Card(choice(room_guesses), Card.room)
        else:
            room_guess = Card(choice(ROOMS), Card.room)
        if all(win_conditions):
            print("I win!")
            print("Guess is suspect: {}, weapon: {}, room: {}".format(suspect_guess, weapon_guess, room_guess))
            print("Actual is suspect: {}, weapon: {}, room: {}".format(game_state.suspect, game_state.weapon, game_state.room))
            exit()
        seen = game_state.make_guess(suspect_guess, weapon_guess, room_guess)
        if seen is None:
            pass

class Human:
    def __init__(self, suspect_cards, weapon_cards, room_cards):
        self.suspect_cards = suspect_cards
        self.weapon_cards = weapon_cards
        self.room_cards = room_cards
        self.other_player_info = {}

    #player that requested, player that responded, whether they showed a card
    def witness(self, player_requested, cards_requested, player_responded, card_shown):
        pass

    def do_turn(self, game_state):
        pass

def partition_set(fset, num_subsets):
    n = len(fset)
    num_each = n // num_sub


class GameState:
    def __init__(self, num_opponents):
        if num_opponents <= 0:
            print("Need at least 1 opponent.")
            exit()
        self.num_players = num_opponents + 1
        self.suspect = choice(SUSPECTS)
        self.suspects = SUSPECTS - frozenset([self.suspect])
        self.weapon = choice(WEAPONS)
        self.weapons = WEAPONS - frozenset([choice(WEAPONS)])
        self.room = choice(ROOMS)
        self.rooms = ROOMS - frozenset([self.room])
        self.players = [Human()] + [Bot() for _ in range(num_opponents)]

    def make_guess(self, suspect_guess, weapon_guess, room_guess):
        people_to_ask = current_player_i

    def play_game(self):
        current_player_i = 0
        while True:
            current_player = self.players[current_player_i]
            current_player.do_turn(self)
            self.current_player_i += 1
            self.current_player_i %= self.num_players

game = GameState(NUM_OPPONENTS)
game.play_game()
