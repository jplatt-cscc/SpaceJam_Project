from panda3d.core import *
from direct.task import Task
from direct.task.Task import TaskManager
from Collisions import *
from typing import Callable


class Planet(SphereCollider):
    """ For loading planet models """
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super(Planet, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 1.1)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setName(nodeName)
        Texture = loader.loadTexture(texPath)
        self.modelNode.setTexture(Texture, 1)


class Drones(SphereCollider):
    """ For loading drone models """
    # Counts how many drones have spawned
    DroneCount = 0

    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super(Drones, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 1.2)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setName(nodeName)
        Texture = loader.loadTexture(texPath)
        self.modelNode.setTexture(Texture, 1)


class Universe(InverseSphereCollider):
    """ For loading the universe model """
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super(Universe, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 1.0)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setName(nodeName)
        Texture = loader.loadTexture(texPath)
        self.modelNode.setTexture(Texture, 1)


class SpaceStation(CapsuleCollider):
    """ For loading the space station model """
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super(SpaceStation, self).__init__(loader, modelPath, parentNode, nodeName, 1, -1, 5, 1, -1, -5, 10)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setName(nodeName)
        Texture = loader.loadTexture(texPath)
        self.modelNode.setTexture(Texture, 1)


class Missile(SphereCollider):
    """ For loading the missile model """
    fireModels = {}
    cNodes = {}
    collisionSolids = {}
    intervals = {}
    missileCount = 0
    
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, posVec: Vec3, scaleVec: float = 1.0):
        super(Missile, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 3.0)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        Missile.missileCount += 1
        Missile.fireModels[nodeName] = self.modelNode
        Missile.cNodes[nodeName] = self.collisionNode
        # Debuging
        Missile.collisionSolids[nodeName] = self.collisionNode.node().getSolid(0)
        Missile.cNodes[nodeName].show()
        print('Fire Missile #' + str(Missile.missileCount))
