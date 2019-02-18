# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 09:28:39 2019

@author: install
"""


import pygame
from boid import Boid

pygame.init()


class Simulation:
    def __init__(self):
        self.display_width = 800
        self.display_height = 600
        
        self.display = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption("Simulation")
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.boids = [Boid() for x in range(100)]
        
    def run(self):
        
        while self.running:
        
            self.display.fill((0,0,0))
            
            #draw boids:
            for boid in self.boids:
                pygame.draw.circle(self.display, (255,255,255), (int(boid.position[0]), int(boid.position[1])), int(2))
                boid.update()
                boid.flock(self.boids)

            
            #Make closing out possible
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            pygame.display.update()
            self.clock.tick(60)
        
        #when self.running set to False.
        pygame.quit()
    
if __name__ == "__main__":
    simulation = Simulation()
    simulation.run()
    
    