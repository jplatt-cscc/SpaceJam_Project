# 6/12/25, CSCI-1511, "Project #2" Space Jam Assignment

# Imports
from direct.showbase.ShowBase import ShowBase
import SpaceJamClasses as SpaceJamClasses
import DefensePaths as DefensePaths

class SpaceJam(ShowBase):
    """ Main Class """

    def __init__(self):
        """ The Constructor """
        # Calls the Constructor to initialize it
        ShowBase.__init__(self)
        # Calls SpaceJamClasses file multiple times to setup & initialize the scene/camera
        self.Universe = SpaceJamClasses.Universe(self.loader, './Assets/Universe/Universe.x', self.render, 'Universe', './Assets/Universe/Starbasesnow.png', (0, 0, 0), 15000)
        self.Planet1 = SpaceJamClasses.Planet(self.loader, './Assets/Planets/protoPlanet.x', self.render, 'Planet1', './Assets/Planets/texture_planet_1.png', (150, 5000, 67), 350)
        self.Planet2 = SpaceJamClasses.Planet(self.loader, './Assets/Planets/protoPlanet.x', self.render, 'Planet2', './Assets/Planets/texture_planet_2.png', (1500, 500, 99), 350)
        self.Planet3 = SpaceJamClasses.Planet(self.loader, './Assets/Planets/protoPlanet.x', self.render, 'Planet3', './Assets/Planets/texture_planet_3.png', (15, 50, 670), 350)
        self.Planet4 = SpaceJamClasses.Planet(self.loader, './Assets/Planets/protoPlanet.x', self.render, 'Planet4', './Assets/Planets/texture_planet_4.png', (350, -7000, 33), 350)
        self.Planet5 = SpaceJamClasses.Planet(self.loader, './Assets/Planets/protoPlanet.x', self.render, 'Planet5', './Assets/Planets/texture_planet_5.png', (133, 750, -999), 350)
        self.Planet6 = SpaceJamClasses.Planet(self.loader, './Assets/Planets/protoPlanet.x', self.render, 'Planet6', './Assets/Planets/texture_planet_6.png', (-2000, 5, 300), 350)
        self.SpaceStation = SpaceJamClasses.SpaceStation(self.loader, './Assets/Space Stations/spaceStation.x', self.render, 'Space Station', './Assets/Space Stations/SpaceStation1_Dif2.png', (4567, -934, 123), 40)
        self.Player = SpaceJamClasses.Player(self.loader, './Assets/Spaceships/Dumbledore.x', self.render, 'Player', './Assets/Spaceships/spacejet_C.png', (0, 0, 0), 50)

        # Drones
        FullCycle = 60
        for j in range(FullCycle):
            SpaceJamClasses.Drones.DroneCount += 1
            NickName = 'Drone' + str(SpaceJamClasses.Drones.DroneCount)
            self.DrawCloudDefense(self.Planet1, NickName)
            self.DrawBaseballSeams(self.SpaceStation, NickName, j, FullCycle, 2)
        
    
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


app = SpaceJam()
app.run()