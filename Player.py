from panda3d.core import *
from direct.task import Task
from direct.task.Task import TaskManager
from Collisions import SphereCollider
from typing import Callable
from SpaceJamClasses import Missile
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
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
        # Boost mode
        self.thrustRate = 0
        self.boostTime = 4
        self.boostOn = False
        # For launching the missiles from the wing tips
        self.missileLeft = self.modelNode.attachNewNode('missileLeft')
        self.missileRight = self.modelNode.attachNewNode('missileRight')
        self.missileLeft.setPos(-5, -3, 0)
        self.missileRight.setPos(4, -2.4, 0)
        # Missile projectile
        self.loader = loader
        self.reloadTime = 0.25
        # Missile Variables
        self.ExplodeCount = 0
        self.explodeIntervals = {}
        self.traverser = CollisionTraverser()
        self.StartTraverserTask()
        self.handler = CollisionHandlerEvent()
        self.SetParticles()
        # Distance where the missile disapears
        self.missileDistance = 4000
        # Launch only 1 missile at a time
        self.missileBay = 4
        # Missile Collision Detection
        self.taskMgr.add(self.CheckIntervals, 'checkMissiles', 30)
        self.handler.addInPattern('into')
        self.accept('into', self.HandleInto)
        # Enables/inits HUD
        self.EnableHUD()


    def StartTraverserTask(self):
        self.taskMgr.add(self.TraverserAddTask, 'collisionTask')


    def TraverserAddTask(self, task):
        self.traverser.traverse(self.render)
        return Task.cont


    def HandleInto(self, entry):
        """ Debuging info for collisions """
        fromNode = entry.getFromNodePath().getName()
        print('fromNode: ' + fromNode)
        intoNode = entry.getIntoNodePath().getName()
        print('intoNode: ' + intoNode)
        intoPosition = Vec3(entry.getSurfacePoint(self.render))
        tempVar = fromNode.split('_')
        print('tempVar1: ' + str(tempVar))
        shooter = tempVar[0]
        print('shooter: ' + str(shooter))
        tempVar = intoNode.split('_')
        print('tempVar2: ' + str(tempVar))
        tempVar = intoNode.split('_')
        print('tempVar3: ' + str(tempVar))
        victim = tempVar[0]
        print('victim: ' + str(victim))
        pattern = r'[0-9]'
        strippedString = re.sub(pattern, '', victim)
        if (strippedString == 'Drone' or strippedString == 'Planet' or strippedString == 'Space Station'):
            print(str(victim) + ' hit at ' + str(intoPosition))
            self.DestroyObject(victim, intoPosition)
        print(shooter + ' is DONE.')
        #Missile.intervals[shooter].finish()
    

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
        base.enableParticles()
        self.explodeEffect = ParticleEffect()
        self.explodeEffect.loadConfig('./Assets/Effects/basic_xpld_efx.ptf')
        self.explodeEffect.setScale(20)
        self.explodeNode = self.render.attachNewNode('ExplosionEffects')


    def EnableHUD(self):
        """ Crosshair for firing the missile """
        self.crossHair = OnscreenImage(image = './Assets/HUD/techno.png', pos = Vec3(0, 0, -0.04), scale = 0.05)
        self.crossHair.setTransparency(TransparencyAttrib.MAlpha)
        self.missileHUD = OnscreenImage(image = './Assets/HUD/missilebay4.png', pos = Vec3(-0.9, 0, -0.87), scale = 0.15)
        self.missileHUD.setTransparency(TransparencyAttrib.MAlpha)
        self.boostHUD = OnscreenImage(image = './Assets/HUD/BoostOff.png', pos = Vec3(0.9, 0, -0.89), scale = 0.10)
        self.speedHUD = OnscreenText(text = f'Ship Speed: {self.thrustRate}', pos = (0, -0.86), scale = 0.07, style = 3)
        self.taskMgr.add(self.shipSpeed, 'ship-speed')
    

    def shipSpeed(self, task):
        self.speedHUD.destroy()
        self.speedHUD = OnscreenText(text = f'Ship Speed: {self.thrustRate}', pos = (0, -0.86), scale = 0.07, style = 3)
        return Task.cont


    def SetKeyBindings(self):
        """ For setting player movement keybinds """
        # '.getH' for left/right turns | '.getP' for up/down turns | '.getR' for left/right rolls
        self.accept('w', self.Thrust, [1])
        self.accept('w-up', self.Thrust, [0])
        self.accept('s', self.Reverse, [1])
        self.accept('s-up', self.Reverse, [0])
        self.accept('a', self.LeftRoll, [1])
        self.accept('a-up', self.LeftRoll, [0])
        self.accept('d', self.RightRoll, [1])
        self.accept('d-up', self.RightRoll, [0])
        self.accept('space', self.Launch)
        self.accept('shift', self.BoostMode)    


    def mouseInit(self):
        """ Initialize mouse tracking """
        self.taskMgr.add(self.mouseTracking, 'mouse-movement')
    

    def mouseTracking(self, task):
        """ Player/camera movement via the mouse """
        if base.mouseWatcherNode.hasMouse():
            mousePos = base.win.getPointer(0)
            x = mousePos.getX()
            y = mousePos.getY()
            # Divide by 2 to get the center of the screen
            screenX = int(base.win.getXSize() / 2)
            screenY = int(base.win.getYSize() / 2)
            deltaX = x - screenX
            deltaY = y - screenY
            self.modelNode.setP(self.modelNode, -deltaY * 0.05)
            self.modelNode.setR(self.modelNode, -deltaX * 0.05)
            base.win.movePointer(0, screenX, screenY)
        return Task.cont

    
    def Launch(self):
        if self.missileBay:
            self.taskMgr.doMethodLater(0, self.Fire, 'Left-Missile')
            self.taskMgr.doMethodLater(0.1, self.Fire, 'Right-Missile')
        else:
            # If not already reloading
            if not self.taskMgr.hasTaskNamed('reload'):
                print('Initializing reload...')
                # Call the reload method
                self.taskMgr.doMethodLater(0, self.Reload, 'reload')
                return Task


    def Fire(self, task):
        """ For firing the missile """
        travRate = self.missileDistance
        # Get the front of the Ship
        aim = self.render.getRelativeVector(self.modelNode, Vec3.down())
        aim.normalize()
        fireSolution = aim * travRate
        # Missile spawns 100 units infront of the Ship
        infront = aim * 100
        posVec = self.missileLeft.getPos(self.render) + infront
        if self.missileBay == 3 or self.missileBay == 1:
            posVec = self.missileRight.getPos(self.render) + infront
            self.missileHUD.setImage('./Assets/HUD/missilebay2.png')
            self.missileHUD.setTransparency(TransparencyAttrib.MAlpha)
        travVec = fireSolution + self.modelNode.getPos()
        # Only 1 missile can be fired at a time
        self.missileBay -= 1
        if self.missileBay == 0:
            self.missileHUD.destroy()
        missileTag = 'Missile' + str(Missile.missileCount)
        # Loads the missile model
        currentMissile = Missile(self.loader, './Assets/Phaser/phaser.egg', self.render, missileTag, posVec, 4.0)
        # Collider Reference
        self.traverser.addCollider(currentMissile.collisionNode, self.handler)
        # 'fluid = 1' checks collions between frames so it doesn't phase through things
        Missile.intervals[missileTag] = currentMissile.modelNode.posInterval(2.0, travVec, startPos = posVec, fluid = 1)
        Missile.intervals[missileTag].start()
        Task.done
            

    def Reload(self, task):
        if task.time > self.reloadTime:
            self.missileBay += 4
            self.missileHUD = OnscreenImage(image = './Assets/HUD/missilebay4.png', pos = Vec3(-0.9, 0, -0.87), scale = 0.15)
            self.missileHUD.setTransparency(TransparencyAttrib.MAlpha)
            # Debug
            print('Done reloading')
            return Task.done
        # Safety check
        if self.missileBay > 4:
            self.missileBay = 4
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


    def BoostMode(self):
        if not self.boostOn:
            self.boostOn = True
            self.boostHUD.setImage('./Assets/HUD/BoostOn.png')
            self.boostHUD.setTransparency(TransparencyAttrib.MAlpha)
            print('Boost Mode Activated')
            self.taskMgr.doMethodLater(0, self.Boost, 'Boost-Mode')
            self.taskMgr.doMethodLater(1, self.Boost, 'Boost-Mode')
            self.taskMgr.doMethodLater(2, self.Boost, 'Boost-Mode')
            self.taskMgr.doMethodLater(3, self.Boost, 'Boost-Mode')
            self.taskMgr.doMethodLater(10, self.BoostReactivate, 'Reactivate-Boost-Mode')
        else:
            print('Boost Mode Already Acivated... Try again in 10 seconds...')


    def Boost(self, task):
        self.thrustRate += 15
        self.boostTime -= 1
        if self.boostTime == 0:
            print('Boost Mode Deactivated')
            self.thrustRate = 10
            self.boostTime = 4
            self.boostHUD.setImage('./Assets/HUD/BoostCooldown.png')
            self.boostHUD.setTransparency(TransparencyAttrib.MAlpha)
        print('Speed: ' + str(self.thrustRate))
        return Task.done


    def BoostReactivate(self, task):
        self.boostOn = False
        self.boostHUD.setImage('./Assets/HUD/BoostOff.png')
        self.boostHUD.setTransparency(TransparencyAttrib.MAlpha)
        return Task.done
    

    def Thrust(self, keyDown):
        """ For detecting forward movement inputs """
        if keyDown:
            self.taskMgr.add(self.ApplyThrust, 'forward-thrust')
            self.thrustRate += 10
            self.speedHUD.destroy()
            self.speedHUD = OnscreenText(text = f'Ship Speed: {self.thrustRate}', pos = (0, -0.86), scale = 0.07, style = 3)
        else:
            self.thrustRate = 0
            self.taskMgr.remove('forward-thrust')
    

    def ApplyThrust(self, task):
        """ For applying forward movement """
        Trajectory = self.render.getRelativeVector(self.modelNode, Vec3.down())
        Trajectory.normalize()
        self.modelNode.setFluidPos(self.modelNode.getPos() + Trajectory * self.thrustRate)
        return Task.cont

    def Reverse(self, keyDown):
        """ For detecting backwards movement inputs """
        if keyDown:
            self.taskMgr.add(self.ApplyReverse, 'backwards-thrust')
            self.thrustRate += 10
        else:
            self.thrustRate = 0
            self.taskMgr.remove('backwards-thrust')
    

    def ApplyReverse(self, task):
        """ For applying backwards movement """
        Trajectory = self.render.getRelativeVector(self.modelNode, Vec3.down())
        Trajectory.normalize()
        self.modelNode.setFluidPos(self.modelNode.getPos() - Trajectory * self.thrustRate)
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
