#Simple Cluedo variation in Python to develop an alg. to crush my sister.
#Buying this game for me was a mistake.
#Written in Python 3 after bug hunting. Wow its code base is cleaner.

from random import sample

SUSPECTS = frozenset(["scarlett", "plum", "peacock", "green", "mustard", "white"])
WEAPONS = frozenset(["candlestick", "dagger", "leadpipe", "revolver", "rope", "spanner"])
ROOMS = frozenset(["kitchen", "ballroom", "conservatory", "billiard",
                   "library", "study", "hall", "lounge", "dining"])

NUM_OPPONENTS = 3

class Card:
    suspect = 0
    weapon = 1
    room = 2

    def __init__(self, name, _type):
        assert _type in [0, 1, 2]
        assert isinstance(name, str)
        self.name = name
        self._type = _type

    def __str__(self):
        assert isinstance(self.name, str)
        return self.name
        #card_types = {self.suspect: "suspect", self.weapon: "weapon", self.room: "room"}
        #return "Card Type: {}, Card Name: {}".format(card_types[self._type], self.name)

    def __lt__(self, other):
        return self.name.__lt__(other.name)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        #print("__eq__ called!")
        return self._type == other._type and self.name == other.name

    def __repr__(self):
        return self.__str__()

def get_item(s):
    assert(len(s) == 1)
    return list(s)[0]

#random.choice doesn't work on frozen sets...
def choice(fset):
    return sample(fset, 1)[0]

class Bot:
    def __init__(self, start_cards):
        self.start_cards = start_cards
        self.suspect_names = set()
        self.weapon_names = set()
        self.room_names = set()
        for card in start_cards:
            if card._type == Card.suspect:
                self.suspect_names.add(card.name)
            elif card._type == Card.weapon:
                self.weapon_names.add(card.name)
            elif card._type == Card.room:
                self.room_names.add(card.name)
            else:
                assert False
        self.orig_suspect_names = set(self.suspect_names)
        self.orig_weapon_names = set(self.weapon_names)
        self.orig_room_names = set(self.room_names)

    #we technically know cards_requested, but we want
    #to minimize state for now

    def witness_personal(self, player_requested, cards_requested, card):
        def add_card(card):
            if card._type == Card.suspect:
                self.suspect_names.add(card.name)
            elif card._type == Card.weapon:
                self.weapon_names.add(card.name)
            elif card._type == Card.room:
                self.room_names.add(card.name)
            else:
                assert False #unreachable
        if card is not None:
            add_card(card)

    def witness(self, player_requested, cards_requested, player_responded, was_card_shown):
        pass

    def ask(self, suspect_guess, weapon_guess, room_guess):
        if suspect_guess.name in self.orig_suspect_names:
            return suspect_guess
        if weapon_guess.name in self.orig_weapon_names:
            return weapon_guess
        if room_guess.name in self.orig_room_names:
            return room_guess
        return None

    def do_turn(self, game_state):
        suspect_guesses = SUSPECTS - self.suspect_names
        weapon_guesses = WEAPONS - self.weapon_names
        room_guesses = ROOMS - self.room_names
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
        game_state.make_guess(suspect_guess, weapon_guess, room_guess)

class PlayerInfo:
    def __init__(self, doesnt_have=set(), has=set(), has_disjs=[]):
        self.doesnt_have = set(doesnt_have)
        self.has = set(has)
        self.has_disjs = list(has_disjs)

    def _simplify(self):
        tmp = []
        for e in self.has_disjs:
            e -= self.doesnt_have
            if not e.isdisjoint(self.has):
                continue
            if len(e) == 1:
                self.has.add(list(e)[0])
            elif len(e) > 1:
                tmp.append(e)
        self.has_disjs = tmp

    def add_doesnt_have_disj(self, cards):
        for card in cards:
            self.doesnt_have.add(card)
        self._simplify()

    def add_has_disj(self, cards):
        disj = set(cards)
        if disj not in self.has_disjs:
            self.has_disjs.append(disj)
            self._simplify()

    def add_has(self, card):
        self.has.add(card)
        self._simplify()

    def __str__(self):
        return "Doesn't Have: {}, Has: {}, Has Disj: {}".format(list(sorted(self.doesnt_have)), list(sorted(self.has)), list(sorted(self.has_disjs)))

    def __repr__(self):
        return self.__str__()

