import random
import sys
import os

from itertools import islice

from player import Player

DIFFICULTY_EASY = 0
DIFFICULTY_NORMAL = 1
DIFFICULTY_HARD = 2


class PlayerAi(Player):

    def __init__(self, card_table, difficulty_level):
        Player.__init__(self)

        self.card_table = card_table

        if (difficulty_level == 0):
            self._difficulty = DIFFICULTY_EASY
        elif (difficulty_level == 1):
            self._difficulty = DIFFICULTY_NORMAL
        elif (difficulty_level == 2):
            self._difficulty = DIFFICULTY_HARD
        else:
            self._difficulty = DIFFICULTY_EASY

   
    # getter for difficulty level for game saves and others
    @property
    def get_difficulty(self):
        return self._difficulty


    def make_guess(self, available_cards):
        # Set the difficulty level
        if (self._difficulty == DIFFICULTY_EASY):
            self.guess_random(available_cards)
        elif (self._difficulty == DIFFICULTY_NORMAL):
            self.guess_remember_sometimes(available_cards)
        elif (self._difficulty == DIFFICULTY_HARD):
            self.guess_remember_all(available_cards)
        else:
            self.guess_random(available_cards)  #defaults to self.guess_random(available_cards) 


    def create(self, ids):
        temp_list = []
        c = iter(ids)
        while True:
            chunk = list(islice(c, 24))
            if not chunk:
                break
            temp_list.append(chunk)
        return temp_list


    def guess_random(self, available_cards):
        this_guess = random.choice(self.create(available_cards)[0])
        print("this guess : " + str(this_guess))
        self.card_table.flip_single_card(this_guess)
        self.select_card(this_guess)


    def guess_remember_all(self, available_cards):
        # If first guess then use random
        if (self.guess[0] == None):
            self.guess_random(available_cards)
            return

        # Search to see if we have seen a matching card
        for search_card in Player.card_memory.values():
            # ignore if current card - or card has been hidden since
            if (search_card == self.guess[0]):
                continue
            # Check to see if the card matches
            if (self.card_table.check_for_match(self.guess[0], search_card)):
                self.card_table.flip_single_card(search_card)
#                search_card.turn_over()
                self.select_card(search_card)
                return
        # If not found the matching card then use random 
        self.guess_random(available_cards)


    def guess_remember_sometimes(self, available_cards):
        # If first guess then use random
        if (self.guess[0] == None):
            self.guess_random(available_cards)
            return
        # Random whether make a proper guess or random guess
        if (random.randint(1, 10) < 5):
            self.guess_random(available_cards)
            return
        # Search to see if we have seen a matching card
        for search_card in Player.card_memory.values():
            # ignore if current card - or card has been hidden since
            if (search_card == self.guess[0]):
                continue
            # Check to see if the card matches
            if (self.card_table.check_for_match(self.guess[0], search_card)):
                self.card_table.flip_single_card(search_card)
#                search_card.turn_over()
                self.select_card(search_card)
                return
        # If not found the matching card then sue random
        self.guess_random(available_cards)


    def guess_remember_recent (self, available_cards):
        # If first guess the use random
        if (self.guess[0] == None):
            self.guess_random(available_cards)
            return
        # Get last 4 cards that were clicked
        # These are just card numbers
        recent_cards = Player.click_order[:-4]      # the slice operator; implied 0 - 4 range
        # Search to see if the one of those is a matching card
        for search_card in Player.card_memory.values():
            # ignore if current card - or card has been hidden since
            if (search_card == self.guess[0]):
                continue
            # ignore if not a recent card
            if (search_card.number not in recent_cards):
                continue
            # Check to see if the card matches
            if (self.card_table.check_for_match(self.guess[0], search_card)):
                self.card_table.flip_single_card(search_card)
#                search_card.turn_over()
                self.select_card(search_card)
                return
        # If not found the matching card then use random 
        self.guess_random(available_cards)


    def get_card(self, card_number):
        return self.guess[card_number]
