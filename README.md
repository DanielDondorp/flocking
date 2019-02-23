# flocking
simulation of flocking boids in numpy and pygame

A simple implementation of Craig Reynolds flocking boids in python, with the addition of predators. 


https://en.wikipedia.org/wiki/Boids

dependencies: numpy, pygame.

Run flocking.py to see the simulation.



Some notes to save with this project

1. Make predatory boids work together by adding some cohesion and separation behaviour.
2. Move distance calculations to the simulation class and do it once per simulation loop instead of once per updated boid. Huge optimizing step.
3. Perhaps never, but interesting to combine this with the genetic algorithm project and introduce evolution into the simulation. I wonder if with you'd get the fitness of populations in antiphase.
