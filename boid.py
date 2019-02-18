# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 09:44:06 2019

@author: install
"""


import numpy as np

def set_mag(vector, new_mag):
    mag = np.linalg.norm(vector)
    vx = vector[0] * (new_mag/mag)
    vy = vector[1] * (new_mag/mag)
    return np.array([vx,vy])

def limit_mag(vector, max_mag):
    if np.linalg.norm(vector) > max_mag:
        return(set_mag(vector, max_mag))
    else:
        return(vector)

class Boid:
    def __init__(self, display_width = 800, display_height = 600):
        
        self.display_width = display_width
        self.display_height = display_height
        
        self.position = np.hstack([np.random.randint(0,self.display_width), np.random.randint(0, self.display_height)])        
        self.max_force = 0.3
        self.max_speed = 5
        self.perception = 50
        self.velocity = np.random.uniform(-2,2,2)
        self.acceleration = np.zeros(2)
        
        
    def update(self):
          
        self.position = self.position + self.velocity
        self.velocity = self.velocity + self.acceleration
        self.velocity = limit_mag(self.velocity, self.max_speed)
        
    
    def flock(self, boids):    
        
       
        neigbours = []
        for boid in boids:
            if boid != self and np.linalg.norm(boid.position - self.position) < self.perception:
                neigbours.append(boid)
        
        
        alignment = self.align(neigbours)
        cohesion = self.cohesion(neigbours)
        separation = self.separation(neigbours)
        
        self.acceleration += alignment
        self.acceleration += cohesion
        self.acceleration += separation        
        
        self.velocity += self.acceleration
        self.velocity = limit_mag(self.velocity, self.max_speed)
        self.position = self.position + self.velocity
        self.edges()
        self.acceleration *= 0
        
    
    def align(self, neighbours):
        steering = np.zeros(2)
        if len(neighbours) > 0:
            steering = np.zeros(2)
            for boid in neighbours:
                steering += boid.velocity
            
            steering = steering / len(neighbours)
            steering = set_mag(steering, self.max_speed)
            steering -= self.velocity
            steering = limit_mag(steering, self.max_force)
        
        return(steering)
    
    
    def cohesion(self, neighbours):
        steering = np.zeros(2)
        if len(neighbours) > 0:
            for boid in neighbours:
                steering += boid.position
                
            steering = steering / len(neighbours)
            steering = steering - self.position
            steering = set_mag(steering, self.max_speed)
            steering -= self.velocity
            steering = limit_mag(steering, self.max_force)
        return(steering)
    
    def separation(self, neighbours):
        steering = np.zeros(2)
        if len(neighbours) > 0:
            for boid in neighbours:
                diff = self.position - boid.position
                diff = diff / (np.linalg.norm(self.position - boid.position)**2)
                
                steering += diff
            
            steering = steering / len(neighbours)
            steering = set_mag(steering, self.max_speed)
            steering -= self.velocity
            steering = limit_mag(steering, self.max_force)
        return(steering)
        
        
    def edges(self):
        for i, p in zip([0,1], [self.display_width,self.display_height]):
            if self.position[i] < 0:
                self.position[i] = p
            elif self.position[i] > p:
                self.position[i] = 0