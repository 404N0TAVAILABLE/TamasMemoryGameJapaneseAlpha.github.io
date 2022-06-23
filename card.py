import random
import math
import cocos
import pyglet
import os

from actor import Actor

class Card(Actor):
    def __init__(self, x, y, name, key, number, card_back_image, card_front_image, actions):
        super(Card, self).__init__(card_back_image, x, y)

        self.name = name
        self.key = key
        self.current_working_dir = os.getcwd()
        self.card_back_image = self.current_working_dir + "/" + card_back_image
        self.card_front_image = card_front_image

        # Status can be 'back' (turned over) 'front' (turned up) or 
        # 'hidden' (already used)
        self.status = self._status = 'back'
        # Number is unique number based on position
        # count left to right, top to bottom
        # updated after dealt. Used for ai memory
        self._number = number
        self.do(actions)

    @property
    def card_status(self):
        return self._status


    @card_status.setter
    def card_status(self, status):
        self._status = status


    @property
    def card_number(self):
        return self._number


    @card_number.setter
    def card_number(self, number):
        self._number = number


    @property
    def card_position(self):
        x, y = self.x, self.y
        return x, y


    # Is it turned to face down
#    @property
    def is_facedown(self):
        if self.card_status == 'back':
            return True
        return False



    def unhide(self):
        self._status = "back"
        self._image = self.card_back_image


    def collide(self, other):
        self.target = other
        if self.target is not None:
            x, y = other.x - self.x, other.y - self.y
            angle = -math.atan2(y, x)
            self.rotation = math.degrees(angle)


    ### image_asset_dir - folder path to images
    ### card_front_image - the image to display when the card is flipped; default is the back
    ### image_ext - ext of the image ie. png, tga, jpg
    def turn_over(self, image_asset_dir, card_front_image, image_ext):
        if (self.card_status == 'back'):
            self.card_status = 'front'
            self.image = pyglet.image.load(image_asset_dir + card_front_image + image_ext)
        elif (self.card_status == 'front'):
            self.card_status = 'back'
            self.image = pyglet.image.load(self.card_back_image)
        # Attempt to turn over a hidden card - ignore
        else:
            return


    def remove_card(self):
        self.kill()


    def set_position(self, x, y, actions):
        self.do(actions)


    def reset(self):
        self.unhide()

