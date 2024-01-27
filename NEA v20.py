# Import necessary libraries
import subprocess
subprocess.check_call(["pip", "install", "pygame_gui"])
subprocess.check_call(["pip", "install", "pygame"])
import pygame as pg 
from pygame.math import Vector2
import os
import math
import pygame_gui

# Initialize pygame
pg.init()

# Set up display
SCREEN_WIDTH = 1050
SCREEN_HEIGHT = 800
FRAME_RATE = 60
    #create clock
clock = pg.time.Clock()
screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pg.display.set_caption("Planet Simulator!")

#Creating fonts
font = pg.font.Font("freesansbold.ttf",18)
font_interact = pg.font.Font("freesansbold.ttf",13)

#More pygame Initialization and Setup:
Button_1_enabled = True
new_press = True
new_input =True

# Initialize UI manager
Manager = pygame_gui.UIManager([SCREEN_WIDTH ,SCREEN_HEIGHT])

# Set up initial configurations
Ui_Refresh_Rate = clock.tick(FRAME_RATE)

# Define planet types and their corresponding images
planet_types = {
    "Earth": "Earth.png", "Mars" : "Mars.png",
    "Uranus" : "Uranus.png", "Jupiter": "Jupiter.png",
    "Saturn" : "Saturn.png", "Mercury" : "Mercury.png",
    "Venus": "Venus.png","Neptune" : "Neptune.png"
}

# Define planet materials and their corresponding images
planet_Mats = {
    "Earth": "EarthMat.png", "Mars" : "MarsMat.png",
    "Uranus" : "UranusMat.png", "Jupiter": "JupiterMat.png",
    "Saturn" : "SaturnMat.png", "Mercury" : "MercuryMat.png",
    "Venus": "VenusMat.png","Neptune" : "NeptuneMat.png"
}

# Define planet material weights (densities)
planet_MatsWeight = {
    "Earth": 5515, "Mars" : 3934 ,
    "Uranus" : 1270 , "Jupiter": 1326 ,
    "Saturn" : 687 , "Mercury" : 5429 ,
    "Venus": 5243 , "Neptune" : 1638
}

