import cocos.sprite
import cocos.euclid as euclidean
import cocos.collision_model as collision_model

from cocos.director import director


class Actor(cocos.sprite.Sprite):
    def __init__(self, img, x, y):
        super(Actor, self).__init__(img, position = (x, y))

        pos = x, y
        side = 80
        self._cshape = collision_model.AARectShape(euclidean.Vector2(*(pos)), side * 0.5, side * 0.5)

#        print("sprite x y position : " + str(x) + " / " + str(y))


       # self._cshape = collision_model.CircleShape(self.position,
#                                      self.width * 0.5)

    @property
    def cshape(self):
        self._cshape.center = euclidean.Vector2(*(self.x, self.y))
#        print("self._cshape.center : " + str(self._cshape.center))
#        print("sprintes position : " + str(self.position))
        return self._cshape

