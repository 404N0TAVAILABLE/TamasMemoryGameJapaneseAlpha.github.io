import pyglet.font
import pyglet.resource

from cocos.director import director

from mainmenu import new_menu

if __name__ == '__main__':
    pyglet.resource.path.append('assets')
    pyglet.resource.reindex()
    pyglet.font.add_file('assets/fonts/Oswald-Regular.ttf')
    director.init(caption = 'Tama\'s Memory Game')
    director.run(new_menu())
