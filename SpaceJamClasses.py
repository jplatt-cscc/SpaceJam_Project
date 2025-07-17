from panda3d.core import *
from direct.task import Task
from direct.task.Task import TaskManager
from Collisions import *
from typing import Callable
import DefensePaths as DefensePaths


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
        super(Universe, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 0.95)
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
        self.modelNode.setFluidPos(posVec)
        self.modelNode.setScale(scaleVec)
        Missile.missileCount += 1
        Missile.fireModels[nodeName] = self.modelNode
        Missile.cNodes[nodeName] = self.collisionNode
        # Debuging
        Missile.collisionSolids[nodeName] = self.collisionNode.node().getSolid(0)
        Missile.cNodes[nodeName].show()
        print('Fire Missile #' + str(Missile.missileCount))


class Orbiter(SphereCollider):
    """ For the moving drones/sentinals """
    numOrbits = 0
    veloctity = 0.01
    cloudTimer = 240

    def __init__(self, loader: Loader, taskMgr: TaskManager, modelPath: str, parentNode: NodePath, nodeName: str, scaleVec: Vec3, texPath: str, centralObject: PlacedObject, orbitRadius: float, orbitType: str, staringAt: Vec3):
        super(Orbiter, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 3.2)
        self.taskMgr = taskMgr
        self.orbitType = orbitType
        self.modelNode.setScale(scaleVec)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)
        self.orbitObject = centralObject
        self.orbitRadius = orbitRadius
        self.staringAt = staringAt
        Orbiter.numOrbits += 1
        self.cloudClock = 0

        self.taskFlag = 'Traveler-' + str(Orbiter.numOrbits)
        self.taskMgr.add(self.Orbit, self.taskFlag)


    def Orbit(self, task):
        if self.orbitType == 'MLB':
            positionVec = DefensePaths.BaseballSeams(task.time * Orbiter.veloctity, self.numOrbits, 2.0)
            self.modelNode.setPos(positionVec * self.orbitRadius + self.orbitObject.modelNode.getPos())
        
        elif self.orbitType == 'Cloud':
            if self.cloudClock < Orbiter.cloudTimer:
                self.cloudClock += 1

            else:
                self.cloudClock = 0
                positionVec = DefensePaths.Cloud()
                self.modelNode.setPos(positionVec * self.orbitRadius + self.orbitObject.modelNode.getPos())

        self.modelNode.lookAt(self.staringAt.modelNode)
        return task.cont        
