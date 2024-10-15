import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the environment
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Define colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Define species classes
class Plant(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(center=(x, y))
        self.growth_rate = 0.1
        self.max_size = 50

    def update(self):
        self.rect.x += random.uniform(-1, 1)
        self.rect.y += random.uniform(-1, 1)
        if self.rect.x < 0 or self.rect.x > screen_width:
            self.rect.x = max(0, min(self.rect.x, screen_width))
        if self.rect.y < 0 or self.rect.y > screen_height:
            self.rect.y = max(0, min(self.rect.y, screen_height))
        self.grow()

    def grow(self):
        if self.rect.width < self.max_size:
            self.rect.width += self.growth_rate
            self.rect.height += self.growth_rate

class Herbivore(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 2
        self.hunger = 10

    def update(self):
        self.rect.x += random.uniform(-self.speed, self.speed)
        self.rect.y += random.uniform(-self.speed, self.speed)
        if self.rect.x < 0 or self.rect.x > screen_width:
            self.rect.x = max(0, min(self.rect.x, screen_width))
        if self.rect.y < 0 or self.rect.y > screen_height:
            self.rect.y = max(0, min(self.rect.y, screen_height))
        self.eat()

    def eat(self):
        if self.hunger > 0:
            self.hunger -= 1
        else:
            self.hunger = 10

class Carnivore(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 165, 0))  # Orange color for carnivore
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 2
        self.hunger = 10

    def update(self):
        self.rect.x += random.uniform(-self.speed, self.speed)
        self.rect.y += random.uniform(-self.speed, self.speed)
        if self.rect.x < 0 or self.rect.x > screen_width:
            self.rect.x = max(0, min(self.rect.x, screen_width))
        if self.rect.y < 0 or self.rect.y > screen_height:
            self.rect.y = max(0, min(self.rect.y, screen_height))
        self.hunt()

    def hunt(self):
        for herbivore in herbivores:
            if self.rect.colliderect(herbivore.rect):
                herbivore.kill()
                self.hunger -= 1
                break

class Resource:
    def __init__(self, x, y, amount):
        self.x = x
        self.y = y
        self.amount = amount

class Food(Resource):
    def __init__(self, x, y, amount):
        super().__init__(x, y, amount)

class Water(Resource):
    def __init__(self, x, y, amount):
        super().__init__(x, y, amount)

# Create species instances
plants = pygame.sprite.Group(Plant(100, 100), Plant(200, 200))
herbivores = pygame.sprite.Group(Herbivore(300, 300), Herbivore(400, 400))
carnivores = pygame.sprite.Group(Carnivore(500, 500))  # Adding carnivores

# Create resource instances
food = Food(100, 100, 100)
water = Water(200, 200, 50)

# Distribute resources
resources = [food, water]

# Implement interactions and update functions
def update_plants():
    for plant in plants:
        plant.update()

def update_herbivores():
    for herbivore in herbivores:
        herbivore.update()

def update_carnivores():
    for carnivore in carnivores:
        carnivore.update()

def check_collisions():
    for herbivore in herbivores:
        for plant in plants:
            if herbivore.rect.colliderect(plant.rect):
                herbivore.eat()
                plant.grow()

def main():
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(WHITE)

        update_plants()
        update_herbivores()
        update_carnivores()
        check_collisions()

        plants.draw(screen)
        herbivores.draw(screen)
        carnivores.draw(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()