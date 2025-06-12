# 6/12/25, CSCI-1511, "Project #1" Space Jam Assignment

# Imports
from direct.showbase.ShowBase import ShowBase

class SpaceJam(ShowBase):
    """ Main Class """

    def __init__(self):
        """ The Constructor """
        # Calls the Constructor to initialize it
        ShowBase.__init__(self)
        # Calls the Scene function to initialize the scene/camera
        self.Scene()


    def Scene(self):
        """ Loads and sets up the scene """
        # Universe | https://opengameart.org/content/perfectly-seamless-night-sky
        # Universe model & texture
        self.Universe = self.loader.loadModel('./Assets/Universe/Universe.x')
        UniverseText = self.loader.loadTexture('./Assets/Universe/Starbasesnow.png')
        self.Universe.setTexture(UniverseText, 1)
        self.Universe.reparentTo(self.render)
        self.Universe.setScale(15000)
        # Planets | https://opengameart.org/content/gas-giants-430003000 | https://opengameart.org/content/planets-satellites-4x3000x3000-2
        # Planet #1 model & texture
        self.Planet1 = self.loader.loadModel('./Assets/Planets/protoPlanet.x')
        self.Planet1.reparentTo(self.render)
        self.Planet1.setPos(150, 5000, 67)
        self.Planet1.setScale(350)
        Planet1Text = self.loader.loadTexture('./Assets/Planets/texture_planet_1.png')
        self.Planet1.setTexture(Planet1Text, 1)
        # Planet #2 model & texture
        self.Planet2 = self.loader.loadModel('./Assets/Planets/protoPlanet.x')
        self.Planet2.reparentTo(self.render)
        self.Planet2.setPos(1500, 500, 99)
        self.Planet2.setScale(350)
        Planet2Text = self.loader.loadTexture('./Assets/Planets/texture_planet_2.png')
        self.Planet2.setTexture(Planet2Text, 1)
        # Planet #3 model & texture
        self.Planet3 = self.loader.loadModel('./Assets/Planets/protoPlanet.x')
        self.Planet3.reparentTo(self.render)
        self.Planet3.setPos(15, 50, 670)
        self.Planet3.setScale(350)
        Planet3Text = self.loader.loadTexture('./Assets/Planets/texture_planet_3.png')
        self.Planet3.setTexture(Planet3Text, 1)
        # Planet #4 model & texture
        self.Planet4 = self.loader.loadModel('./Assets/Planets/protoPlanet.x')
        self.Planet4.reparentTo(self.render)
        self.Planet4.setPos(350, -7000, 33)
        self.Planet4.setScale(350)
        Planet4Text = self.loader.loadTexture('./Assets/Planets/texture_planet_4.png')
        self.Planet4.setTexture(Planet4Text, 1)
        # Planet #5 model & texture
        self.Planet5 = self.loader.loadModel('./Assets/Planets/protoPlanet.x')
        self.Planet5.reparentTo(self.render)
        self.Planet5.setPos(133, 750, -999)
        self.Planet5.setScale(350)
        Planet5Text = self.loader.loadTexture('./Assets/Planets/texture_planet_5.png')
        self.Planet5.setTexture(Planet5Text, 1)
        # Planet #6 model & texture
        self.Planet6 = self.loader.loadModel('./Assets/Planets/protoPlanet.x')
        self.Planet6.reparentTo(self.render)
        self.Planet6.setPos(-2000, 5, 300)
        self.Planet6.setScale(350)
        Planet6Text = self.loader.loadTexture('./Assets/Planets/texture_planet_6.png')
        self.Planet6.setTexture(Planet6Text, 1)
        # Space Station
        # Space Station model & texture
        self.SpaceStation = self.loader.loadModel('./Assets/Space Stations/spaceStation.x')
        SpaceStationText = self.loader.loadTexture('./Assets/Space Stations/SpaceStation1_Dif2.png')
        self.SpaceStation.setTexture(SpaceStationText, 1)
        self.SpaceStation.setPos(4567, -934, 123)
        self.SpaceStation.setScale(250)
        self.SpaceStation.reparentTo(self.render)
        # Player
        # Space Ship model & texture
        self.Player = self.loader.loadModel('./Assets/Spaceships/Dumbledore.x')
        PlayerText = self.loader.loadTexture('./Assets/Spaceships/spacejet_C.png')
        self.Player.setTexture(PlayerText, 1)
        self.Player.setScale(50)
        self.Player.reparentTo(self.render)


app = SpaceJam()
app.run()