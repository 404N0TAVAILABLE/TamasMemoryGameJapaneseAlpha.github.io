import cocos.menu
import cocos.scene
import cocos.layer
import cocos.actions as cocos_action
from cocos.director import director
from cocos.scenes.transitions import FadeTRTransition

import pyglet.app

from gamelayerhiragana import new_game_hiragana
from gamelayerkatakana import new_game_katakana

class MainMenu(cocos.menu.Menu):
    def __init__(self):
        super(MainMenu, self).__init__('Tama\'s Memory Game')

        self.font_title['font_name'] = 'Oswald'
        self.font_title['font_size'] = 40
        self.font_title['bold'] = True
        self.font_item['font_name'] = 'Oswald'
        self.font_item_selected['font_name'] = 'Oswald'

        self.difficulty = ['Easy', 'Normal', 'Hard']
        self.level_map = ['Hiragana', 'Katakana']

        # Index of the level_map list
        self._level_map_item = 0
        # Index of the difficulty list
        self._difficulty_item = 0

        self.menu_anchor_y = 'center'
        self.menu_anchor_x = 'center'

        items = list()
        # The 2 line below appears to be deprecated.  It still works on windows
        # but fails on Kali linux on ARM
#        items.append(cocos.menu.MultipleMenuItemMouseClick('Difficulty: ', self.get_difficulty, self.difficulty,
#        items.append(cocos.menu.MultipleMenuItemMouseClick('Level Map: ', self.set_level_map, self.level_map,
        items.append(cocos.menu.MultipleMenuItem('Difficulty: ', self.get_difficulty, self.difficulty,
                                            self._difficulty_item))
        items.append(cocos.menu.MultipleMenuItem('Level Map: ', self.set_level_map, self.level_map,
                                            self._level_map_item))
        items.append(cocos.menu.MenuItem('New Game', self.on_new_game))
        items.append(cocos.menu.ToggleMenuItem('Show FPS: ', self.show_fps, director.show_FPS))
        items.append(cocos.menu.MenuItem('Quit', pyglet.app.exit))

        self.create_menu(items, cocos_action.ScaleTo(1.25, duration = 0.25), 
                cocos_action.ScaleTo(1.0, duration = 0.25))

    def on_new_game(self):
        if (self.get_level_map == 0):
            self.on_new_game_hiragana()
        elif (self.get_level_map == 1):
            self.on_new_game_katakana()

    
    @property
    def get_level_map(self):
        return self._level_map_item


    def set_level_map(self, index):
        print('Level map set to: ', self.level_map[index])
        self._level_map_item = index


    def on_new_game_hiragana(self):
        director.push(FadeTRTransition(new_game_hiragana(self.game_difficulty), duration = 3))


    def on_new_game_katakana(self):
        director.push(FadeTRTransition(new_game_katakana(self.game_difficulty), duration = 3))


    def start_game(self):
        print('Starting a new game!')


    def set_player_name(self, name):
        print('Player name: ', name)


    @property
    def game_difficulty(self):
        return self._difficulty_item

    def get_difficulty(self, index):
        print('Difficulty est to ', self.difficulty[index])
        self._difficulty_item = index


    def show_fps(self, val):
        #cocos.director.director.show_FPS = val
        director.show_FPS = val


def new_menu():
    scene = cocos.scene.Scene()
    color_layer = cocos.layer.ColorLayer(205, 133, 63, 255)
    scene.add(MainMenu(), z = 1)
    scene.add(color_layer, z = 0)
    return scene