# Define the Planet class
class Planet():

    def __init__(self, y ,type, offset,size):
        # Add the instance to the global Planets list
        Planets.append(self)

        self.Ord = Planets.index(self)
        # Add the instance to the global PlanetPos list
        PlanetPos[self.Ord] = self

        # Set initial properties
        self.TagText = Names[self.Ord]
        self.type = type
        self.size = size
        self.y = y
        self.SliderPos = 50
        self.SurfaceGrav = 0
        self.EscapeVel = 0
        self.OrbPeriod = 0
        self.distance = 0
        self.OGoffset = offset
        self.offset = offset
        self.scaleIn_Diameter = 2
        self.scaleOut_Diameter = 24
        self.SizeIn = size
        self.SizeOut = size
        self.slider1Pos = 927
        self.slider2Pos = 927

        # Load planet image
        self.image = pg.image.load(os.path.join('Planets', planet_types[self.type])).convert_alpha()
        self.image = pg.transform.scale_by(self.image, self.size)
        self.width = (self.image.get_width()*self.size)
        self.speed = self.Ord + 5
        self.DegreesPerSecond = 0
        self.angle = self.speed*2
        self.degrees = 0
        self.new_press = True
        self.on = True
        self.active = False
        self.enabled = True

        # Initialize image and position
        self.image_set()
        self.Move()

    # Set image and position based on button/slider states
    def image_set(self):
        self.Order = PlanetPos.index(self)
        if self.Ord == 0:
            self.colour = "Red"
        elif self.Ord == 1:
            self.colour = "Green"
        elif self.Ord == 2:
            self.colour = "Blue"
        elif self.Ord == 3:
            self.colour = "White"
        for i in PlanetPos:
            if i == self:
                Velocitys[self.Order] = self.speed
                if PlanetPos.index(self) == 0:
                    self.x = 375
                elif PlanetPos.index(self) == 1:
                    self.x = 500
                elif PlanetPos.index(self) == 2:
                    self.x = 625
                elif PlanetPos.index(self) == 3:
                    self.x = 750

        self.OGwidth = 146

        if buttonStart.on:
            self.pos = Vector2(500 , 400)
            self.image = pg.image.load(os.path.join('Planets', planet_types[self.type])).convert_alpha()

            self.image = pg.transform.scale_by(self.image, self.SizeIn)
            self.rect = self.image.get_rect(center = (self.x,self.y))
            self.offset = Vector2(0,0)
            self.angle=0

        else:
            self.pos = Vector2(400 , 400)
            self.image = pg.image.load(os.path.join('Planets', planet_types[self.type])).convert_alpha()
            self.image = pg.transform.scale_by(self.image, self.SizeOut)
            self.rect = self.image.get_rect(center = [400 , 400])
            self.width = (self.OGwidth * self.SizeOut)
            self.offset = Vector2( self.OGoffset , 0)
            self.rect.center = self.pos + self.offset.rotate(self.angle)

            pg.draw.circle(screen, "lightblue", self.pos, self.OGoffset, width=2)
            pg.draw.circle(screen,"black",self.rect.center,(self.OGwidth*self.SizeOut)+5)
            pg.draw.circle(screen,self.colour,self.rect.center,(self.OGwidth*self.SizeOut)+5,2)
        screen.blit(self.image, self.rect)

    # Move planet based on angle and speed
    def Move(self):
        # Update angle
        self.angle -= self.speed
        self.degrees = self.angle/360
        if self.degrees< -2:
            self.degrees+=2

        # Add the rotated offset vector to the pos vector to get the rect.center then rotate image
        self.rect.center = self.pos + self.offset.rotate(self.angle)

    #makes it so the user can only look a planet info if the simulation isnt running

    #renders all the information calculated for the planet and the box it is in
    def Tag(self):
        self.Density = "Density(kg/m^3): " + str(planet_MatsWeight[self.type])
        self.Diameter = "Diameters(km): " + str(round((self.OGwidth*self.size)*2321.17))
        self.SurfaceGravity = "Gravity(m/s^2): " + str(self.SurfaceGrav)
        self.EscapeVelocity = "Escape velocity(m/s): " + str(round(self.EscapeVel,1))
        self.OrbitalPeriod = "Orbital Period(Days): " +str(round(self.OrbPeriod,1))
        self.DistanceFromSun = "Distance from Sun(10^6Kg) : \n" +str(round(self.distance,3))

        if buttonStart.on:
            if self.enabled: 
                if self.on :
                    Text = font_interact.render(self.TagText, True , self.colour)
                    if PlanetPos.index(self)% 2 == 0:
                    
                        screen.blit(Text , [self.rect.centerx-len(self.TagText)*3, self.rect.centery+30])
                    else:
                        screen.blit(Text , [self.rect.centerx-len(self.TagText)*3, self.rect.centery-40])


                else:
                    Text = font_interact.render(self.TagText, True , "white")
                    pg.draw.rect(screen, ("lightgreen"), ([self.rect.centerx- 100, self.rect.centery-(210+(self.image.get_height() / 2))],[200,200]))
                    pg.draw.rect(screen, (self.colour), ([self.rect.centerx- 100, self.rect.centery-(210+(self.image.get_height() / 2))],[200,200]),2)
                    screen.blit(font.render(self.TagText, True , "black") , [self.rect.centerx-95, self.rect.centery-(205+(self.image.get_height() / 2))])
                    screen.blit(font_interact.render(self.Density, True , "black") , [self.rect.centerx-95, self.rect.centery-(180+(self.image.get_height() / 2))])
                    screen.blit(font_interact.render(self.Diameter, True , "black") , [self.rect.centerx-95, self.rect.centery-(160+(self.image.get_height() / 2))])
                    screen.blit(font_interact.render(self.SurfaceGravity, True , "black") , [self.rect.centerx-95, self.rect.centery-(140+(self.image.get_height() / 2))])
                    screen.blit(font_interact.render(self.EscapeVelocity, True , "black") , [self.rect.centerx-95, self.rect.centery-(120+(self.image.get_height() / 2))])
                    screen.blit(font_interact.render(self.OrbitalPeriod, True , "black") , [self.rect.centerx-95, self.rect.centery-(100+(self.image.get_height() / 2))])
                    screen.blit(font_interact.render(self.DistanceFromSun, True , "black") , [self.rect.centerx-95, self.rect.centery-(80+(self.image.get_height() / 2))])
                self.new_press_check()



    #checks if the planet has been clicked
    def check_click(self):

        mouse_pos = pg.mouse.get_pos()
        left_click = pg.mouse.get_pressed()[0]
        if left_click and self.rect.collidepoint(mouse_pos) :
            return True
        else:
            return False
    
    #Checks if the button has been clicked previously so if it has it can now be toggled off
    def new_press_check(self):

        if pg.mouse.get_pressed()[0] and self.new_press:
            if self.check_click():
                self.new_press = False
                if self.on :
                    self.on = False
                    for i in Planets:
                        i.enabled = False
                    self.enabled = True
                    

                elif not self.on :
                    self.on = True
                    for i in Planets:
                     i.enabled = True

        elif not pg.mouse.get_pressed()[0] and not self.new_press:
            self.new_press = True
    def Scale_speed(self):
        if not Timebutton1.on:
            self.speed = self.DegreesPerSecond*60
        elif not Timebutton2.on:
            self.speed = self.DegreesPerSecond*3600
        elif not Timebutton3.on:
            self.speed = self.DegreesPerSecond*86400
        else:
            self.speed = self.DegreesPerSecond

    def Scale_size(self):
            self.SizeOut= self.scaleOut_Diameter/self.OGwidth
            self.SizeIn = self.scaleIn_Diameter/self.OGwidth



