# this allows us to use code from
# the open-source pygame library
# throughout this file
import sys
import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    pygame.init()
    print("Starting asteroids!")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    score = 0
    points = 0
    lives = 3
    points_to_new_life = NEW_LIFE_POINTS

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    updatable.add(player)
    drawable.add(player)

    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (shots, updatable, drawable)
    asteroid_field = AsteroidField()

    Player.containers = (updatable, drawable)
    dt = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        for u in updatable:
            u.update(dt)

        for a in asteroids:
            if player.collides_with(a):
                lives -= 1
                if lives == 0:
                    print("Game over!")
                    print(f"Score: {score}")
                    sys.exit()
                else:
                    player.kill()
                    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

            for s in shots:
                if a.collides_with(s):
                    points += a.split()
                    score += points
                    points_to_new_life -= points
                    points = 0
                    if points_to_new_life <= 0:
                        lives += 1
                        points_to_new_life = NEW_LIFE_POINTS
                    s.kill()

        screen.fill("black")

        for d in drawable:
            d.draw(screen)

        pygame.display.flip()
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
