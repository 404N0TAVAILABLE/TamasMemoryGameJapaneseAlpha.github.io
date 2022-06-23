import random
import cocos
import cocos.actions as cocos_action
import cocos.collision_model as collision_model

from cocos.scenes.transitions import SplitColsTransition, FadeTransition
from cocos.director import director

from hud import HUD

from mytimer import Timer
from scenario import get_scenario
from cardtable import CardTable
from gamemode import GameMode
from card import Card
from player import Player
from playerai import PlayerAi
import mainmenu
from dataCardsAvailable_hiragana_jpn import cards_available_hiragana_jpn
from dataCardsAvailable_hiragana_eng import cards_available_hiragana_eng

# These constants are used to simplify the game
# For more flexibility these could be replaced with configurable variables
# (eg. different number of cards for different difficulty levels)
NUM_CARDS_PER_ROW = 6
X_DISTANCE_BETWEEN_CARDS = 85
Y_DISTANCE_BETWEEN_CARDS = 85
CARD_START_X = 190
CARD_START_Y = -20
MAX_CARDS_DEALT = 12
CARD_BACK = 'assets/images/imageback/memorycard_back.png'
PLAYER_AI_STATUS_MESSAGE = 'Thinking which card to pick'
IMAGE_ASSET_DIR = 'assets/images/hiragana/'