#Defines a Sun class for simulating the sun on screen for the user
class Sun():
    def __init__(self, pos):
        self.pos = pos
        self.render()
        self.width = self.image.get_width()

    #renders the sun in the correct position, with correct size and with the correct image
    def render(self):
        if buttonStart.on:
            self.pos = [0,400]
            self.image = pg.image.load(os.path.join('Planets', "Sun.png")).convert_alpha()
            #real di = 1.3927 million km, virtual di = 600 so 1 px = 2321.17 km
            self.image = pg.transform.scale(self.image ,(600 ,600))
            self.rect = self.image.get_rect(center = self.pos)
            self.pos = Vector2(self.pos)
            

        elif not buttonStart.on:
            self.pos = [400 , 400]
            self.image = pg.image.load(os.path.join('Planets', "Sun.png")).convert_alpha()
            #real di = 1.3927 million km, virtual di = 50 so 1 px = 27854 km
            self.image = pg.transform.scale(self.image ,(50 ,50))
            self.width = 25
            self.rect = self.image.get_rect(center = self.pos)
            self.pos = Vector2(self.pos)
        screen.blit(self.image, self.rect)


class NewPlanet():
    def __init__(self, y,size, enabled):
        self.x = 935
        self.y = y
        self.size = size
        self.new_press = True
        self.on = True
        self.enabled = enabled
        self.rep = 1

    #renders the button, its text, its different stages and any images it needs
    def make(self):
        if len(Planetbuttons)< 2:
            self.y=645
            self.x = 935 - ((len(Planetbuttons))*110)
        else: 
            self.y =715
            self.x = 935 - ((len(Planetbuttons)-2)*110)
        self.button_rect = pg.rect.Rect((self.x,self.y),(self.size)) 
        #rect = rectangle or sqaure
        self.button_rect = pg.rect.Rect((self.x,self.y),(self.size))    

        if self.enabled:
            pg.draw.rect(screen, "gray" , self.button_rect, 0 , 5)
            pg.draw.rect(screen, "white" , self.button_rect, 2 , 5)

        else:
            #5 at the end is corners rounded off with r of 5 
            pg.draw.rect(screen, "green" , self.button_rect, 0 , 5)
            #border, 2 = edge width
            pg.draw.rect(screen, "light green" ,self.button_rect, 2 ,5)
        self.new_press_check()
        self.check_click()
        screen.blit(font_interact.render("Add Planet!", True , "white"), (self.x + 10 ,self.y + 10))    
    #checks if the button has been clicked
    def check_click(self):
        mouse_pos = pg.mouse.get_pos()
        left_click = pg.mouse.get_pressed()[0]
        if left_click and self.button_rect.collidepoint(mouse_pos) :
            self.enabled = False
        else:
            self.enabled = True
            
        
    def check_click_2(self):

        mouse_pos = pg.mouse.get_pos()
        left_click = pg.mouse.get_pressed()[0]
        if left_click and self.button_rect.collidepoint(mouse_pos) :
            if len(Planetbuttons)<=3:
                planet = Planet( 400 ,Type, 86 , 0.3)
                button1 = UsersPlanets((100,50),enabled)
                DelButton = Delete( 345,(100,15),enabled)
                

            return True
        else:
            self.enabled = True
            return False
    
    #Checks if the button has been clicked previously so if it has it can now be toggled off
    def new_press_check(self):
        self.enabled = True
        if pg.mouse.get_pressed()[0] and self.new_press:
            if self.check_click_2():
                self.new_press = False
                if self.on :
                    self.on = False
                elif not self.on :
                    self.on = True             

        elif not pg.mouse.get_pressed()[0] and not self.new_press:
            
            self.new_press = True


