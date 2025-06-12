import math, random
from panda3d.core import *


def Cloud(radius = 1):
    """ Random cluster drone pattern """
    x = 2 * random.random() - 1
    y = 2 * random.random() - 1
    z = 2 * random.random() - 1
    UnitVector = Vec3(x, y, z)
    UnitVector.normalize()
    return UnitVector * radius


def BaseballSeams(step, numSeams, B, F = 1):
    """ Baseball seam ring drone pattern """
    # Complicated math
    time = step / float(numSeams) * 2 * math.pi
    F4 = 0
    R = 1
    xxx = math.cos(time) - B * math.cos(3 * time)
    yyy = math.sin(time) + B * math.sin(3 * time)
    zzz = F * math.cos(2 * time) + F4 * math.cos(4 * time)
    rrr = math.sqrt(xxx ** 2 + yyy ** 2 + zzz ** 2)
    x = R * xxx / rrr
    y = R * yyy / rrr
    z = R * zzz / rrr
    return Vec3(x, y, z)


def CircleX(self):
    pass


def CircleY(self):
    pass


def CircleZ(self):
    pass