class Human:
    def __init__(self, start_cards):
        self.start_cards = start_cards
        self.suspect_names = set()
        self.weapon_names = set()
        self.room_names = set()
        for card in start_cards:
            if card._type == Card.suspect:
                self.suspect_names.add(card.name)
            elif card._type == Card.weapon:
                self.weapon_names.add(card.name)
            elif card._type == Card.room:
                self.room_names.add(card.name)
            else:
                assert False
        self.orig_suspect_names = set(self.suspect_names)
        assert self.orig_suspect_names is not self.suspect_names
        self.orig_weapon_names = set(self.weapon_names)
        self.orig_room_names = set(self.room_names)
        self.other_player_info = [PlayerInfo() for _ in range(NUM_OPPONENTS)]
        for player in self.other_player_info:
            player.add_doesnt_have_disj(start_cards)

    def witness_personal(self, player_responded, cards_requested, card):
        #print("We're shown {} by {}!".format(card, player_responded))
        def add_card(card):
            if card._type == Card.suspect:
                self.suspect_names.add(card.name)
            elif card._type == Card.weapon:
                self.weapon_names.add(card.name)
            elif card._type == Card.room:
                self.room_names.add(card.name)
            else:
                assert False #unreachable
        if card is None:
            self.other_player_info[player_responded-1].add_doesnt_have_disj(cards_requested)
        else:
            add_card(card)
            for i, player in enumerate(self.other_player_info):
                if i == player_responded-1:
                    player.add_has(card)
                else:
                    player.add_doesnt_have_disj(set([card]))

    #player that requested, player that responded, whether they showed a card
    def witness(self, _player_requested, cards_requested, player_responded, was_card_shown):
        #assumption: we are always player 0
        player_i = player_responded - 1
        if was_card_shown:
            #print("We saw that player {} had one of the following: {}".format(player_responded, cards_requested))
            self.other_player_info[player_i].add_has_disj(cards_requested)
        else:
            #print("We saw that player {} didn't have one of the following: {}".format(player_responded, cards_requested))
            self.other_player_info[player_i].add_doesnt_have_disj(cards_requested)

    def ask(self, suspect_guess, weapon_guess, room_guess):
        possible_answers = []
        if suspect_guess.name in self.orig_suspect_names:
            possible_answers.append(suspect_guess)
        if weapon_guess.name in self.orig_weapon_names:
            possible_answers.append(weapon_guess)
        if room_guess.name in self.orig_room_names:
            possible_answers.append(room_guess)
        if len(possible_answers) == 0:
            #print("You didn't have any of the cards. We'll tell everyone that.")
            return None
        #print("Please select from the following:")
        #print("\n".join("{} -> {}".format(*x) for x in enumerate(possible_answers)))
        #if len(possible_answers) == 1:
        #    return possible_answers[0]

        return choice(possible_answers)
        #actual human
        """
        while True:
            try:
                answer = int(input("Please pick a number: "))
                if answer not in range(len(possible_answers)):
                    print("Try again with valid number.")
                    continue
            except ValueError:
                print("Try again with valid number.")
                continue
            return possible_answers[answer]
        """

    def do_turn(self, game_state):
        #print("Here's the current known info:")
        for player in self.other_player_info:
            for card in player.has:
                if card._type == Card.suspect:
                    self.suspect_names.add(card.name)
                elif card._type == Card.weapon:
                    self.weapon_names.add(card.name)
                elif card._type == Card.room:
                    self.room_names.add(card.name)
        #print("We have: {}, {}, {}".format(list(sorted(self.suspect_names)), list(sorted(self.weapon_names)), list(sorted(self.room_names))))
        #for player_i in range(NUM_OPPONENTS):
        #    print("Player number {} info: {}".format(player_i+1, self.other_player_info[player_i]))

        #auto Ned
        suspect_guesses = SUSPECTS - self.suspect_names
        weapon_guesses = WEAPONS - self.weapon_names
        room_guesses = ROOMS - self.room_names
        assert len(suspect_guesses) != 0 and len(weapon_guesses) != 0 and len(room_guesses) != 0

        #if len(suspect_guesses) == 1:
        #    print("guessing only possible supect")
        #if len(weapon_guesses) == 1:
        #    print("guessing only possible weapon")
        #if len(room_guesses) == 1:
        #    print("guessing only possible room")

        suspect_guess = Card(choice(suspect_guesses), Card.suspect)
        weapon_guess = Card(choice(weapon_guesses), Card.weapon)
        room_guess = Card(choice(room_guesses), Card.room)
        game_state.make_guess(suspect_guess, weapon_guess, room_guess)

        #human can play too
        """
        while True:
            suspect_guess = input("Please pick a suspect ({}): ".format(", ".join(list(sorted(SUSPECTS)))))
            if suspect_guess in SUSPECTS:
                break
            print("Sorry, that wasn't a valid suspect.")
        while True:
            weapon_guess = input("Please pick a weapon ({}): ".format(", ".join(list(sorted(WEAPONS)))))
            if weapon_guess in WEAPONS:
                break
            print("Sorry, that wasn't a valid weapon.")
        while True:
            room_guess = input("Please pick a room ({}): ".format(", ".join(list(sorted(ROOMS)))))
            if room_guess in ROOMS:
                break
            print("Sorry, that wasn't a valid room.")
        game_state.make_guess(Card(suspect_guess, Card.suspect), Card(weapon_guess, Card.weapon), Card(room_guess, Card.room))
        """

