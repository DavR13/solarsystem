import pygame
import math
import numpy as np


class Planet:

    def __init__(self, mass, position, init_velocity, img_file):
        self.mass = mass
        self.position = position
        self.current_velocity = np.array(init_velocity)
        self.img = pygame.image.load(img_file)
        self.radius = self.img.get_width()

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
                self.current_velocity += accel_vector * time_step

    def is_collision(self, all_planets):
        for planet in all_planets:
            if planet != self:
                delta_x = planet.position[0] - self.position[0]
                delta_y = planet.position[1] - self.position[1]

                sqr_dist = delta_x**2 + delta_y**2
                distance = math.sqrt(sqr_dist)

                if distance < min(planet.radius, self.radius):
                    return True

        return False


DISPLAY_SIZE = DISPLAY_WIDTH, DISPLAY_HEIGHT = 1200, 900
BLACK = (0, 0, 0)
GRAV_CONSTANT = 9.8
TIME_STEP = 1

pygame.init()
screen = pygame.display.set_mode(DISPLAY_SIZE)
pygame.display.set_caption('Solar System')
clock = pygame.time.Clock()


def draw(planets):

    screen.fill(BLACK)
    for planet in planets:
        update(planets)
        screen.blit(planet.img, planet.position)


def update(planets):

    for planet in planets:
        planet.update_velocity(planets, TIME_STEP)
        planet.update_position(TIME_STEP)


def game_loop():

    planets = set()
    blue_planet = Planet(10000, [400, 350], [float(0), float(0)], 'planet_img/bluePlanet.png')
    red_planet = Planet(400, [200, 700], [float(-7), float(-10)], 'planet_img/redPlanet.png')
    planets.add(blue_planet)
    planets.add(red_planet)

    game_exit = False
    while not game_exit:

        draw(planets)

        for planet in planets:
            if planet.is_collision(planets):
                print("IMPACT!")
                game_exit = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True

            if event.type == pygame.WINDOWCLOSE:
                game_exit = True

        clock.tick(15)
        pygame.display.update()


if __name__ == "__main__":
    game_loop()
    pygame.display.quit()
    pygame.quit()
