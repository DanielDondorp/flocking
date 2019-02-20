# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 09:28:39 2019

@author: install
"""


import pygame
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
        
        self.boids = [Boid() for x in range(50)]
        self.pboids = [Pboid() for x in range(3)]
        
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
                        print(boid.position, boids.velocity, boid.acceleration, e)
                
                
                
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
            self.clock.tick(60)
        
        #when self.running set to False.
        pygame.quit()
    
if __name__ == "__main__":
    simulation = Simulation()
    simulation.run()
    
    