class Delete():
    def __init__(self , y,size, enabled):
        DelButtons.append(self)
        self.x = 935 - (DelButtons.index(self)*110)
        self.y = y
        self.size = size
        self.left_click = False
        self.new_press = True
        self.on = True
        self.enabled = enabled
        self.rep = 1
        self.Ord = DelButtons.index(self)
        self.planet = Planets[self.Ord]

    #renders the button, its text, its different stages and any images it needs
    def make(self):

        #rect = rectangle or sqaure
        if DelButtons.index(self)< 2:
            self.y=695
            self.x = 935 - (DelButtons.index(self)*110)
        else: 
            self.y =765
            self.x = 935 - ((DelButtons.index(self)-2)*110)
        self.button_rect = pg.rect.Rect((self.x,self.y),(self.size))    
        #5 at the end is corners rounded off with r of 5 
        pg.draw.rect(screen, "red" , self.button_rect, 0 , 5)
        #border, 2 = edge width
        pg.draw.rect(screen, "white" ,self.button_rect, 2 ,5)
        self.new_press_check()
            
        
    def check_click_2(self):
        mouse_pos = pg.mouse.get_pos()
        self.left_click = pg.mouse.get_pressed()[0]
        if self.left_click and self.button_rect.collidepoint(mouse_pos) :
            self.enabled = False
            return True
        else:
            self.enabled = True
            self.enabled = False
            return False
    
    #Checks if the button has been clicked previously so if it has it can now be toggled off
    def new_press_check(self):
        self.enabled = True
        if pg.mouse.get_pressed()[0] and self.new_press:
            if self.check_click_2():
                self.new_press = False
                if self.on :
                    self.on = False
                elif not self.on :
                    self.on = True
        
        elif not pg.mouse.get_pressed()[0] and not self.new_press:
            Ord = DelButtons.index(self)
            if Planetbuttons[Ord].on == False:
                    for i in Planetbuttons:
                        i.on = True
                        i.enabled = True
            del DelButtons[Ord]
            del Planetbuttons[Ord]
            Pos1 = Planets[Ord]
            del Planets[Ord]
            Pos2 = PlanetPos.index(Pos1)
            PlanetPos[Pos2] = 0
            Velocitys[Pos2] = 0
            self.new_press = True

class UsersPlanets():
    def __init__(self, size, enabled):
        Planetbuttons.append(self)
        self.Ord = Planetbuttons.index(self)
        self.x = 935 - (Planetbuttons.index(self)*110)
        self.y = 645
        self.text = Planets[self.Ord].TagText
        self.size = size
        self.type = Type
        self.new_press = True
        self.on = True
        self.enabled = enabled
        self.planet = Planets[self.Ord]

    #renders the button, its text, its different stages and any images it needs
    def make(self):

        #rect = rectangle or sqaure
        self.text = Planets[self.Ord].TagText
        if Planetbuttons.index(self)< 2:
            self.y = 645
            self.x = 935 - (Planetbuttons.index(self)*110)
        else: 
            self.y = 715
            self.x = 935 - ((Planetbuttons.index(self)-2)*110)
        self.button_rect = pg.rect.Rect((self.x,self.y),(self.size)) 
           

        if self.enabled:
            if self.on :
                pg.draw.rect(screen, "gray" , self.button_rect, 0 , 5)
                pg.draw.rect(screen, self.planet.colour , self.button_rect, 2 , 5)
                self.planet.active = False

            else:
                #5 at the end is corners rounded off with r of 5 
                pg.draw.rect(screen, "green" , self.button_rect, 0 , 5)
                #border, 2 = edge width
                pg.draw.rect(screen, self.planet.colour  ,self.button_rect, 2 ,5)
                self.planet.active = True
            self.new_press_check()

        else:
            pg.draw.rect(screen, "Red" , self.button_rect, 0 , 5)
            pg.draw.rect(screen, self.planet.colour  , self.button_rect, 2 , 5)
            self.planet.active = False
        
        self.image = pg.image.load(os.path.join('Planets', planet_types[self.planet.type] )).convert_alpha()
        self.image = pg.transform.scale_by(self.image, 0.15)
        width = self.image.get_width()/2

        screen.blit(font_interact.render(self.text, True , "white"), (self.button_rect.centerx - (len(self.text)*3) ,self.button_rect.centery - 20))
        screen.blit(self.image, [self.button_rect.centerx-width,self.button_rect.centery])

            
        
    #checks if the button has been clicked
    def check_click(self):

        self.mouse_pos = pg.mouse.get_pos()
        left_click = pg.mouse.get_pressed()[0]
        if left_click and self.button_rect.collidepoint(self.mouse_pos) :
            return True
        else:
            return False
    
    #Checks if the button has been clicked previously so if it has it can now be toggled off
    def new_press_check(self):

        if pg.mouse.get_pressed()[0] and self.new_press:
            if self.check_click():
                self.new_press = False
                if self.on :
                    self.on = False
                    for i in Planetbuttons:
                        i.enabled = False
                    self.enabled = True
                    for i in DensityButtons:
                        i.planet = self

                elif not self.on :
                    self.on = True
                    for i in Planetbuttons:
                        i.enabled = True
                        i.on = True             

        elif not pg.mouse.get_pressed()[0] and not self.new_press:
            self.new_press = True