class GameLayerHiragana(cocos.layer.Layer):
    is_event_handler = True

    def __init__(self, hud, scenario, difficulty):
        super(GameLayerHiragana, self).__init__()

        self.hud = hud
        self.scenario = scenario
        self._player_1_score = 0
        self._player_2_score = 0
        self.is_game_over = False

        self.timer = Timer(3)   # used for player ai
        self.game_state = GameMode()
        self.player1 = Player()
        self.game_state = GameMode()

        width, height = director.get_window_size()
        cell_size = 80

        print("windows size : " + str(width) + " x " + str(height))

        self.coll_man = collision_model.CollisionManagerGrid(0, width, 0, height,
                                                            cell_size,
                                                            cell_size)

        self._coll_man_slots = collision_model.CollisionManagerGrid(0, width, 0, 
                height, cell_size, cell_size)

        # initialize the cards
        self.all_cards = CardTable(self, CARD_START_X, CARD_START_Y, CARD_BACK, 
                            cards_available_hiragana_jpn, cards_available_hiragana_eng, self.scenario, IMAGE_ASSET_DIR)
        # Set up the table
        self.all_cards.setup_table(CARD_START_X, CARD_START_Y, NUM_CARDS_PER_ROW,
                             X_DISTANCE_BETWEEN_CARDS, Y_DISTANCE_BETWEEN_CARDS)

        # GAME LOOP
        self.schedule(self.game_loop)

        self.player_ai = PlayerAi(self.all_cards, difficulty)


    @property
    def player_1_score(self):
        return self._player_1_score


    @player_1_score.setter
    def player_1_score(self, val):
        self._player_1_score = val
        self.hud.update_player_1_score(val)


    @property
    def player_2_score(self):
        return self._player_2_score 


    @player_2_score.setter
    def player_2_score(self, val):
        self._player_2_score = val
        self.hud.update_player_2_score(val)


    def deal_all_cards(self, max_cards_dealt):
        self.game_state.is_game_start = True
        self.all_cards.deal_cards(max_cards_dealt)


    def update_display_messages(self):
        if (self.game_state.is_player_2_wait() or self.game_state.is_player_2_card1()):
            self.hud.update_status_line_1(PLAYER_AI_STATUS_MESSAGE) 
        else:
            # clear status messages
            self.hud.update_status_line_1('')



    def check_player_ai(self):
        if (self.game_state.is_player_2_start()):
            self.timer.start_count_down()
            self.game_state.set_player_2_wait()

        if (self.game_state.is_player_2_wait()):
            if (self.timer.get_time_remaining() > 0):
                return

            # pass a card list excluding face-up cards
            self.player_ai.make_guess(self.all_cards.cards_face_down(self._coll_man_slots.known_objs()))
            self.timer.start_count_down()
            self.game_state.set_player_2_card1()

        elif (self.game_state.is_player_2_card1()):     # card 1 turned
            if (self.timer.get_time_remaining() > 0):
                return

            # pass a card list excluding face-up cards
            self.player_ai.make_guess(self.all_cards.cards_face_down(self._coll_man_slots.known_objs()))
            self.timer.start_count_down()
            self.game_state.set_player_2_card2()

        elif (self.game_state.is_player_2_card2()):      # card 2 selected - wait then check if matches
            if (self.timer.get_time_remaining() > 0):
                return

            if (self.all_cards.check_for_match(self.player_ai.get_card(0), self.player_ai.get_card(1))):
                # If match add points and remove cards
                self.player_2_score += 1
                self.all_cards.remove_matched_cards(self.player_ai)
                self.player_ai.reset_player_guesses() 

                # referesh the collision manager list since items were removed
                self.update_collision_manager()

                # End of game
                if (self.all_cards.end_level_reached(self._coll_man_slots.known_objs())):
                    # start game over transtion scene
                    director.replace(SplitColsTransition(game_over()))
                    self.game_state.is_game_over = True
                else:
                    self.game_state.continue_player()
            else: # If not match then turn both around
                # flip all the cards over
                self.all_cards.reset_faceup_cards(self.player_ai)
                # reset player guesses
                self.player_ai.reset_player_guesses()
                self.game_state.next_player()


    # BEGIN GAME LOOP    
    def game_loop(self, _):
   #     self._coll_man_slots.clear()

   #     for obj in self.get_children():
   #         if isinstance (obj, Card):
   #             self._coll_man_slots.add(obj)

        # update collision_manager list
        self.update_collision_manager()

        # check for collisions
        for cards in self.all_cards.cards:
            obj = next(self._coll_man_slots.iter_colliding(cards), None)
            cards.collide(obj)

        # Update player ai actions
        self.check_player_ai()

        # Check for messages to display
        self.update_display_messages()


    def update_collision_manager(self):
        
        self._coll_man_slots.clear()

        for obj in self.get_children():
            if isinstance (obj, Card):
               self._coll_man_slots.add(obj)

  

    # INPUT CONTROL
    def on_mouse_press(self, x, y, buttons, mod):

        # Only interested in the left button
        if (not buttons == 1):
            return

        # Return if it's the AI's turn
        if self.game_state.is_player_2():
            return

        # if we reach here then we are in game play
        # Is it player1's turn; double check
        if (not self.game_state.is_player_1):
            return

        if (self.game_state.is_pair_turned_over()):
            if (self.all_cards.check_for_match(self.player1.get_card(0), self.player1.get_card(1))):
                # If match add points and remove cards
                self.player_1_score += 1
                self.all_cards.remove_matched_cards(self.player1)
                self.player1.reset_player_guesses()

                # referesh the collision manager list since items were removed
                self.update_collision_manager()

                # End of game
                if (self.all_cards.end_level_reached(self._coll_man_slots.known_objs())):
                    # start game over transtion scene
                    director.replace(SplitColsTransition(game_over()))
                    self.game_state.is_game_over = True
                else:
                    self.game_state.continue_player()
            # If not match then turn both around
            else:
                # flip all the cards over
                self.all_cards.reset_faceup_cards(self.player1)
                # reset player guesses
                self.player1.reset_player_guesses()
                self.game_state.next_player()

                return

        card_clicked = self.all_cards.check_card_clicked(x, y)
        if (card_clicked != None):
            print("card clicked")
            self.all_cards.flip_single_card(card_clicked)
            self.player1.select_card(card_clicked)
            # Update state
            self.game_state.card_clicked()



def new_game_hiragana(difficulty):
    scenario = get_scenario()
    background = scenario.get_background()
    hud = HUD()
    game_layer = GameLayerHiragana(hud, scenario, difficulty)
    game_layer.deal_all_cards(MAX_CARDS_DEALT)

    return cocos.scene.Scene(background, game_layer, hud)


def game_over():
    width, height = director.get_window_size()
    layer = cocos.layer.Layer()
    text = cocos.text.Label('Game Over', position = (width * 0.5, height * 0.5),
            font_name = 'Oswald', font_size = 72, anchor_x = 'center', anchor_y = 'center')
    layer.add(text)
    scene = cocos.scene.Scene(layer)
    new_scene = FadeTransition(mainmenu.new_menu())
    new_scene_func = lambda: director.replace(new_scene)
    scene.do(cocos_action.Delay(3) + cocos_action.CallFunc(new_scene_func))

    return scene

