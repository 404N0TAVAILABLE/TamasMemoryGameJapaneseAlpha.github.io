import random

import cocos.actions as cocos_action

from itertools import islice

from card import Card

CARD_HIDDEN_STATUS = 'hidden'
CARD_FRONT_STATUS = 'front'
CARD_BACK_STATUS = 'back'
IMAGE_EXT = '.png'

LEFT = cocos_action.RotateBy(-90, 1)

def move(x, y):
    dur = abs(x + y) / 100.0
    return cocos_action.MoveBy((x, y), duration = 0.5)




class CardTable: 
    def __init__ (self, game_layer, x, y, card_back, cards_available_set_1, cards_available_set_2, scenario, image_asset_dir):
        self.cards = []                     # complete list of cards in deck
        self.pair_of_keys = []              # list of key numbers that have been dealt
#        self.cards_in_deck = []             # stores the cards that have been dealt
        self.position_x = x
        self.position_y = y
        self.game_layer = game_layer
        self.scenario = scenario
        self.card_back = card_back
        self.name = ''
        self.key = 0
        self.number = 0
        self.image_asset_dir = image_asset_dir

        self.side = 40

        # Create individual card objects, two per image
        for key in cards_available_set_1.keys():
            # Add to list of cards
            self.name = key
            self.cards.append(Card(self.position_x, self.position_y, self.name, self.key, self.number, 
                card_back, cards_available_set_1[key], self.scenario.actions))

        for key in cards_available_set_1.keys():
            # Add again (to have 2 cards for each img)
            self.name = key
            self.cards.append(Card(self.position_x, self.position_y, self.name, self.key, self.number, 
                card_back, cards_available_set_2[key], self.scenario.actions))

        # hide all the cards
#        for card in self.cards:
#            card.hide = CARD_HIDDEN_STATUS


    # Set the table settings
    def setup_table(self, card_start_x, card_start_y, num_cards_per_row, 
            x_distance_between_cards, y_distance_between_cards):

        self.card_start_x = card_start_x
        self.card_start_y = card_start_y
        self.num_cards_per_row = num_cards_per_row
        self.x_distance_between_cards = x_distance_between_cards
        self.y_distance_between_cards = y_distance_between_cards


    # Shuffle the cards and update their positions
    def deal_cards(self, max_cards_dealt):
        # Create a temporary list of card indexes that is then shuffled
        keys = []   # list to store inital deck without matching pairs
        self.pair_of_keys = []  # reset the working key list

        # half of the deck is a set and the other is the matching pair
        for i in range (len(self.cards) // 2):        # // = integer division
            keys.append(i)

        random.shuffle(keys)    # we shuffle to randomize the unique deck

        # We pull the max_cards_default from the unique deck and add it to our paired deck
        for c in range (max_cards_dealt):
            self.pair_of_keys.append(keys[c])
            # we add len(keys) because the matching pair is in the 2nd set of cards added above
            # ex. a deck of 20 unique cards, current key is 7, the 2nd card would be self.cards[27]
            self.pair_of_keys.append(keys[c] + (len(keys)))
            print("self cards in set 1  : " + str(self.cards[keys[c]].name))
            print("self cards in set 2 : " + str(self.cards[keys[c] + (len(keys))].name)) 

        # we shuffle again to minimize the chance same pairs end up next to one another
        random.shuffle(self.pair_of_keys)    

        # Setup card positions
        xpos = self.card_start_x
        ypos = self.card_start_y
        print("Card start x : " + str(self.card_start_x))
        print("Card start y : " + str(self.card_start_y))
        cards_on_row = 0

        # Give each card number based on position
        # count left to right, top to bottom
        card_number = 0

        for key in self.pair_of_keys:
            # Reset (ie. unhide if hidden and display back)
            self.cards[key].reset()
            self.scenario.actions = [move(xpos, ypos), LEFT]

            self.game_layer.add(Card(-80, 110, self.cards[key].name, key, card_number, 
                self.card_back, self.cards[key], self.scenario.actions))

            self.game_layer._coll_man_slots.add(Card(xpos, ypos, self.cards[key].name, key, card_number, 
                    self.card_back, self.cards[key], self.scenario.actions))

            xpos += self.x_distance_between_cards 

            print("image name " + self.cards[key].card_front_image)

            cards_on_row += 1
            # If reached end of row - move to next
            if (cards_on_row >= self.num_cards_per_row):
                cards_on_row = 0
                xpos = self.card_start_x
                ypos += self.y_distance_between_cards
            card_number += 1


    # Returns all cards that are face down as Card objects
    def cards_face_down(self, card_list):
        selected_cards = []
        for key in card_list:
            if (key.is_facedown()):
                selected_cards.append(key)

        return selected_cards


    def check_for_match(self, card_1, card_2):
        # Note this only works if the total amount of cards is even.
        # Will put in an assert check later because it should never happen
        print("card 1 : " + str(card_1) + " / " + str(card_2))
        if (card_1.key == (card_2.key - len(self.cards) / 2)):
            return True
        elif (card_1.key == (card_2.key + len(self.cards) / 2)):
            return True

        return False


    def reset_faceup_cards(self, player):
        for card in range (2):
            player.get_card(card).turn_over(self.image_asset_dir,
                    self.cards[player.get_card(card).key].card_front_image, IMAGE_EXT)


    def flip_single_card(self, card_to_flip):
        print("flip single card : " + str(card_to_flip))
        card_to_flip.turn_over(self.image_asset_dir, 
                    self.cards[card_to_flip.key].card_front_image, IMAGE_EXT)


    def check_card_clicked(self, x, y):
        card_clicked = self.game_layer._coll_man_slots.objs_touching_point(x, y)

        # return if no card was clicked
        if not len(card_clicked):
            return None

        card = next(iter(card_clicked))
        
        # if not facedown then skip
        if not card.is_facedown():
            return None

        return card
        

    def end_level_reached(self, available_cards):
        card_list = self.create_list_from_set(available_cards)
        print("card list length is : " + str(len(card_list)))
        print("last card is : " + str(card_list))
        if (len(card_list) > 0):
            return False
        return True


    def create_list_from_set(self, ids):
        temp_list = []
        c = iter(ids)
        while True:
            chunk = list(islice(c, 24))
            if not chunk:
                break
            temp_list.append(chunk)
        return temp_list

#    def end_level_reached(self):
#        for card in self.cards:
#            if (not card.is_hidden()):
#                return False
#        return True

    def remove_matched_cards(self, player_1):
        for card in range (2):
            player_1.get_card(card).remove_card()

        # this is the handle for the card from the collision manager click
#        print("card center : " + str(card.cshape.center))
#        print("card name : " + str(card.name))
#        print("card key : " + str(card.key))
#        print("Image is : " + str(card.card_front_image))
        #card_i.image = pyglet.image.load('assets/images/' + self.cards[card.key].card_front_image + '.png')

        # flip the card over
#        card.turn_over(IMAGE_ASSET_DIR, self.cards[card.key].card_front_image, IMAGE_EXT)
#        print("path of image : " + str(self.cards[card.key].card_front_image))

        # this line works
#        card_i.self_destruct()

        