#object for toggleable buttons where there is only one option with 2 phases 
class Button_Toggle:
    def __init__(self , text1, text2 , x , y , dis_x, dis_y ):
        self.text1 = text1
        self.text2 = text2
        self.x = x
        self.y = y
        self.dis_x = dis_x
        self.dis_y = dis_y
        self.new_press = True
        self.on = True

    #creates and renders the start button
    def make(self):
        
        button_text_start = font.render(self.text1, True , "white")
        button_text_end = font.render(self.text2, True , "white")
        #rect = rectangle or sqaure
        self.button_rect = pg.rect.Rect((self.x,self.y),(150,25))    


        if self.on:
            pg.draw.rect(screen, "green" , self.button_rect, 0 , 5)
            pg.draw.rect(screen, "white" , self.button_rect, 2 , 5)
            #draw text
            screen.blit(button_text_start, (self.x+self.dis_x ,  self.y+self.dis_y))
        else:
            #5 at the end is corners rounded off with r of 5 
            pg.draw.rect(screen, "Red" , self.button_rect, 0 , 5)
            #border, 2 = edge width
            pg.draw.rect(screen, "white" ,self.button_rect, 2 ,5)
            screen.blit(button_text_end, (self.x+self.dis_x ,  self.y+self.dis_y))
            sun.render()
            for i in Planets:
                i.image_set()
                i.Move()

        self.new_press_check()

    #checks if the button has been clicked    
    def check_click(self):

        mouse_pos = pg.mouse.get_pos()
        left_click = pg.mouse.get_pressed()[0]
        if left_click and self.button_rect.collidepoint(mouse_pos) :
            return True
        else:
            return False
        
    #Checks if the button has been clicked previously so if it has it can now be toggled off
    def new_press_check(self):
        if pg.mouse.get_pressed()[0] and self.new_press:
            if self.check_click():
                self.new_press = False
                if self.on :
                    self.on = False
                elif not self.on :
                    self.on = True
                    
        elif not pg.mouse.get_pressed()[0] and not self.new_press:
            self.new_press = True

#Creates the object used for select buttons where there are multiple options for the user
class SelBut():
    def __init__(self, Mat, x , y,size, enabled,Type):
        self.x = x
        self.y = y
        self.size = size
        self.name = Mat
        self.type = Type
        self.new_press = True
        self.on = True
        self.IsCurrent = False
        if self.type == "Density":
            self.image = pg.image.load(os.path.join('Planet Mats', planet_Mats[Mat])).convert_alpha()
            self.image = pg.transform.scale(self.image,(50,50) )
            self.planet = Planets[0]
        self.enabled = enabled

    #renders the button, its text, its different stages and any images it needs
    def make(self):
        #rect = rectangle or sqaure
        self.button_rect = pg.rect.Rect((self.x,self.y),(self.size))    

        if self.enabled:
            if self.on or not self.check_click:
                pg.draw.rect(screen, "gray" , self.button_rect, 0 , 5)
                pg.draw.rect(screen, "white" , self.button_rect, 2 , 5)

            else:
                #5 at the end is corners rounded off with r of 5 
                pg.draw.rect(screen, "green" , self.button_rect, 0 , 5)
                #border, 2 = edge width
                pg.draw.rect(screen, "light green" ,self.button_rect, 2 ,5)
            if self.IsCurrent:
                self.new_press_check()

        else:
            pg.draw.rect(screen, "Red" , self.button_rect, 0 , 5)
            pg.draw.rect(screen, "white" , self.button_rect, 2 , 5)

        #draw text
        if self.type == "Density":
            screen.blit(self.image , (self.x+25, self.y+15))
            screen.blit(font.render(self.name, True , "white"), (self.x + 30 - (len(self.name)),self.y + 75))
        else:
            screen.blit(font.render(self.name, True , "white"), (self.x + 12 - (len(self.name)),self.y + 5))
        
    #checks if the button has been clicked
    def check_click(self):

        mouse_pos = pg.mouse.get_pos()
        left_click = pg.mouse.get_pressed()[0]
        if left_click and self.button_rect.collidepoint(mouse_pos) :
            return True
        else:
            return False
    
    #Checks if the button has been clicked previously so if it has it can now be toggled off
    def new_press_check(self):

        if pg.mouse.get_pressed()[0] and self.new_press:
            if self.check_click():
                self.new_press = False
                if self.on :
                    self.on = False
                    if Selected:
                        if self.type == "Density":
                            for i in DensityButtons:
                                i.enabled = False
                            Current.type = self.name
                            Current.image_set()
                        self.enabled = True
                    if self.type == "Time":
                        for i in Timebuttons:
                            i.enabled = False
                        self.enabled = True
                    

                elif not self.on :
                    if Selected:
                        self.on = True
                        if self.type == "Density":
                            for i in DensityButtons:
                                i.enabled = True
                    if self.type == "Time":
                        self.on = True
                        for i in Timebuttons:
                            i.enabled = True

        elif not pg.mouse.get_pressed()[0] and not self.new_press:
            self.new_press = True


