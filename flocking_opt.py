# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 20:22:55 2019

@author: install
"""


import pygame
import sys
import numpy as np
from boid_opt import Boid
#from boid import Pboid
import pandas as pd


pygame.init()


class Simulation:
    def __init__(self):
        self.display_width = 800
        self.display_height = 600
        self.framerate = 30
        
        self.display = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption("Simulation")
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.boids = [Boid(display_width=self.display_width, display_height=self.display_height) for x in range(100)]
#        self.pboids = [Pboid(display_width=self.display_width, display_height=self.display_height) for x in range(4)]
        self.boids = np.array(self.boids)
    def run(self):
        
        while self.running:
            
            self.display.fill((0,0,0))
            
            #draw boids:
            self.positions = np.zeros(2)
            for boid in self.boids:
                self.positions = np.vstack([self.positions, boid.position])
                try:
                    pygame.draw.circle(self.display, (255,255,255), (int(boid.position[0]), int(boid.position[1])), int(2))
                except:
                    pass
            self.positions = self.positions[1:]
            for boid in self.boids:
                boid.flock(self.boids, self.positions)
                boid.update()
            
            #Make closing out possible
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            pygame.display.update()
            self.clock.tick(self.framerate)
            
            sys.stdout.write("\r fps: "+str(np.round(self.clock.get_fps()))+" Boids left: "+str(len(self.boids)))
        #when self.running set to False.
        pygame.quit()
    
if __name__ == "__main__":
    simulation = Simulation()
    simulation.run()
    