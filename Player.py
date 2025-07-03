from panda3d.core import *
from direct.task import Task
from direct.task.Task import TaskManager
from Collisions import SphereCollider
from typing import Callable


class Ship(SphereCollider):
    """ For loading the player model """
    def __init__(self, loader: Loader, taskMgr: TaskManager, accept: Callable[[str, Callable], None], modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super(Ship, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 0.9)
        self.taskMgr = taskMgr
        self.accept = accept
        self.render = parentNode
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setName(nodeName)
        Texture = loader.loadTexture(texPath)
        self.modelNode.setTexture(Texture, 1)

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

    
    def Thrust(self, keyDown):
        """ For detecting forward movement inputs """
        if keyDown:
            self.taskMgr.add(self.ApplyThrust, 'forward-thrust')
        else:
            self.taskMgr.remove('forward-thrust')
    

    def ApplyThrust(self, task):
        """ For applying forward movement """
        Rate = 5
        Trajectory = self.render.getRelativeVector(self.modelNode, Vec3.down())
        Trajectory.normalize()
        self.modelNode.setFluidPos(self.modelNode.getPos() + Trajectory * Rate)
        return Task.cont

    
    def LeftTurn(self, keyDown):
        """ For detecting left turn inputs """
        if keyDown:
            self.taskMgr.add(self.ApplyLeftTurn, 'left-turn')
        else:
            self.taskMgr.remove('left-turn')
    

    def ApplyLeftTurn(self, task):
        """ For applying left turn movement """
        # Turns half a degree left per frame
        Rate = 0.5
        self.modelNode.setR(self.modelNode.getR() + Rate)
        return Task.cont


    def RightTurn(self, keyDown):
        """ For detecting Right turn inputs """
        if keyDown:
            self.taskMgr.add(self.ApplyRightTurn, 'right-turn')
        else:
            self.taskMgr.remove('right-turn')
    

    def ApplyRightTurn(self, task):
        """ For applying right turn movement """
        # Turns half a degree right per frame
        Rate = -0.5
        self.modelNode.setR(self.modelNode.getR() + Rate)
        return Task.cont
    

    def UpTurn(self, keyDown):
        """ For detecting up turn inputs """
        if keyDown:
            self.taskMgr.add(self.ApplyUpTurn, 'up-turn')
        else:
            self.taskMgr.remove('up-turn')

    
    def ApplyUpTurn(self, task):
        """ For applying Up turn movement """
        # Turns half a degree up per frame
        Rate = 0.5
        self.modelNode.setP(self.modelNode.getP() + Rate)
        return Task.cont
    

    def DownTurn(self, keyDown):
        """ For detecting down turn inputs """
        if keyDown:
            self.taskMgr.add(self.ApplyDownTurn, 'down-turn')
        else:
            self.taskMgr.remove('down-turn')


    def ApplyDownTurn(self, task):
        """ For applying Down turn movement """
        # Turns half a degree down per frame
        Rate = -0.5
        self.modelNode.setP(self.modelNode.getP() + Rate)
        return Task.cont
    

    def LeftRoll(self, keyDown):
        """ For detecting left roll inputs """
        if keyDown:
            self.taskMgr.add(self.ApplyLeftRoll, 'left-roll')
        else:
            self.taskMgr.remove('left-roll')
    

    def ApplyLeftRoll(self, task):
        """ For applying left roll movement """
        # Rolls one a degree left per frame
        Rate = 1
        self.modelNode.setH(self.modelNode.getH() + Rate)
        return Task.cont
    

    def RightRoll(self, keyDown):
        """ For detecting right roll inputs """
        if keyDown:
            self.taskMgr.add(self.ApplyRightRoll, 'right-roll')
        else:
            self.taskMgr.remove('right-roll')
    

    def ApplyRightRoll(self, task):
        """ For applying right roll movement """
        # Rolls one a degree right per frame
        Rate = -1
        self.modelNode.setH(self.modelNode.getH() + Rate)
        return Task.cont