#defines the slider class so it can be used in the program as an object
class Slider():
    def __init__(self,pos,size,initial_value , min , max ):
        self.pos = pos
        self.size = size

        self.SliderLeftPos = self.pos[0] - (self.size[0]/2)
        self.IntLeftPos = self.SliderLeftPos + 2
        self.SliderRightPos = self.pos[0] + (self.size[0]/2)
        self.SliderTopPos = self.pos[1] - (self.size[1]/2)
        self.IntTopPos = self.SliderTopPos - 9

        self.initial_value = (self.SliderRightPos-self.SliderLeftPos) * initial_value
        self.min = min 
        self.max = max

        self.Container_rect = pg.Rect(self.SliderLeftPos, self.SliderTopPos, self.size[0], self.size[1])
        self.InteractArea_rect = pg.Rect(self.IntLeftPos, self.IntTopPos, self.size[0] - 4, self.size[1] * 5)
        self.button_rect = pg.Rect(self.SliderLeftPos + self.initial_value - 5 , self.SliderTopPos - 7, 15 ,self.size[1] * 4)

        self.render()
        
    #once the slider button is clicked this makes sure the button is moved to where the mouse drags it
    def MoveSlider(self,mouse_pos):

        if self.min == 0.01:
            Current.slider1Pos = mouse_pos[0]
        else:
            Current.slider2Pos = mouse_pos[0]

        self.render()

    #creates the slider and renders it
    def render(self):
        if Selected:
            if self.min == 0.01:
                self.button_rect.centerx = Current.slider1Pos
            else:
                self.button_rect.centerx = Current.slider2Pos
        pg.draw.rect(screen,"lightgrey", self.Container_rect)
        pg.draw.rect(screen,"red", self.button_rect, 0 , 5)
        self.D= round(self.GetVal(),1)
        if self.max == 3.5e5:
            self.DText = str(self.D)
            self.DForm = font.render(self.DText, True , "green")
            screen.blit(self.DForm, (self.button_rect.centerx-(len(self.DText*3)), self.button_rect.centery-20))

        else:
            self.DText = str(self.D)+ "x10^24"
            self.DForm = font.render(self.DText, True , "green")
            screen.blit(self.DForm, (self.button_rect.centerx-(len(self.DText*3)), self.button_rect.centery-20))

    #checks if the slider button has been selected/clicked
    def check_click(self):
        mouse_pos = pg.mouse.get_pos()
        left_click = pg.mouse.get_pressed()[0]
        if left_click and self.button_rect.collidepoint(mouse_pos) and self.InteractArea_rect.collidepoint(mouse_pos) :
            self.MoveSlider(mouse_pos)
        else:
            return False
        
    #gets the value of the slider
    def GetVal(self):
        ValRange = self.SliderRightPos - self.SliderLeftPos -3
        ButtonVal = self.button_rect.centerx - self. SliderLeftPos 

        return(ButtonVal/ValRange)*(self.max-self.min)+self.min


