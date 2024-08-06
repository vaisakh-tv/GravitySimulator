# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 14:15:21 2024

@author: VTV01
"""
import numpy as np
import sys
import pygame

class Colors:
    def __init__(self):
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.black = (0,0,0)   

class sun:
    def __init__(self, mass,location):
        self.mass = mass
        self.G = 10
        self.location = location
        self.velocity = np.zeros(2)
        self.dt = 0.01
        
    def move(self,plnts):
        '''if len(plnts) > 0:
            F = np.zeros(2)
            for p in plnts:
                r = np.linalg.norm(self.location - p.location);# print(r)
                F = F + -self.G*p.mass*self.mass*(self.location - p.location)/(r**3); #print(F)
            a = F/self.mass; #print(a)
            self.velocity = self.velocity + a*self.dt; #print(self.velocity)
            
        else:
            self.velocity = np.zeros(2)
            
        self.location = self.location + self.velocity*self.dt'''
        pass
        
class planet:
    def __init__(self, location, velocity):
        self.location = np.array(location)
        self.mass = 50
        self.velocity = np.array(velocity)
        self.G = 10
        self.dt = 0.01
        self.c = Colors()  
        self.color = np.random.randint(10,255,3) #colorArray[np.random.randint(0,len(colorArray))]
        self.tail = []


        
        
    def move(self, suns):
        self.tail.append(self.location)
        if len(self.tail) > 30:
            self.tail.pop(0)
        F = np.zeros(2)
        for s in suns:
            r = np.linalg.norm(self.location - s.location);# print(r)
            F = F + -self.G*s.mass*self.mass*(self.location - s.location)/(r**3); #print(F)
        a = F/self.mass; #print(a)
        self.velocity = self.velocity + a*self.dt; #print(self.velocity)
        self.location = self.location + self.velocity*self.dt

class planetarySystem:
    def __init__(self):   
        ## Initialize Pygame
        pygame.init()
        
        #Initialize Parameters of the simulation
        self.FrameRate = 120
        self.screenFactor = 10
        self.sunMass = 1000
        #---------------------------------------
        
        # Set up colors
        self.color = Colors()
        
        # Set up display
        self.width = self.height = 800 #self.count*self.circle_radius*2*self.spacing
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("--- Planetary System ---")
        self.screen.fill(self.color.white)
    
       
    
        # Set up clock
        self.clock = pygame.time.Clock()
        
    def getPos_n_Velocity(self,pos1, pos2):
        r = np.array([pos1[0] - self.width/2, pos1[1] - self.height/2])/self.screenFactor
        v = -np.array([pos2[0] - pos1[0], pos2[1] - pos1[1]] )/self.screenFactor   
        return r, v
    
    def drawPlanet(self, plnt):
        x = plnt.location[0]*self.screenFactor + self.width/2
        y =  self.height/2 + plnt.location[1]*self.screenFactor
        radius = 5
        for sun in self.sunArray:
            if np.linalg.norm(plnt.location - sun.location) < 1.5:
                self.planetArray.remove(plnt)
                
        if x < 0 or x > self.width:
            self.planetArray.remove(plnt)
            #print("opt 1")
        elif y < 0 or y > self.height:
            self.planetArray.remove(plnt)
            #print("opt 2")
        #elif abs(plnt.location[0]) < 1.5 and abs(plnt.location[1]) < 1.5:
            #print("opt 3")
            #self.planetArray.remove(plnt)
        else:   
            pygame.draw.circle(self.screen, plnt.color, (x,y), radius)
            for i, t in enumerate(plnt.tail):
                x = t[0]*self.screenFactor + self.width/2
                y =  self.height/2 + t[1]*self.screenFactor
                pygame.draw.circle(self.screen, plnt.color, (x,y), radius*i/30)
                
                
    def drawSuns(self, s):
        x = s.location[0]*self.screenFactor + self.width/2
        y =  self.height/2 + s.location[1]*self.screenFactor
        radius = 15
        
        color = self.color.black
        if s.mass < 0:
            color = self.color.red

            
        pygame.draw.circle(self.screen, color, (x,y), radius)
            
        
    def drawCount(self):
         # Set up font
         self.font = pygame.font.SysFont("Arial", 20)  # You can replace 'None' with a specific font file path

         # Set up text
         self.text = str(len(self.planetArray))
         self.text_render = self.font.render(self.text, True, self.color.black)
         
         # Set up text position
         self.text_rect = self.text_render.get_rect()
         self.text_rect.center = (50, 50)
         
         # Draw the text
         self.screen.blit(self.text_render, self.text_rect)
        
        
    def run(self):
        # Main game loop
        pos1 = (0,0); pos2 = (0,0)
        sunPos = (0,0)
        running = True
        holding = False
        self.planetArray = []
        self.sunArray = [sun(self.sunMass, np.zeros(2))]
        
        # Fill the background with white
        self.screen.fill(self.color.white)
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.planetArray.clear()
                        self.sunArray.clear()
                        
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos1 = (event.pos[0],event.pos[1])
                        holding = True
                    elif event.button == 3:
                        if pygame.key.get_mods() & pygame.KMOD_CTRL:
                            sunPos = (event.pos[0],event.pos[1])
                            r, v = self.getPos_n_Velocity(sunPos, (0,0))
                            self.sunArray.append(sun(-self.sunMass, r))
                            
                        else:
                            sunPos = (event.pos[0],event.pos[1])
                            r, v = self.getPos_n_Velocity(sunPos, (0,0))
                            self.sunArray.append(sun(self.sunMass, r))
                        
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        pos2 = (event.pos[0],event.pos[1])                       
                        r, v = self.getPos_n_Velocity(pos1, pos2)
                        p = planet(r,v)
                        self.planetArray.append(p)
                        holding = False
                        
                        

            # Fill the background with white
            self.screen.fill(self.color.white)
            
            if holding:
                x, y = pygame.mouse.get_pos()
                d1 = (pos1[0] - x )
                d2 = (pos1[1] - y )
                
                x1 = pos1[0] + d1
                y1 = pos1[1] + d2
                pygame.draw.aaline(self.screen, self.color.red, pos1, (x1,y1)  , 1)
                pygame.draw.circle(self.screen, self.color.red, pos1, 5)

            for p in self.planetArray:
                p.move(self.sunArray)
                self.drawPlanet(p)
                
            for s in self.sunArray:
                s.move(self.planetArray)
                self.drawSuns(s)
                
            
            self.drawCount()
            
            # Update the display
            pygame.display.flip()
            
            # Cap the frame rate
            self.clock.tick(self.FrameRate)
            
        # Quit Pygame
        pygame.quit()
        sys.exit()


if __name__ =="__main__":            
    a = planetarySystem()
    a.run()