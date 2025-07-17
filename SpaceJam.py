# 7/17/25, CSCI-1551, "Project #7" Space Jam Assignment

# Imports
from direct.showbase.ShowBase import ShowBase
from panda3d.core import CollisionTraverser, CollisionHandlerPusher
import SpaceJamClasses as SpaceJamClasses
import DefensePaths as DefensePaths
import Player as PlayerClass
import sys


class SpaceJam(ShowBase):
    """ Main Class """

    def __init__(self):
        """ The Constructor """
        # Calls the Constructor to initialize it
        ShowBase.__init__(self)

        # Loads models/scene
        self.SetScene()
        PlayerClass.Ship.EnableHUD(self)

        # Spawns drones
        self.SpawnDrones()
        print(f'Drone Count: {SpaceJamClasses.Drones.DroneCount}')

        #Controls
        self.SetCamera()
        # Player movement
        PlayerClass.Ship.SetKeyBindings(self.Player)
        # Quit game keybind
        self.accept('escape', self.quit)

        # Collisions
        self.cTrav = CollisionTraverser()
        self.cTrav.traverse(self.render)
        self.pusher = CollisionHandlerPusher()
        self.pusher.addCollider(self.Player.collisionNode, self.Player.modelNode)
        self.cTrav.addCollider(self.Player.collisionNode, self.pusher)
        # Debug Option
        self.cTrav.showCollisions(self.render)


    def SetScene(self):
        """ Calls SpaceJamClasses file multiple times to setup & initialize the scene/camera """
        self.Universe = SpaceJamClasses.Universe(self.loader, './Assets/Universe/Universe.x', self.render, 'Universe', './Assets/Universe/Starbasesnow.png', (0, 0, 0), 15000)
        self.Planet1 = SpaceJamClasses.Planet(self.loader, './Assets/Planets/protoPlanet.x', self.render, 'Planet1', './Assets/Planets/texture_planet_1.jpg', (150, 5000, 67), 350)
        self.Planet2 = SpaceJamClasses.Planet(self.loader, './Assets/Planets/protoPlanet.x', self.render, 'Planet2', './Assets/Planets/texture_planet_2.jpg', (1500, 500, 990), 350)
        self.Planet3 = SpaceJamClasses.Planet(self.loader, './Assets/Planets/protoPlanet.x', self.render, 'Planet3', './Assets/Planets/texture_planet_3.jpg', (15, 50, 6700), 350)
        self.Planet4 = SpaceJamClasses.Planet(self.loader, './Assets/Planets/protoPlanet.x', self.render, 'Planet4', './Assets/Planets/texture_planet_4.jpg', (350, -7000, 33), 350)
        self.Planet5 = SpaceJamClasses.Planet(self.loader, './Assets/Planets/protoPlanet.x', self.render, 'Planet5', './Assets/Planets/texture_planet_5.jpg', (133, 7500, -999), 350)
        self.Planet6 = SpaceJamClasses.Planet(self.loader, './Assets/Planets/protoPlanet.x', self.render, 'Planet6', './Assets/Planets/texture_planet_6.jpg', (-2000, 50, 300), 350)
        self.SpaceStation = SpaceJamClasses.SpaceStation(self.loader, './Assets/Space Stations/spaceStation.x', self.render, 'Space Station', './Assets/Space Stations/SpaceStation1_Dif2.png', (4567, -934, 123), 40)
        self.Player = PlayerClass.Ship(self.loader, self.taskMgr, self.accept, './Assets/Spaceships/Dumbledore.x', self.render, 'Player', './Assets/Spaceships/spacejet_C.png', (0, 0, 0), 10)
        self.Sentinal1 = SpaceJamClasses.Orbiter(self.loader, self.taskMgr, './Assets/Drone Defender/DroneDefender.obj', self.render, 'Drone', 10.0, './Assets/Drone Defender/octotoad1_auv.png', self.Planet5, 900, 'MLB', self.Player)
        self.Sentinal2 = SpaceJamClasses.Orbiter(self.loader, self.taskMgr, './Assets/Drone Defender/DroneDefender.obj', self.render, 'Drone', 10.0, './Assets/Drone Defender/octotoad1_auv.png', self.Planet2, 500, 'Cloud', self.Player)


    def SpawnDrones(self):
        """ Spawns all drones/drone patterns """
        FullCycle = 60
        x = 0
        for i in range(FullCycle):
            NickName = 'Drone' + str(SpaceJamClasses.Drones.DroneCount)
            self.DrawCloudDefense(self.Planet1, NickName)
            SpaceJamClasses.Drones.DroneCount += 1
            self.DrawCloudDefense(self.Planet2, NickName)
            SpaceJamClasses.Drones.DroneCount += 1
            self.DrawCloudDefense(self.Planet3, NickName)
            SpaceJamClasses.Drones.DroneCount += 1
            self.DrawCloudDefense(self.Planet4, NickName)
            SpaceJamClasses.Drones.DroneCount += 1
            self.DrawCloudDefense(self.Planet5, NickName)
            SpaceJamClasses.Drones.DroneCount += 1
            self.DrawCloudDefense(self.Planet6, NickName)
            SpaceJamClasses.Drones.DroneCount += 1
            self.DrawBaseballSeams(self.SpaceStation, NickName, i, FullCycle, 2)
            SpaceJamClasses.Drones.DroneCount += 1
            self.DrawCircleY(x, NickName)
            SpaceJamClasses.Drones.DroneCount += 1
            self.DrawCircleX(x, NickName)
            SpaceJamClasses.Drones.DroneCount += 1
            self.DrawCircleZ(x, NickName)
            SpaceJamClasses.Drones.DroneCount += 1
            x = x + 0.105
            # Added to DroneCount multiple times because otherwise it only counts 1 per loop no matter how many are spawned
        
    
    def DrawBaseballSeams(self, centralObject, droneName, step, numSeams, radius = 1):
        UnitVector = DefensePaths.BaseballSeams(step, numSeams, B = 0.4)
        UnitVector.normalize()
        position = UnitVector * radius * 250 + centralObject.modelNode.getPos()
        SpaceJamClasses.Drones(self.loader, './Assets/Drone Defender/DroneDefender.obj', self.render, droneName, './Assets/Drone Defender/octotoad1_auv.png', position, 5)


    def DrawCloudDefense(self, centralObject, droneName):
        UnitVector = DefensePaths.Cloud()
        UnitVector.normalize()
        position = UnitVector * 500 + centralObject.modelNode.getPos()
        SpaceJamClasses.Drones(self.loader, './Assets/Drone Defender/DroneDefender.obj', self.render, droneName, './Assets/Drone Defender/octotoad1_auv.png', position, 10)

    
    def DrawCircleY(self, x, droneName):
        UnitVector = DefensePaths.CircleY(x)
        UnitVector.normalize()
        position = UnitVector * 100
        SpaceJamClasses.Drones(self.loader, './Assets/Drone Defender/DroneDefender.obj', self.render, droneName, './Assets/Drone Defender/blue.jpg', position, 1)

    
    def DrawCircleX(self, x, droneName):
        UnitVector = DefensePaths.CircleX(x)
        UnitVector.normalize()
        position = UnitVector * 100
        SpaceJamClasses.Drones(self.loader, './Assets/Drone Defender/DroneDefender.obj', self.render, droneName, './Assets/Drone Defender/red.jpg', position, 1)


    def DrawCircleZ(self, x, droneName):
        UnitVector = DefensePaths.CircleZ(x)
        UnitVector.normalize()
        position = UnitVector * 100
        SpaceJamClasses.Drones(self.loader, './Assets/Drone Defender/DroneDefender.obj', self.render, droneName, './Assets/Drone Defender/green.jpg', position, 1)
    

    def SetCamera(self):
        """ Sets player camera """
        self.disableMouse()
        self.camera.reparentTo(self.Player.modelNode)
        # Sets the camera behind the ship's engines
        self.camera.setFluidPos(0.3, 1, 10)
        self.camera.setHpr(180, -90, -180)
    

    def quit(self):
        """ Allows for quiting the game """
        sys.exit()


app = SpaceJam()
app.run()