#function the creates and renders all the text and aesthetic boxes 
def UI():
    Mass = font_interact.render("Mass(kg):", True , "Black")
    Velocity = font_interact.render("Velocity(m/s): ", True , "Black")
    Name = font_interact.render("Planet Name:", True , "Black")
    if buttonStart.on:
        scale = font_interact.render("Scale: 1pxl = 2321.2km" , True , "white")
    else:
        scale = font_interact.render("Scale: 1pxl = 27854km" , True , "white")
    pg.draw.rect(screen, ("white") ,(800 ,0 , 250 ,800))
    pg.draw.rect(screen, ("royalblue1") ,(820 ,5 , 220 ,45))
    pg.draw.rect(screen, ("royalblue1") ,(820 ,60 , 220 ,50))
    pg.draw.rect(screen, ("royalblue1") ,(820 ,120 , 220 ,50))
    pg.draw.rect(screen, ("royalblue1") ,(820 ,180 , 220 ,445))
    pg.draw.rect(screen, ("royalblue1") ,(820 ,637 , 220 ,150))
    pg.draw.rect(screen, ("royalblue1") ,(325 ,625 , 150 ,175))
    pg.draw.rect(screen, ("white") ,(325 ,625 , 150 ,175),3)
    screen.blit(font_interact.render("Time Scale:", True , "Black"),(362,  650))
    screen.blit(font_interact.render("Density(Kg/m^3): ", True , "Black"),(830,  185))
    screen.blit(Name,(830,  10))
    screen.blit(Mass,(830,  65))
    screen.blit(Velocity,(830,  125))
    screen.blit(scale, (5,780))

#Calculates the distance between the centre of the sun and the centre of the planet
def DistanceCalc(MSun,VPlanet,G,):
    Distance = (G* MSun )/(VPlanet **2)
    # distance is in m not km
    scale_distance = Distance/1000
    virtual_distance =  (scale_distance /27854) 
    #makes sure the distance is large enough that the planets don't intersect.
    Current.OGoffset = int(virtual_distance )
    Current.image_set()
    return Distance

#Function that calculates the scale factor that the original image needs to be multiplid by
def size(Mass,Density):
    Volume = (Mass*10e24)/Density
    Diameter= (((6*Volume)/math.pi)**(1/3))/1000
    Current.scaleOut_Diameter = Diameter/27854
    Current.scaleIn_Diameter = Diameter/2321.17
    return Diameter

#Function for calculating scaled velocity based on orbit size and time period
def ScaleVelocityCalc(Velocity,Distance):
    Velocity= Velocity/1000
    DegreesPerSecond= (360 * Velocity) / (2*math.pi*Distance)
    Current.DegreesPerSecond = DegreesPerSecond

#Surface gravity calculating function
def SurfaceGrav(Density,Diameter):
    GravTop = 4*math.pi*GravitationalConstant*Density*(Diameter/2)
    SurfaceGravity = (GravTop/3)*1000
    Current.SurfaceGrav=round(SurfaceGravity,2)

#Escape velocity calculation function
def EscVel():
    EscapeVelocity_Squrd = (2*(GravitationalConstant)*(Mass*10e24))/((Diameter*1000)/2)
    EscapeVelocity = math.sqrt(EscapeVelocity_Squrd)
    Current.EscapeVel = EscapeVelocity
 
#Orbital Period calculation function
def OrbPeriod():
    Current.OrbPeriod = (360/ Current.DegreesPerSecond)/ 86400

def bubbleSort(arr):
    n = len(arr)
    # optimize code, so if the array is already sorted, it doesn't need
    # to go through the entire process
    swapped = False
    # Traverse through all array elements
    for i in range(n-1):

        for j in range(0, n-i-1):
 
            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            if arr[j] < arr[j + 1]:
                swapped = True
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                PlanetPos[j],PlanetPos[j+1] = PlanetPos[j+1],PlanetPos[j]
         
        if not swapped:

            return
run = True
Selected = False

screen_rect = screen.get_rect()

#Creates nessasry constants for the maths
GravitationalConstant = 6.67430e-11
MSun = 1.98e30
speed = 1

#Creates start values for the planet so hey can start with something on the screen

TagText = ""
Type = "Earth"

#Puts all planets in group
    # List to store planet objects and their corresponding buttons
Planets=[]
Planetbuttons =[]
DelButtons = []
# List to store planet ordered positions
PlanetPos = [0,0,0,0]
    # List to store orbital velocities, so the planets can be sorted by velocity
Velocitys= [0,0,0,0]

#sets the starter names for the planets 
Names = ["Planet 1","Planet 2","Planet 3","Planet 4"]

