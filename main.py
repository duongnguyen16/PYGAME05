# code by duong nguyen
import pygame, sys, random
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()

w, h = 800, 400

game_display = pygame.display.set_mode((w, h))
screen = pygame.surface.Surface((w,h))

# mac oc optimize
pygame.display.set_caption("Duong Nguyen Xuan - PYGAME05 (Dino in developing)")

RED = pygame.color.Color("red")
GREEN = pygame.color.Color("green")

map = pygame.image.load("./Asset/other/map.png")

def print_screen_center(text, color, size, y):
    gen_font = pygame.font.SysFont('Arial', size)
    gen_text = gen_font.render(text, True, color)
    gen_text_width, gen_text_height = gen_font.size(text)
    game_display.blit(gen_text, [w / 2 - gen_text_width / 2, y])


class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # STATE: IDLE, JUMP, DUCK, START
        self.state = "idle"
        self.id = 1

        self.game_over = False
        self.asset_dir = f"./Asset/dino/Dino{self.id}.png"

        self.image = pygame.image.load(self.asset_dir)
        self.rect = self.image.get_rect()
        self.rect.topleft = [22, 228]

        self.idle_count = 0
        self.vel = 0
        self.jump_state = 0
        self.jump = False

    def update(self):
        if self.state == "start":
            self.id = 0
        elif self.state == "idle":
            if self.idle_count < 4:
                self.id = 1
                self.idle_count += 1
            elif self.idle_count < 10:
                self.id = 2
                self.idle_count += 1
            else:
                self.idle_count = 0
                self.id = 1
        elif self.state == "jump":
            self.id = 3
        elif self.state == "duck":
            if self.id == 4:
                self.id = 5
            elif self.id == 5:
                self.id = 4
            else:
                self.id = 4
        elif self.state == "die":
                self.id = 6

        if self.state == "duck":
            self.rect.y = 262
            self.state = "idle"
        elif self.state == "idle":
            self.rect.y = 228

        self.asset_dir = f"./Asset/dino/Dino{self.id}.png"
        self.image = pygame.image.load(self.asset_dir)

        if self.rect.y == 227 or self.rect.y == 224:
            # print("Stop JUMP")
            self.jump_state = 0
            self.rect.y = 228
            self.state = "idle"


        if not self.game_over:
            key = pygame.key.get_pressed()

            if key[pygame.K_w] or key[pygame.K_SPACE] or key[pygame.K_UP]:
                if self.jump_state == 0 and not self.state == "jump":
                    self.vel = -20
                    self.jump_state = 1
                    self.state = "jump"
            elif key[pygame.K_s] or key[pygame.K_LSHIFT] or key[pygame.K_DOWN]:
                if not self.state == "duck" and self.jump_state == 0:
                    self.state = "duck"
                    print("Duck!")

        if self.state == "jump" and self. jump_state != 0:
            if self.jump_state == 1:
                self.vel += 1
            if self.vel == 1 and self.jump_state == 1:
                self.jump_state = 2
            if self.jump_state == 2:
                self.vel += 1
            self.rect.y += self.vel
        print(f"Rect.y {self.rect.y} - Vel: {self.vel} - Jump_State: {self.jump_state} - id: {self.id}")


        # hit = pygame.sprite.spritecollide(self, enemy_gr, False)
        # if hit:
        #     self.game_over = True



player_gr = pygame.sprite.Group()

player = Player()

player_gr.add(player)

game_over = False

while True:
    game_display.fill(pygame.color.Color("white"))
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()

    game_display.blit(map,[0,300])
    player_gr.update()
    player_gr.draw(game_display)

    clock.tick(60)
    pygame.display.update()
