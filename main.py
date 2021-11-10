import pygame
import math
import numpy as np

class Planet:

    def __init__(self, mass, position, init_velocity, img_file, id):
        self.mass = mass
        self.position = position
        self.current_velocity = np.array(init_velocity)
        self.img = pygame.image.load(img_file)
        self.id = id

    def update_position(self, time_step):
        self.position += self.current_velocity * time_step

    def update_velocity(self, all_planets, time_step):
        for planet in all_planets:
            if planet != self:

                delta_x = planet.position[0] - self.position[0]
                delta_y = planet.position[1] - self.position[1]

                sqr_dist = delta_x**2 + delta_y**2
                distance = math.sqrt(sqr_dist)

                # Divide by distance to turn it into a unit vector
                force_dir = np.array([delta_x/distance, delta_y/distance])

                force_vector = np.array([(force_dir[0] * GRAV_CONSTANT * self.mass * planet.mass / sqr_dist),
                                         (force_dir[1] * GRAV_CONSTANT * self.mass * planet.mass / sqr_dist)])
                accel_vector = np.array([force_vector[0]/self.mass, force_vector[1]/self.mass])

                force = math.sqrt(force_vector[0]**2 + force_vector[1]**2)
                acceleration = float(force / self.mass)

                print(self.id)
                print("--------")
                print("OV = " + str(self.current_velocity))
                print("DELTA V = ", str(accel_vector*time_step))

                self.current_velocity += accel_vector*time_step


                print("FORCE VECTOR = " + str(force_vector))
                print("ACCEL VECTOR = " + str(accel_vector))
                # print("FORCE = " + str(force))
                print("CV = " + str(self.current_velocity))

size = width, height = 1200, 900
BLACK = (0, 0, 0)
GRAV_CONSTANT = 9.8

pygame.init()
screen = pygame.display.set_mode((size))
pygame.display.set_caption('Solar System')
clock = pygame.time.Clock()

planets = set()
bluePlanet = Planet(10000, [400, 350], [float(0), float(0)], 'planet_img/bluePlanet.png', 'BLUE')
redPlanet = Planet(400, [200, 700], [float(0),float(0)], 'planet_img/redPlanet.png', 'RED')
planets.add(bluePlanet)
planets.add(redPlanet)

def draw():
    screen.fill(BLACK)

    for planet in planets:
        planet.update_velocity(planets, time_step)
        planet.update_position(time_step)
        screen.blit(planet.img, planet.position)


time_step = 1
quit = False
while not quit:

    draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.WINDOWCLOSE:
            quit = True

    clock.tick(20)

    pygame.display.update()

pygame.display.quit()
pygame.quit()