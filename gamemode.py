# State is tracked as a number, but to make the code readable constants are used
STATE_NEW = 0                   # Game ready to start, but not running
STATE_PLAYER1_START = 10         # Player 1 to turn over card
STATE_PLAYER1_CARDS_1 = 11       # Card 1 turned over
STATE_PLAYER1_CARDS_2 = 12      # Card 2 turned over
STATE_PLAYER2_START = 20       # Card 2 starts go
STATE_PLAYER2_WAIT = 21         # Delay before Card 1 turned over
STATE_PLAYER2_CARDS_1 = 22      # Card 1 turned over
STATE_PLAYER2_CARDS_2 = 23      # Card 2 turned over
STATE_END = 50

# Number of seconds to display high score before allowing click to continue
TIME_DISPLAY_SCORE = 3

class GameMode:

    def __init__ (self):
        # These are what we need to track
#        self.score = 0
        self._state = STATE_NEW

#        # These are the cards that have been turned up.
#        self.cards_selected = [None, None]

    # If game has not yet started
    def is_new_game(self):
        if self._state == STATE_NEW:
            return True
        return False


    @property
    def is_game_over(self):
        if self._state == STATE_END:
            return True
        return False


    @is_game_over.setter
    def is_game_over(self, _):
        # player gets to see high score
#        if is_end:
        self._state = STATE_END


    @property
    def is_game_start(self):
        if self._state == STATE_PLAYER1_START:
            return True
        return False


    @is_game_start.setter
    def is_game_start(self, is_game_start):
        print("is game start called ")
        if (is_game_start): 
            self._state = STATE_PLAYER1_START


    @property
    def is_player_1(self):
        print("state is " + str(self._state))
        if (self._state >= STATE_PLAYER1_START and self._state <= STATE_PLAYER1_CARDS_2):
            return True
        return False

    def is_player_2(self):
        if (self._state >= STATE_PLAYER2_START and self._state <= STATE_PLAYER2_CARDS_2):
            return True
        return False

    def is_player_2_start(self):
        if (self._state == STATE_PLAYER2_START):
            return True
        return False

    def is_player_2_wait(self):
        if (self._state == STATE_PLAYER2_WAIT):
            return True
        return False

    def is_player_2_card1(self):
        if (self._state == STATE_PLAYER2_CARDS_1):
            return True
        return False

    def is_player_2_card2(self):
        if (self._state == STATE_PLAYER2_CARDS_2):
            return True
        return False

    def set_new_game(self):
        self._state = STATE_NEW

    def set_player_2_wait(self):
        self._state = STATE_PLAYER2_WAIT

    def set_player_2_card1(self):
        self._state = STATE_PLAYER2_CARDS_1

    def set_player_2_card2(self):
        self._state = STATE_PLAYER2_CARDS_2

    def is_game_running(self):
        if (self._state >= STATE_PLAYER1_START and self._state <
                STATE_END):
            return True
        return False

    # Continue with current player (matched correctly)
    def continue_player(self):
        if self._state <= STATE_PLAYER1_CARDS_2:
            self._state =  STATE_PLAYER1_START
        else:
            self._state = STATE_PLAYER2_START

    # Switch to next player (not matched)
    def next_player(self):
        if self._state <= STATE_PLAYER1_CARDS_2:
            self._state = STATE_PLAYER2_START
        else:
            self._state = STATE_PLAYER1_START

    def set_new_game(self):
        self._state = STATE_NEW

    def is_pair_turned_over(self):
        if (self._state == STATE_PLAYER1_CARDS_2):
            return True
        return False

    # If a card is clicked then update the state accordingly
    def card_clicked(self):
        if (self._state == STATE_PLAYER1_START):
            self._state = STATE_PLAYER1_CARDS_1
        elif (self._state == STATE_PLAYER1_CARDS_1):
            self._state = STATE_PLAYER1_CARDS_2