def partition_set(fset, num_subsets):
    assert 0 <= num_subsets <= len(fset)
    num_each = len(fset) // num_subsets
    num_extra = len(fset) % num_subsets
    assert num_extra < num_subsets
    st = set(fset) #make mutable copy
    assert st is not fset
    l = []
    for i in range(num_subsets):
        num_to_pick = num_each
        if i < num_extra:
            num_to_pick += 1
        picked = set(sample(st, num_to_pick))
        st -= picked
        l.append(picked)
    assert len(l) == num_subsets
    assert sum(len(sb) for sb in l) == len(fset)
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
        self.weapons = WEAPONS - frozenset([self.weapon])
        self.room = choice(ROOMS)
        self.rooms = ROOMS - frozenset([self.room])
        self.banned = set()
        start_cards = set()
        for suspect in self.suspects:
            start_cards.add(Card(suspect, Card.suspect))
        for weapon in self.weapons:
            start_cards.add(Card(weapon, Card.weapon))
        for room in self.rooms:
            start_cards.add(Card(room, Card.room))
        assignments = partition_set(start_cards, self.num_players)
        self.players = [Human(assignments[0])] + [Bot(assignments[i+1]) for i in range(num_opponents)]
        self.game_running = True
        self.winner = None

    def accuse(self, suspect_name, weapon_name, room_name):
        if (self.suspect, self.weapon, self.room) == (suspect_name, weapon_name, room_name):
            print("Player {} was right! They win!".format(self.current_player_i))
            exit()
        else:
            print("Player {} was wrong. They're banned from playing but can still show cards.")
            self.banned.add(self.current_player_i)
            if len(self.banned) == self.num_players:
                print("Wow, you're all losers!")
                exit()

    def _check_ai(self):
        human_info = self.players[0].other_player_info
        for i, player in enumerate(human_info):
            player_i = i+1
            assert player.has.issubset(self.players[player_i].start_cards)

    def make_guess(self, suspect_guess, weapon_guess, room_guess):
        #print("Player {} is guessing {}, {}, {}.".format(self.current_player_i, suspect_guess, weapon_guess, room_guess))
        if suspect_guess.name == self.suspect and weapon_guess.name == self.weapon and room_guess.name == self.room:
            print("Player {} won!".format(self.current_player_i))
            self.game_running = False
            self.winner = self.current_player_i
            return
        all_players = list(range(self.num_players))
        #everyone in order after the player
        #player 3 goes in a game of 5 players -> [4, 0, 1, 2]
        people_to_ask = all_players[self.current_player_i+1:] + all_players[:self.current_player_i]
        cards_requested = (suspect_guess, weapon_guess, room_guess)
        #this code smells bad
        for person_i in people_to_ask:
            card = self.players[person_i].ask(*cards_requested)
            if card is None:
                #print("Player {} says: I don't have a card!".format(person_i))
                #make sure they didn't lie
                assert suspect_guess.name not in self.players[person_i].orig_suspect_names
                assert weapon_guess.name not in self.players[person_i].orig_weapon_names
                assert room_guess.name not in self.players[person_i].orig_room_names
            else:
                #print("Player {} says: I have a card!".format(person_i))
                assert isinstance(card, Card)
            for person_i2 in range(self.num_players):
                if person_i2 == person_i:
                    pass #they know the info they just gave...
                elif person_i2 == self.current_player_i:
                    self.players[person_i2].witness_personal(person_i, cards_requested, card)
                elif card is None:
                    self.players[person_i2].witness(person_i, cards_requested, person_i, was_card_shown=False)
                else:
                    assert isinstance(card, Card)
                    self.players[person_i2].witness(person_i, cards_requested, person_i, was_card_shown=True)
            if card is not None:
                break
        self._check_ai()

    def play_game(self):
        self.current_player_i = 0
        while self.game_running:
            if self.current_player_i not in self.banned:
                current_player = self.players[self.current_player_i]
                current_player.do_turn(self)
            self.current_player_i += 1
            self.current_player_i %= self.num_players

from collections import Counter

ctr = Counter()
for _ in range(10000):
    game = GameState(NUM_OPPONENTS)
    game.play_game()
    ctr[game.winner] += 1
    print("hi", ctr)
