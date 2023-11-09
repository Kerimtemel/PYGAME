import pygame
import random
import time
import sys
# Initialize pygame
pygame.init()

# window settings
screen_width = 750
screen_height = 750
screen =pygame.display.set_mode((screen_width,screen_height))

# fps settings
FPS =30
clock = pygame.time.Clock()

# clases
class Game:
    def __init__(self,fisherman,fish_group):
        # objects
        self.fisherman = fisherman
        self.fish_group = fish_group

        # game variables
        self.elapsed_time = 0
        self.fps_counter = 0
        self.level = 0

        # fish images
        fish1 = pygame.image.load("fish1.png")
        fish2 = pygame.image.load("fish2.png")
        fish3 = pygame.image.load("fish3.png")
        fish4 = pygame.image.load("fish4.png")
        self.fish_images = [fish1, fish2, fish3, fish4]
        self.target_fish_index = random.randint(0, 3)
        self.target_fish_image = self.fish_images[self.target_fish_index]
        self.target_fish_rect = self.target_fish_image.get_rect()
        self.target_fish_rect.top = 40
        self.target_fish_rect.centerx = screen_width // 2

        # font
        self.game_font = pygame.font.SysFont("game_font_ttf",40)

        # game music and sound effects
        self.catch_sound = pygame.mixer.Sound("catch_sound.wav")
        self.death_sound = pygame.mixer.Sound("death_sound.wav")
        pygame.mixer.music.load("background_music.wav")
        pygame.mixer.music.play(-1)

        # background
        self.game_background =pygame.image.load("game_background.jpg")
        self.game_over_image = pygame.image.load("game_over_image.jpg")

    def update(self):
        self.fps_counter += 1
        if self.fps_counter == FPS:
            self.elapsed_time += 1
            self.fps_counter = 0
            self.check_collision()
        self.set_safe_zone()

    def draw(self):
        text1 = self.game_font.render("TIME: " + str(self.elapsed_time), True, (255, 255, 255), (0, 0, 170))
        text1_rect = text1.get_rect()
        text1_rect.top = 30
        text1_rect.left = 30
        text2 = self.game_font.render("LIVES: " + str(self.fisherman.lives), True, (255, 255, 255), (0, 0, 170))
        text2_rect = text2.get_rect()
        text2_rect.top = 30
        text2_rect.right = screen_width - 50

        screen.blit(self.game_background, (0, 0))
        screen.blit(text1, text1_rect)
        screen.blit(text2, text2_rect)
        screen.blit(self.target_fish_image, self.target_fish_rect)
        pygame.draw.rect(screen, (255, 255, 255), (350, 30, 50, 50), 5)
        pygame.draw.rect(screen, (255, 0, 255), (0, 100, 750, screen_height - 150), 5)


    def check_collision(self):
        collision_occurred = pygame.sprite.spritecollideany(self.fisherman, self.fish_group)
        if collision_occurred:
            if collision_occurred.fish_type == self.target_fish_index:
                collision_occurred.remove(self.fish_group)
                self.catch_sound.play()
                if self.fish_group:
                    self.refresh_target_fish()
                else:
                    self.set_target_fish()
            else:
                self.fisherman.lives -= 1
                self.death_sound.play()
                if self.fisherman.lives <= 0:
                    self.game_over()

    def game_over(self):
        screen.blit(self.game_over_image, (0, 0))
        pygame.display.update()
        time.sleep(3)  # waitng 3 second
        pygame.quit()
        sys.exit()  #   and close game

    def reset(self):
        self.fisherman.lives = 3
        self.level = 0
        self.set_target_fish()
        self.set_safe_zone()

    def set_safe_zone(self):
        #  safe zone update
        self.fisherman.rect.left = max(0, self.fisherman.rect.left)
        self.fisherman.rect.right = min(screen_width, self.fisherman.rect.right)
        self.fisherman.rect.top = max(100, self.fisherman.rect.top)
        self.fisherman.rect.bottom = min(screen_height - 50, self.fisherman.rect.bottom)

    def refresh_target_fish(self):
        target_fish = random.choice(self.fish_group.sprites())
        self.target_fish_image = target_fish.image
        self.target_fish_index = target_fish.fish_type

    def set_target_fish(self):
        self.level = 1
        for fish in self.fish_group:
            self.fish_group.remove(fish)
        for _ in range(self.level):
            self.fish_group.add(Fish(random.randint(0, screen_width - 32), random.randint(105, screen_height - 150),
                                     self.fish_images[0], 0))
            self.fish_group.add(Fish(random.randint(0, screen_width - 32), random.randint(105, screen_height - 150),
                                     self.fish_images[1], 1))
            self.fish_group.add(Fish(random.randint(0, screen_width - 32), random.randint(105, screen_height - 150),
                                     self.fish_images[2], 2))
            self.fish_group.add(Fish(random.randint(0, screen_width - 32), random.randint(105, screen_height - 150),
                                     self.fish_images[3], 3))


class Fish(pygame.sprite.Sprite):
    def __init__(self, x, y, image, fish_type):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.fish_type = fish_type
        self.speed = random.randint(1, 5)
        self.direction_x = random.choice([-1, 1])
        self.direction_y = random.choice([-1, 1])

    def update(self):
        self.rect.x += self.speed * self.direction_x
        self.rect.y += self.speed * self.direction_y
        if self.rect.left <= 0 or self.rect.right >= screen_width:
            self.direction_x *= -1
        if self.rect.top <= 100 or self.rect.bottom >= screen_height - 50:
            self.direction_y *= -1


class Fisherman(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("fisherman.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.lives = 3
        self.speed = 10

    def update(self):
        self.move()

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        elif keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif keys[pygame.K_UP]:
            self.rect.y -= self.speed
        elif keys[pygame.K_DOWN]:
            self.rect.y += self.speed

# character group operations
fisherman_group = pygame.sprite.Group()
fisherman = Fisherman(screen_width // 2, screen_height // 2)
fisherman_group.add(fisherman)

# Fish test
fish_group = pygame.sprite.Group()

# Game class
game = Game(fisherman, fish_group)
game.set_target_fish()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    game.update()
    game.draw()
    # Draw fisherman and update
    fisherman_group.update()
    fisherman_group.draw(screen)
    # Fish test
    fish_group.update()
    fish_group.draw(screen)
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()



