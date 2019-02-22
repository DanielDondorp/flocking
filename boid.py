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
    def __init__(self, display_width = 400, display_height = 300):
        
        self.display_width = display_width
        self.display_height = display_height
        
        self.position = np.hstack([np.random.randint(0,self.display_width), np.random.randint(0, self.display_height)])        
        self.max_force = 0.5
        self.max_speed = 4
        self.min_speed = 0.1
        self.perception = 20
        self.predator_perception = 15
        self.velocity = np.random.uniform(-2,2,2)
        self.acceleration = np.zeros(2)
        self.alive = True
        
    def update(self):
        
        self.velocity += self.acceleration
        self.position = self.position + self.velocity
        self.velocity = self.velocity + self.acceleration
        self.velocity = limit_mag(self.velocity, self.max_speed)
        self.edges()
        self.acceleration *= 0
    
    def flock(self, boids, pboids):    
        
        neigbours = []
        for boid in boids:
            if boid != self and np.linalg.norm(boid.position - self.position) < self.perception:
                neigbours.append(boid)
        
        
        alignment = self.align(neigbours)
        cohesion = self.cohesion(neigbours)
        cohesion *= 1.1
        separation = self.separation(neigbours)
        fleeing = self.run_away(pboids)
        
        self.acceleration += alignment
        self.acceleration += cohesion
        self.acceleration += separation
        self.acceleration += fleeing
        
        self.acceleration = limit_mag(self.acceleration, self.max_force)        
        

        
        
    
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
    
    def run_away(self, pboids):
        p_close = []
        for boid in pboids:
            if boid != self and np.linalg.norm(boid.position - self.position) < self.predator_perception:
                p_close.append(boid)
        steering = self.separation(p_close)
        steering = steering * 1.5
        return(steering)
    def die(self):
        pass
        
        
    def edges(self):
        for i, p in zip([0,1], [self.display_width,self.display_height]):
            if self.position[i] < 0:
                self.position[i] = p
            elif self.position[i] > p:
                self.position[i] = 0


class Pboid(Boid):
    def __init__(self, **kw):
        Boid.__init__(self, **kw)
        self.perception = 10
        self.max_force = 1
        self.max_speed = 3.8
    
    def flock(self, boids, pboids):    
        neigbours = []
        for boid in boids:
            if boid != self and np.linalg.norm(boid.position - self.position) < self.perception:
                neigbours.append(boid)
                
        alignment = self.align(neigbours)
        cohesion = self.cohesion(neigbours)
#        cohesion *= 1.3
#        separation = self.separation(neigbours)
#        fleeing = self.run_away(pboids)        
        self.acceleration += alignment
        self.acceleration += cohesion
        self.acceleration += -(set_mag(self.velocity, np.linalg.norm(self.velocity)/100))
#        self.acceleration += separation
#        self.acceleration += fleeing
        
        self.acceleration = limit_mag(self.acceleration, self.max_force)   
        
    def cohesion(self, neighbours):
        steering = np.zeros(2)
        #find closest boid
        if len(neighbours) > 0:
            dists = [np.linalg.norm(boid.position - self.position) for boid in neighbours]

            closest = neighbours[np.argmin(dists)]
            if np.min(dists) < 3:
                closest.alive = False
                closest.die()
            steering = closest.position
            steering = steering - self.position
            steering = set_mag(steering, self.max_speed)
            steering -= self.velocity
            steering = limit_mag(steering, self.max_force)
        return(steering)
