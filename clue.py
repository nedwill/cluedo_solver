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

    def __init__(self, name, _type):
        assert type in [0, 1, 2]
        self.name = name
        self._type = _type

    def __str__(self):
        card_types = {self.suspect: "suspect", self.weapon: "weapon", self.room: "room"}
        return "Card Type: {}, Card Name: {}".format(self.name, card_types[self._type])

    def __repr__(self):
        return self.__str__()

def get_item(s):
    assert(len(s) == 1)
    return list(s)[0]

#all players must implement witness and do_turn

#random.choice doesn't work on frozen sets...
def choice(fset):
    return sample(fset, 1)[0]

class Bot:
    def __init__(self, suspect_cards, weapon_cards, room_cards):
        self.suspect_cards = suspect_cards
        self.weapon_cards = weapon_cards
        self.room_cards = room_cards
        self.known_suspects = set()
        self.known_weapons = set()
        self.known_rooms = set()

    #we technically know cards_requested, but we want
    #to minimize state for now

    def witness_personal(self, cards_requested, card):
        def add_card(card):
            if card._type = Card.suspect:
                self.known_suspects.add(card.name)
            elif card._type = Card.weapon:
                self.known_weapons.add(card.name)
            elif card._type = Card.room:
                self.known_rooms.add(card.name)
            else:
                assert False #unreachable
        if card is None:
            for _card in cards_requested:
                add_card(_card)
        else:
            add_card(card)

    def witness(self, player_requested, cards_requested, player_responded, card_shown):
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

class PlayerInfo:
    def __init__(self, doesnt_have=set(), has=set(), has_conj=[]):
        self.doesnt_have = set(doesnt_have) #make copy
        self.has = set(has)
        self.has_conj = has_conj

    def add_doesnt_have_disj(self, cards):
        for card in cards:
            self.doesnt_have.add(card)

    def add_has_disj(self, cards):
        disj = set(cards)
        self.has_conj.add(has_conj)

    def add_has(self, card):
        self.has.add(card)

class Human:
    def __init__(self, suspect_cards, weapon_cards, room_cards):
        self.suspect_cards = suspect_cards
        self.weapon_cards = weapon_cards
        self.room_cards = room_cards
        self.known_suspects = set()
        self.known_weapons = set()
        self.known_rooms = set()
        self.other_player_info = {}

    def witness_personal(self, cards_requested, card):
        def add_card(card):
            if card._type = Card.suspect:
                self.known_suspects.add(card.name)
            elif card._type = Card.weapon:
                self.known_weapons.add(card.name)
            elif card._type = Card.room:
                self.known_rooms.add(card.name)
            else:
                assert False #unreachable
        if card is None:
            for _card in cards_requested:
                add_card(_card)
        else:
            add_card(card)

    #player that requested, player that responded, whether they showed a card
    def witness(self, player_requested, cards_requested, player_responded, card_shown):
        if card_shown:

    def do_turn(self, game_state):
        pass

def partition_set(fset, num_subsets):
    assert 0 <= num_subsets <= len(fset)
    st = set(fset) #make mutable copy
    num_each = len(fset) // num_sub
    num_extra = len(fset) % num_sub
    assert num_extra < num_sub
    l = []
    for i in range(num_subsets):
        num_to_pick = num_each
        if i < num_extra:
            num_to_pick += 1
        picked = sample(st, num_to_pick)
        st -= picked
        l.append(picked)
    assert len(l) == num_subsets
    assert sum(len(sb) for sb in l) == n
    return l

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
        all_peeps = list(range(self.num_players))
        #everyone in order after the player
        #player 3 goes in a game of 5 players -> [4, 0, 1, 2]
        people_to_ask = all_peeps[self.current_player_i:] + all_peeps[:self.current_player_i-1]

    def play_game(self):
        current_player_i = 0
        while True:
            current_player = self.players[current_player_i]
            current_player.do_turn(self)
            self.current_player_i += 1
            self.current_player_i %= self.num_players

game = GameState(NUM_OPPONENTS)
game.play_game()
