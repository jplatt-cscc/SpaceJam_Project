from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.task import Task


class Planet(ShowBase):
    """ For loading planet models """
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setName(nodeName)
        Texture = loader.loadTexture(texPath)
        self.modelNode.setTexture(Texture, 1)


class Drones(ShowBase):
    """ For loading drone models """
    # Counts how many drones have spawned
    DroneCount = 0

    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setName(nodeName)
        Texture = loader.loadTexture(texPath)
        self.modelNode.setTexture(Texture, 1)


class Universe(ShowBase):
    """ For loading the universe model """
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setName(nodeName)
        Texture = loader.loadTexture(texPath)
        self.modelNode.setTexture(Texture, 1)


class Player(ShowBase):
    """ For loading the player model """
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setName(nodeName)
        Texture = loader.loadTexture(texPath)
        self.modelNode.setTexture(Texture, 1)


# Needed to use 'base' instead of 'self' for '.taskMgr' and '.render' | I don't know why
    def Thrust(self, keyDown):
        """ For player movement & detecting inputs """
        if keyDown:
            base.taskMgr.add(self.ApplyThrust, 'forward-thrust')
        else:
            base.taskMgr.remove('forward-thrust')
    

    def ApplyThrust(self, task):
        """ For player movement & applying inputs """
        Rate = 5
        Trajectory = base.render.getRelativeVector(self.modelNode, Vec3.forward())
        Trajectory.normalize()
        self.modelNode.setFluidPos(self.modelNode.getPos() + Trajectory * Rate)
        return Task.cont
    

    def SetKeyBindings(self):
        """ For player movement & setting keybinds """
        self.accept('space', self.Thrust, [1])
        self.accept('space-up', self.Thrust, [0])
        self.accept('a', self.LeftTurn, [1])
        self.accept('a-up', self.LeftTurn, [0])

    
    def LeftTurn(self, keyDown):
        if keyDown:
            base.taskMgr.add(self.ApplyLeftTurn, 'left-turn')
        else:
            base.taskMgr.remove('left-turn')
    

    def ApplyLeftTurn(self, task):
        # Turns half a degree per frame
        Rate = 0.5
        self.modelNode.setH(self.modelNode.getH() + Rate)
        return Task.cont


class SpaceStation(ShowBase):
    """ For loading the space station model """
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setName(nodeName)
        Texture = loader.loadTexture(texPath)
        self.modelNode.setTexture(Texture, 1)
