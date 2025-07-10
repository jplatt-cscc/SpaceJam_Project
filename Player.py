from panda3d.core import *
from direct.task import Task
from direct.task.Task import TaskManager
from Collisions import SphereCollider
from typing import Callable
from SpaceJamClasses import Missile
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.LerpInterval import LerpFunc
from direct.particles.ParticleEffect import ParticleEffect
# Regex module for editing strings
import re


class Ship(SphereCollider):
    """ For loading the player model """
    def __init__(self, loader: Loader, taskMgr: TaskManager, accept: Callable[[str, Callable], None], modelPath: str, parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3, scaleVec: float):
        super(Ship, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0.3, 0, 0), 1.5)
        self.taskMgr = taskMgr
        self.accept = accept
        self.render = parentNode
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setName(nodeName)
        Texture = loader.loadTexture(texPath)
        self.modelNode.setTexture(Texture, 1)
        # Missile projectile
        self.loader = loader
        self.reloadTime = 0.25
        # Missile Variables
        self.ExplodeCount = 0
        self.explodeIntervals = {}
        self.traverser = CollisionTraverser()
        self.handler = CollisionHandlerEvent()
        # Distance where the missile disapears
        self.missileDistance = 4000
        # Launch only 1 missile at a time
        self.missileBay = 1
        # Missile Collision Detection
        self.taskMgr.add(self.CheckIntervals, 'checkMissiles', 30)
        self.handler.addInPattern('into')
        self.accept('into', self.HandleInto)


    def HandleInto(self, entry):
        """ Debuging info for collisions """
        fromNode = entry.getFromNodePath().getName()
        print('fromNode: ' + fromNode)
        intoNode = entry.getIntoNodePath().getName()
        print('intoNode: ' + intoNode)
        intoPosition = Vec3(entry.getSurfacePoint(self.render))
        tempVar = fromNode.split('_')
        print('tempVar1: ' + str(tempVar))
        shooter = intoNode.split('_')
        print('shooter: ' + str(shooter))
        tempVar = fromNode.split('_')
        print('tempVar2: ' + str(tempVar))
        tempVar = fromNode.split('_')
        print('tempVar3: ' + str(tempVar))
        victim = tempVar[0]
        print('victim: ' + str(victim))
        pattern = r'[0-9]'
        strippedString = re.sub(pattern, '', victim)
        if (strippedString == 'Drone' or strippedString == 'Planet' or strippedString == 'Space Station'):
            print(victim + ' hit at ' + intoPosition)
            self.DestroyObject(victim, intoPosition)
        print(shooter + ' is DONE.')
        Missile.intervals[shooter].finish()
    

    def DestroyObject(self, hitID, hitPosition):
        # Finds what the missile hit
        nodeID = self.render.find(hitID)
        nodeID.detachNode()
        # Starts explosion
        self.explodeNode.setPos(hitPosition)
        self.Explode()


    def Explode(self):
        """ Explosion animation """
        self.ExplodeCount += 1
        tag = 'particles-' + str(self.ExplodeCount)
        self.explodeIntervals[tag] = LerpFunc(self.ExplodeLight, duration = 4.0)
        self.explodeIntervals[tag].start()


    def ExplodeLight(self, t):
        if t == 1.0 and self.explodeEffect:
            self.explodeEffect.disable()
        elif t == 0:
            self.explodeEffect.start(self.explodeNode)
    

    def SetParticles(self):
        self.enableParticles()
        self.explodeEffect = ParticleEffect()
        self.explodeEffect.loadConfig('./Assets/Effects/basic_xpld_efx.ptf')
        self.explodeEffect.setScale(20)
        self.explodeNode = self.render.attachNewNode('ExplosionEffects')


    def EnableHUD(self):
        """ Crosshair for firing the missile """
        self.HUD = OnscreenImage(image = './Assets/HUD/techno.png', pos = Vec3(0, 0, -0.03), scale = 0.05)
        self.HUD.setTransparency(TransparencyAttrib.MAlpha)


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
        self.accept('f', self.Fire)


    def Fire(self):
        """ For firing the missile """
        if self.missileBay:
            travRate = self.missileDistance
            # Get the front of the Ship
            aim = self.render.getRelativeVector(self.modelNode, Vec3.down())
            aim.normalize()
            fireSolution = aim * travRate
            # Missile spawns 100 units infront of the Ship
            infront = aim * 100
            posVec = self.modelNode.getPos() + infront
            travVec = fireSolution + self.modelNode.getPos()
            # Only 1 missile can be fired at a time
            self.missileBay -= 1
            missileTag = 'Missile' + str(Missile.missileCount)
            # Loads the missile model
            currentMissile = Missile(self.loader, './Assets/Phaser/phaser.egg', self.render, missileTag, posVec, 4.0)
            # Collider Reference
            self.traverser.addCollider(currentMissile.collisionNode, self.handler)
            # 'fluid = 1' checks collions between frames so it doesn't phase through things
            Missile.intervals[missileTag] = currentMissile.modelNode.posInterval(2.0, travVec, startPos = posVec, fluid = 1)
            Missile.intervals[missileTag].start()
        else:
            # If not already reloading
            if not self.taskMgr.hasTaskNamed('reload'):
                print('Initializing reload...')
                # Call the reload method
                self.taskMgr.doMethodLater(0, self.Reload, 'reload')
                return Task
            

    def Reload(self, task):
        if task.time > self.reloadTime:
            self.missileBay += 1
            # Debug
            print('Done reloading')
            return Task.done
        # Safety check
        if self.missileBay > 1:
            self.missileBay = 1
        elif task.time <= self.reloadTime:
            print('Reload processing...')
            return Task.cont

    def CheckIntervals(self, task):
        for i in Missile.intervals:
            # 'isPlaying' returns True or False if the missile has reached the end of its path/life
            if not Missile.intervals[i].isPlaying():
                # Gets rid of the missile
                Missile.cNodes[i].detachNode()
                Missile.fireModels[i].detachNode()
                del Missile.intervals[i]
                del Missile.fireModels[i]
                del Missile.cNodes[i]
                del Missile.collisionSolids[i]
                print(i + ' has reached the end of its path.')
                # 'break' fixes the dictionary after things are deleted from it
                break
        return Task.cont



    def Thrust(self, keyDown):
        """ For detecting forward movement inputs """
        if keyDown:
            self.taskMgr.add(self.ApplyThrust, 'forward-thrust')
        else:
            self.taskMgr.remove('forward-thrust')
    

    def ApplyThrust(self, task):
        """ For applying forward movement """
        Rate = 15
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
        self.modelNode.setR(self.modelNode, Rate)
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
        self.modelNode.setR(self.modelNode, Rate)
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
        self.modelNode.setP(self.modelNode, Rate)
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
        self.modelNode.setP(self.modelNode, Rate)
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
        self.modelNode.setH(self.modelNode, Rate)
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
        self.modelNode.setH(self.modelNode, Rate)
        return Task.cont
