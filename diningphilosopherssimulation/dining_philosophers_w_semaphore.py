import os
import sys
import pygame
from threading import Thread, Semaphore
import random
import time

'''This is a simple visual representation of Dining Philosophers problem by using pygame module
    and threading.Semaphore as mutex.

    Enis Buğra BULUT - 190315040 '''

# Fixes the File not found error when running from the command line.
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class BackgroundFurniture(pygame.sprite.Sprite):
    def __init__(self, image_file, location, scale_factor=1.0, horizontal_flip=False, vertical_flip=False):
        super().__init__()
        self.image = pygame.image.load(image_file)
        self.image = pygame.transform.flip(self.image, horizontal_flip, vertical_flip)
        self.image = pygame.transform.scale(
            self.image,
            (
                int(self.image.get_width() * scale_factor),
                int(self.image.get_height() * scale_factor)
            )
        )
        self.rect = self.image.get_rect(center=location)


class Chair(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        super().__init__()
        self.image = pygame.image.load(image_file)
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*4, self.image.get_height()*4))
        self.rect = self.image.get_rect(center=location)


class Character(pygame.sprite.Sprite):
    def __init__(self, character_id, state_id, location):
        super().__init__()
        self.image = pygame.image.load("assets/characters.png")
        self.rect = self.image.get_rect(center=location)
        self.image = self.image.subsurface(pygame.Rect(abs(state_id)*16, character_id*16, 16, 16))
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*4, self.image.get_height()*4))
        if state_id < 0:
            self.image = pygame.transform.flip(self.image, True, False)
        self.direction = "right"
        self.moving = False
        self.speed = 5


class Text:
    def __init__(self, text, location, font_size=20, font_color=(0, 0, 0)):
        self.text = text
        self.font = pygame.font.Font("assets/PressStart2P.ttf", font_size)
        self.text_surface = self.font.render(self.text, True, font_color)
        self.text_rect = self.text_surface.get_rect(center=location)


class Meal(pygame.sprite.Sprite):
    def __init__(self, location, is_meal_done=False):
        super().__init__()
        self.location = location
        self.is_meal_done = is_meal_done
        self.image = pygame.image.load("assets/spaghetti_full.png")
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*1, self.image.get_height()*1))
        self.rect = self.image.get_rect(center=location)

    def meal_is_done(self):
            self.image = pygame.image.load("assets/spaghetti_empty.png")
            self.image = pygame.transform.scale(self.image, (self.image.get_width() * 1, self.image.get_height() * 1))
            self.rect = self.image.get_rect(center=self.location)


class Chopstick(pygame.sprite.Sprite):
    def __init__(self, angle, location):
        super().__init__()
        self.image = pygame.image.load("assets/chopstick.png")
        self.image = pygame.transform.scale(self.image, (self.image.get_width()*0.2, self.image.get_height()*0.2))
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center=location)


class DiningPhilosophers:
    def __init__(self, number_of_philosophers, meal_size=9):
        self.meals = [meal_size for _ in range(number_of_philosophers)]
        self.chopsticks = [Semaphore(value=1) for _ in range(number_of_philosophers)]
        self.number_of_philosophers = number_of_philosophers

    def philosopher(self, i):
        j = (i+1) % self.number_of_philosophers
        while self.meals[i] > 0:
            time.sleep(random.random())
            if self.chopsticks[i].acquire(timeout=1):
                chopstick_list[i] = chopstick_list2[i*2]
                time.sleep(random.random())
                if self.chopsticks[j].acquire(timeout=1):
                    chopstick_list[j] = chopstick_list2[(j*2)+1]
                    time.sleep(5)  # long time to observe the program
                    self.meals[i] -= 1
                    chopstick_list[j] = chopstick_list_default[j]
                    self.chopsticks[j].release()
                chopstick_list[i] = chopstick_list_default[i]
                self.chopsticks[i].release()
        meal_list[j].meal_is_done()


def main():
    number_of_philosophers = 5
    number_of_meals = 7
    dining_philosophers = DiningPhilosophers(number_of_philosophers, number_of_meals)
    philosophers = [Thread(target=dining_philosophers.philosopher, args=(i, )) for i in range(number_of_philosophers)]
    t_end = time.time() + 60 * 15
    for philosopher in philosophers:
        philosopher.start()
    while time.time() < t_end:
        # sum(dining_philosophers.meals) > 0: we can change the while loop with this code
        # if we want to stop program right after meals are done.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        background_group.draw(screen)
        screen.blit(title_text.text_surface, title_text.text_rect)
        meal_group.draw(screen)
        chair_group.draw(screen)
        philosopher_group.draw(screen)
        # recreating chopstick sprites group, so we can observe the change of positions in every second
        chopstick_group = pygame.sprite.Group()
        chopstick_group.add(chopstick_list)  # adding dynamic chopstick sprite list to the group
        chopstick_group.draw(screen)
        pygame.display.update()
        clock.tick(60)
        time.sleep(0.1)
    for philosopher in philosophers:
        philosopher.join()


WIDTH = 800  # for the resolution of the program
HEIGHT = 600
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dining Philosophers")  # for the name of program
screen.fill((255, 255, 255))
clock = pygame.time.Clock()

