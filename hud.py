
import cocos

from cocos.director import director

COLOR_RED = (255, 0, 0, 255)

class HUD(cocos.layer.Layer):
    def __init__(self):
        super(HUD, self).__init__()
        width, height = director.get_window_size()
        self.player_1_score_text = self._create_text(60, height - 40)
        self.player_2_score_text = self._create_text(width - 100, height - 40)
        self.message = self._create_text_color(width / 2, height / 2, COLOR_RED)


    def _create_text(self, x, y):
        text = cocos.text.Label(font_size = 18, font_name = 'Oswald',
                anchor_x = 'center', anchor_y = 'center')

        text.position = (x, y)
        self.add(text)
        return text


    def _create_text_color(self, x, y, color_rgba):
        text = cocos.text.Label(color = color_rgba, font_size = 18, font_name = 'Oswald',
                anchor_x = 'center', anchor_y = 'center')

        text.position = (x, y)
        self.add(text)
        return text


    def update_player_1_score(self, player_1_score):
        self.player_1_score_text.element.text = 'Player 1: %s' % player_1_score


    def update_player_2_score(self, player_2_score):
        self.player_2_score_text.element.text = 'Player 2: %s' % player_2_score


    def update_status_line_1(self, message):
        self.message.element.text = message 
