# 6/25/25, CSCI-1511, "Project #3" Space Jam Assignment

# Imports
from direct.showbase.ShowBase import ShowBase
import SpaceJamClasses as SpaceJamClasses
import DefensePaths as DefensePaths
import sys

class SpaceJam(ShowBase):
    """ Main Class """

    def __init__(self):
        """ The Constructor """
        # Calls the Constructor to initialize it
        ShowBase.__init__(self)
        # Calls SpaceJamClasses file multiple times to setup & initialize the scene/camera
        self.Universe = SpaceJamClasses.Universe(self.loader, './Assets/Universe/Universe.x', self.render, 'Universe', './Assets/Universe/Starbasesnow.png', (0, 0, 0), 15000)
        self.Planet1 = SpaceJamClasses.Planet(self.loader, './Assets/Planets/protoPlanet.x', self.render, 'Planet1', './Assets/Planets/texture_planet_1.png', (150, 5000, 67), 350)
        self.Planet2 = SpaceJamClasses.Planet(self.loader, './Assets/Planets/protoPlanet.x', self.render, 'Planet2', './Assets/Planets/texture_planet_2.png', (1500, 500, 990), 350)
        self.Planet3 = SpaceJamClasses.Planet(self.loader, './Assets/Planets/protoPlanet.x', self.render, 'Planet3', './Assets/Planets/texture_planet_3.png', (15, 50, 6700), 350)
        self.Planet4 = SpaceJamClasses.Planet(self.loader, './Assets/Planets/protoPlanet.x', self.render, 'Planet4', './Assets/Planets/texture_planet_4.png', (350, -7000, 33), 350)
        self.Planet5 = SpaceJamClasses.Planet(self.loader, './Assets/Planets/protoPlanet.x', self.render, 'Planet5', './Assets/Planets/texture_planet_5.png', (133, 7500, -999), 350)
        self.Planet6 = SpaceJamClasses.Planet(self.loader, './Assets/Planets/protoPlanet.x', self.render, 'Planet6', './Assets/Planets/texture_planet_6.png', (-2000, 50, 300), 350)
        self.SpaceStation = SpaceJamClasses.SpaceStation(self.loader, './Assets/Space Stations/spaceStation.x', self.render, 'Space Station', './Assets/Space Stations/SpaceStation1_Dif2.png', (4567, -934, 123), 40)
        self.Player = SpaceJamClasses.Player(self.loader, './Assets/Spaceships/Dumbledore.x', self.render, 'Player', './Assets/Spaceships/spacejet_C.png', (0, 0, 0), 10)

        # Drones
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
        
        print(SpaceJamClasses.Drones.DroneCount)

        #Controls
        self.SetCamera()
        # Player movement
        SpaceJamClasses.Player.SetKeyBindings(self.Player)
        # Quit game keybind
        self.accept('escape', self.quit)
        
        
    
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
        self.camera.setFluidPos(0, -10, 0)
    

    def quit(self):
        """ Allows for quiting the game """
        sys.exit()


app = SpaceJam()
app.run()