background_group = pygame.sprite.Group()
background_group.add(
    [
        BackgroundFurniture("assets/floor.png", (x, y))
        for x in range(0, WIDTH+100, 62) for y in range(0, HEIGHT+100, 46)
    ]
)
background_group.add(BackgroundFurniture("assets/carpet.png", (WIDTH//2, HEIGHT//2), 12))
background_group.add(BackgroundFurniture("assets/fireplace.png", (WIDTH//2, 60), 4))
background_group.add(BackgroundFurniture("assets/music_player.png", (720, 90), 4))
background_group.add(BackgroundFurniture("assets/sofa_front.png", (560, 80), 4))
background_group.add(BackgroundFurniture("assets/sofa_single_right.png", (740, 200), 4))
background_group.add(BackgroundFurniture("assets/stairs.png", (700, 440), 4, True))
background_group.add(BackgroundFurniture("assets/desk.png", (170, 120), 3))
background_group.add(BackgroundFurniture("assets/table_horizontal.png", (WIDTH//2, HEIGHT//2), 4))

title_text = Text("Dining Philosophers", (WIDTH//2 - 100, HEIGHT - 50), 24, (200, 255, 200))

meal_0 = Meal((WIDTH//2 - 40, HEIGHT//2 - 50))
meal_1 = Meal((WIDTH//2 + 40, HEIGHT//2 - 50))
meal_2 = Meal((WIDTH//2 + 60, HEIGHT//2 - 15))
meal_3 = Meal((WIDTH//2 + 0, HEIGHT//2 - 10))
meal_4 = Meal((WIDTH//2 - 60, HEIGHT//2 - 15))
meal_list = [meal_0, meal_1, meal_2, meal_3, meal_4]
meal_group = pygame.sprite.Group()
meal_group.add(meal_list)

chair_0 = Chair("assets/chair_front_2.png", (WIDTH//2 - 40, HEIGHT//2 - 110))
chair_1 = Chair("assets/chair_front_2.png", (WIDTH//2 + 40, HEIGHT//2 - 110))
chair_2 = Chair("assets/chair_right_2.png", (WIDTH//2 + 130, HEIGHT//2 - 10))
chair_3 = Chair("assets/chair_back_2.png", (WIDTH//2, HEIGHT//2 + 100))
chair_4 = Chair("assets/chair_left_2.png", (WIDTH//2 - 130, HEIGHT//2 - 10))
chair_group = pygame.sprite.Group()
chair_group.add([chair_0, chair_1, chair_2, chair_3, chair_4])

philosopher_0 = Character(6, 0, (WIDTH//2 + 10, HEIGHT//2 + 30))
philosopher_1 = Character(0, 0, (WIDTH//2 + 90, HEIGHT//2 + 30))
philosopher_2 = Character(4, -2, (WIDTH//2 + 160, HEIGHT//2 + 100))
philosopher_3 = Character(10, 1, (WIDTH//2 + 45, HEIGHT//2 + 180))
philosopher_4 = Character(2, 2, (WIDTH//2 - 65, HEIGHT//2 + 100))

philosopher_list = [philosopher_0, philosopher_1, philosopher_2, philosopher_3, philosopher_4]
philosopher_group = pygame.sprite.Group()
philosopher_group.add(philosopher_list)

chopstick_0 = Chopstick(225, (WIDTH//2 + 0, HEIGHT//2 - 60))
chopstick_1 = Chopstick(160, (WIDTH//2 + 55, HEIGHT//2 - 35))
chopstick_2 = Chopstick(75, (WIDTH//2 + 40, HEIGHT//2 + 10))
chopstick_3 = Chopstick(15, (WIDTH//2 - 40, HEIGHT//2 + 10))
chopstick_4 = Chopstick(290, (WIDTH//2 - 55, HEIGHT//2 - 35))

# the list we are going to change dynamically
chopstick_list = [chopstick_0, chopstick_1, chopstick_2, chopstick_3, chopstick_4]
# for the chopsticks go default location
chopstick_list_default = [chopstick_0, chopstick_1, chopstick_2, chopstick_3, chopstick_4]

chopstick_0_1 = Chopstick(250, (WIDTH//2 + 25, HEIGHT//2 - 65))  # location and angle arranging for the chopstick 0
chopstick_0_2 = Chopstick(195, (WIDTH//2 - 25, HEIGHT//2 - 65))

chopstick_1_1 = Chopstick(145, (WIDTH//2 + 75, HEIGHT//2 - 25))  # location and angle arranging for the chopstick 1
chopstick_1_2 = Chopstick(195, (WIDTH//2 + 55, HEIGHT//2 - 65))

chopstick_2_1 = Chopstick(65, (WIDTH//2 + 10, HEIGHT//2))  # location and angle arranging for the chopstick 2
chopstick_2_2 = Chopstick(125, (WIDTH//2 + 75, HEIGHT//2 - 10))

chopstick_3_1 = Chopstick(325, (WIDTH//2 - 75, HEIGHT//2 - 10))  # location and angle arranging for the chopstick 3
chopstick_3_2 = Chopstick(25, (WIDTH//2 - 10, HEIGHT//2))

chopstick_4_1 = Chopstick(250, (WIDTH//2 - 50, HEIGHT//2 - 65))  # location and angle arranging for the chopstick 4
chopstick_4_2 = Chopstick(305, (WIDTH//2 - 75, HEIGHT//2 - 25))

# for the change sprite's location and angle
chopstick_list2 = [chopstick_0_1, chopstick_0_2, chopstick_1_1, chopstick_1_2, chopstick_2_1, chopstick_2_2,
                   chopstick_3_1, chopstick_3_2, chopstick_4_1, chopstick_4_2]


if __name__ == "__main__":
    main()