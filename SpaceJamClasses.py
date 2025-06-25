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
        """ For detecting forward movement inputs """
        if keyDown:
            base.taskMgr.add(self.ApplyThrust, 'forward-thrust')
        else:
            base.taskMgr.remove('forward-thrust')
    

    def ApplyThrust(self, task):
        """ For applying forward movement """
        Rate = 5
        Trajectory = base.render.getRelativeVector(self.modelNode, Vec3.forward())
        Trajectory.normalize()
        self.modelNode.setFluidPos(self.modelNode.getPos() + Trajectory * Rate)
        return Task.cont
    

    def SetKeyBindings(self):
        """ For setting player movement keybinds """
        # '.getH' for left/right turns | '.getP' for up/down turns | '.getR' for left/right rolls
        self.accept('space', self.Thrust, [1])
        self.accept('space-up', self.Thrust, [0])
        self.accept('a', self.LeftTurn, [1])
        self.accept('a-up', self.LeftTurn, [0])
        self.accept('d', self.RightTurn, [1])
        self.accept('d-up', self.RightTurn, [0])
        self.accept('w', self.UpTurn, [1])
        self.accept('w-up', self.UpTurn, [0])
        self.accept('s', self.DownTurn, [1])
        self.accept('s-up', self.DownTurn, [0])
        self.accept('q', self.LeftRoll, [1])
        self.accept('q-up', self.LeftRoll, [0])
        self.accept('e', self.RightRoll, [1])
        self.accept('e-up', self.RightRoll, [0])

    
    def LeftTurn(self, keyDown):
        """ For detecting left turn inputs """
        if keyDown:
            base.taskMgr.add(self.ApplyLeftTurn, 'left-turn')
        else:
            base.taskMgr.remove('left-turn')
    

    def ApplyLeftTurn(self, task):
        """ For applying left turn movement """
        # Turns half a degree left per frame
        Rate = 0.5
        self.modelNode.setH(self.modelNode.getH() + Rate)
        return Task.cont


    def RightTurn(self, keyDown):
        """ For detecting Right turn inputs """
        if keyDown:
            base.taskMgr.add(self.ApplyRightTurn, 'right-turn')
        else:
            base.taskMgr.remove('right-turn')
    

    def ApplyRightTurn(self, task):
        """ For applying right turn movement """
        # Turns half a degree right per frame
        Rate = -0.5
        self.modelNode.setH(self.modelNode.getH() + Rate)
        return Task.cont
    

    def UpTurn(self, keyDown):
        """ For detecting up turn inputs """
        if keyDown:
            base.taskMgr.add(self.ApplyUpTurn, 'up-turn')
        else:
            base.taskMgr.remove('up-turn')

    
    def ApplyUpTurn(self, task):
        """ For applying Up turn movement """
        # Turns half a degree up per frame
        Rate = 0.5
        self.modelNode.setP(self.modelNode.getP() + Rate)
        return Task.cont
    

    def DownTurn(self, keyDown):
        """ For detecting down turn inputs """
        if keyDown:
            base.taskMgr.add(self.ApplyDownTurn, 'down-turn')
        else:
            base.taskMgr.remove('down-turn')


    def ApplyDownTurn(self, task):
        """ For applying Down turn movement """
        # Turns half a degree down per frame
        Rate = -0.5
        self.modelNode.setP(self.modelNode.getP() + Rate)
        return Task.cont
    

    def LeftRoll(self, keyDown):
        """ For detecting left roll inputs """
        if keyDown:
            base.taskMgr.add(self.ApplyLeftRoll, 'left-roll')
        else:
            base.taskMgr.remove('left-roll')
    

    def ApplyLeftRoll(self, task):
        """ For applying left roll movement """
        # Rolls one a degree left per frame
        Rate = -1
        self.modelNode.setR(self.modelNode.getR() + Rate)
        return Task.cont
    

    def RightRoll(self, keyDown):
        """ For detecting right roll inputs """
        if keyDown:
            base.taskMgr.add(self.ApplyRightRoll, 'right-roll')
        else:
            base.taskMgr.remove('right-roll')
    

    def ApplyRightRoll(self, task):
        """ For applying right roll movement """
        # Rolls one a degree right per frame
        Rate = 1
        self.modelNode.setR(self.modelNode.getR() + Rate)
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