#creates instances of the sliders
slider1 = Slider([925,97], [190,5], 0.5 , 0.01 ,100 )
slider2 = Slider([925,157], [190,5], 0.5 , 1.1e5 ,3.5e5)

enabled = True

#creating and grouping buttons

NewPlanetButton = NewPlanet(670,(100,50),enabled)

Timebutton1 = SelBut("Per Minute", 350, 670,(100,30),enabled,"Time")
Timebutton2 = SelBut("Per Hour", 350, 700,(100,30),enabled,"Time")
Timebutton3 = SelBut("Per Day" ,350, 730,(100,30),enabled,"Time")
Timebuttons = [Timebutton1, Timebutton2, Timebutton3]

buttonStart = Button_Toggle("Start", "Stop", 10, 10, 45 , 3 )

#creates and instance of the sun and planet then putting them on the UI
planet1 = Planet( 400 ,Type, 86 , 0.3)
SelectPlanet1 = UsersPlanets((100,50),enabled)
SelectPlanet1.on = False
DelPlanet1= Delete( 345,(100,15),enabled)

sun = Sun([400 , 400])

button1 = SelBut("Earth", 825, 205,(100,100),enabled,"Density")
button2 = SelBut("Mars", 935, 205,(100,100),enabled,"Density")
button3 = SelBut("Venus" ,825, 310,(100,100),enabled,"Density")
button4 = SelBut("Mercury" ,935, 310,(100,100),enabled,"Density")
button5 = SelBut("Jupiter" ,825, 415,(100,100),enabled,"Density")
button6 = SelBut("Saturn" ,935, 415,(100,100),enabled,"Density")
button7 = SelBut("Uranus" ,825, 520,(100,100),enabled,"Density")
button8 = SelBut("Neptune" ,935, 520,(100,100),enabled,"Density")
DensityButtons =[button1, button2, button3,button4,button5,button6,button7,button8]

#renders and creates the text box
NameInput = pygame_gui.elements.UITextEntryLine(relative_rect=pg.Rect([820,23],[220,25]), manager = Manager, object_id = "#main_text_entry")    

#Main Game Loop
while run:
    Selected = False
    bubbleSort(Velocitys)
    for i in Planets:
        if i.active:
            Selected = True
            Current = i
            for i in DensityButtons:
                i.IsCurrent = True
            for i in Timebuttons:
                i.IsCurrent = True
                
    screen.fill("black")
    sun.render()

    if Selected:
        VPlanet = slider2.GetVal()
        Mass = slider1.GetVal()

    #User Interface Rendering and Update
    UI()
    
    slider1.check_click()
    slider1.render()
    slider2.check_click()
    slider2.render()
    buttonStart.make()
    if len(Planetbuttons) <=3:
        NewPlanetButton.make()

    
    #Runnung and updating information calculation for the current planet 
    if Selected:

        Distance = DistanceCalc(MSun, VPlanet , GravitationalConstant)
        Current.distance = Distance/10e6
        Diameter = size(Mass, planet_MatsWeight[Current.type])
        ScaleVelocity =ScaleVelocityCalc(VPlanet,Distance)
        SurfaceGravity = SurfaceGrav(planet_MatsWeight[Current.type],Diameter)
        EscVel()
        OrbPeriod()

    else:
        for i in DensityButtons:
            i.on = True
            i.enabled = True

    
    #Event Handling and Update
    for event in pg.event.get():

        if event.type == pg.QUIT:
            run = False
        
        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == "#main_text_entry":
            TagText = event.text

        Manager.process_events(event)

    #making sure the planet name is within length boundaries 
    if Selected:
        if len(TagText)<=20:
            if not TagText == "":
                Current.TagText = TagText
                NameInput.clear()
                TagText = ""
            else:
                Current.TagText = Current.TagText
        if not NewPlanetButton.enabled and len(Planetbuttons) <4 :
            for i in DensityButtons:
                i.on = True
                i.enabled = True

    
    for i in DensityButtons:
        i.make()
    for i in Timebuttons:
        i.make()
    for i in Planetbuttons:
        i.make()
    for i in DelButtons:
        i.make()
    for i in Planets:
        i.image_set()
        i.Scale_speed()
        i.Scale_size()
        i.Tag()


    #Display Update and Frame Rate Control
    Manager.update(Ui_Refresh_Rate)

    Manager.draw_ui(screen)

    clock.tick(FRAME_RATE)
    pg.display.flip()

#game cleanup
pg.quit()