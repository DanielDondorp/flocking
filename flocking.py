# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 09:28:39 2019

@author: install
"""


import pygame
import sys
from boid import Boid
from boid import Pboid

pygame.init()


class Simulation:
    def __init__(self):
        self.display_width = 400
        self.display_height = 300
        
        self.display = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption("Simulation")
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.boids = [Boid(display_width=self.display_width, display_height=self.display_height) for x in range(100)]
        self.pboids = [Pboid(display_width=self.display_width, display_height=self.display_height) for x in range(3)]
        
    def run(self):
        
        while self.running:
        
            self.display.fill((0,0,0))
            
            #draw boids:
            for boid in self.boids:
                if not boid.alive:
                    self.boids.remove(boid)
                else:
                    try:
                        
                        pygame.draw.circle(self.display, (255,255,255), (int(boid.position[0]), int(boid.position[1])), int(2))
                        boid.update()
                        boid.flock(self.boids, self.pboids)
                    except Exception as e:
                        print(boid.position, boid.velocity, boid.acceleration, e)
                
                
                
            for pboid in self.pboids:
                pygame.draw.circle(self.display, (255,0,127), (int(pboid.position[0]), int(pboid.position[1])), int(5))
                pboid.update()
                pboid.flock(self.boids,self.pboids)
#            
            #Make closing out possible
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            pygame.display.update()
            self.clock.tick(15)
            
            sys.stdout.write("\r fps: "+str(self.clock.get_fps()))
        #when self.running set to False.
        pygame.quit()
    
if __name__ == "__main__":
    simulation = Simulation()
    simulation.run()
    
    