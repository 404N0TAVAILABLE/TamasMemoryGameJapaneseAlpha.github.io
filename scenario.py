import cocos.tiles
import cocos.actions as cocos_action

RIGHT = cocos_action.RotateBy(90, 1)
LEFT = cocos_action.RotateBy(-90, 1)

def move(x, y):
    dur = abs(x + y) / 100.0
    return cocos_action.MoveBy((x, y), duration = dur)



class Scenario(object):
    def __init__(self, tmx_map):
        self.tmx_map = tmx_map
        self._actions = None


    def get_background(self):
#        tmx_map = cocos.tiles.load('assets/images/tower_defense.tmx')
        tmx_map = cocos.sprite.Sprite('assets/images/background/girl_sleeping_on_desk_001.png')
        tmx_map.position = 320, 240 
        tmx_map.scale = 1 
#        background = tmx_map[self.tmx_map]
#        background.set_view(0, 0, background.px_width, background.px_height)

        return tmx_map
#        return background


    @property
    def actions(self):
        return self._actions


    @actions.setter
    def actions(self, actions):
        self._actions = cocos_action.RotateBy(90, 0.5)
        for step in actions:
            self._actions += step



def get_scenario():
    scenario_01 = Scenario('map0')      # calls class Scenario
    scenario_01.actions = [move(610, 0), LEFT, move(0, 160),
            LEFT, move(-415, 0), RIGHT, move(0, 160), RIGHT, move(420, 0)]

    return scenario_01

