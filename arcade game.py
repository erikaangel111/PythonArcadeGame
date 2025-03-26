#arcade game 
from random import randint
import pygame 
from pygame import sprite, transform  
pygame.init()
font = pygame.font.Font(None, 72)


win_width = 800
win_height = 600
left_bound = win_width / 40           
right_bound = win_width - 8 * left_bound
shift = 0
speed = 0
shift += speed

x_start, y_start = 20, 10

pygame.display.set_caption("Arcade")  
window = pygame.display.set_mode((win_width, win_height))
clock = pygame.time.Clock()


img_file_back = pygame.transform.scale(pygame.image.load(r"C:\Users\Herberth\OneDrive\Escritorio\Arcade\FondoCompe.png"), (win_width, win_height)) 
img_file_hero = pygame.transform.scale(pygame.image.load(r"C:\Users\Herberth\OneDrive\Escritorio\Arcade\a_simple_guy_caminando.png"), (50, 50)) 
img_file_bomb = pygame.transform.scale(pygame.image.load(r"C:\Users\Herberth\OneDrive\Escritorio\Arcade\bomb.png"), (30, 30)) 
img_file_enemy = pygame.transform.scale(pygame.image.load(r"C:\Users\Herberth\OneDrive\Escritorio\Arcade\dude2.png"), (50, 50)) 
img_file_princess = pygame.transform.scale(pygame.image.load(r"C:\Users\Herberth\OneDrive\Escritorio\Arcade\a_simple_guy_caminando.png"), (50, 50)) 


C_GREEN = (0, 255, 0)

class GameSprite(sprite.Sprite):
    def __init__(self, image, x, y):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(pygame.image.load(image), (80, 80))
        self.rect = self.image.get_rect() 
        self.rect.x = x
        self.rect.y = y
    def gravitate(self):
        self.y_speed += 0.25
    
class FinalSprite(pygame.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y): 
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(player_image), (60, 120))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

class Wall(pygame.sprite.Sprite):
    def __init__(self, x=20, y=0, width=120, height=120, color=C_GREEN):
       pygame.sprite.Sprite.__init__(self)

       self.image = pygame.Surface([width, height])
       self.image.fill(color)


       self.rect = self.image.get_rect()
       self.rect.x = x
       self.rect.y = y


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x=20, y=0, filename=img_file_enemy, width=100, height=100):
       pygame.sprite.Sprite.__init__(self)


       self.image = pygame.transform.scale(pygame.image.load(filename), (width, height)).convert_alpha()
       self.rect = self.image.get_rect()
       self.rect.x = x
       self.rect.y = y

    def update(self):
       ''' mueve el personaje usando la velocidad horizontal y vertical actual'''
       self.rect.x += randint(-5, 5)
       self.rect.y += randint(-5, 5)
        
#Inicio del juego 
pygame.display.set_caption("Arcade")
window = pygame.display.set_mode([win_width, win_height])

back  = pygame.transform.scale(pygame.image.load(r"C:\Users\Herberth\OneDrive\Escritorio\Arcade\FondoCompe.png").convert(), (win_width, win_height))

all_sprites = pygame.sprite.Group()
barriers = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bombs = pygame.sprite.Group()

# Crea el héroe
hero = GameSprite(img_file_hero, x_start, y_start)
all_sprites.add(hero)

# Crea las paredes
w = Wall(50, 150, 480, 20)
barriers.add(w)
all_sprites.add(w)
w = Wall(700, 50, 50, 360)
barriers.add(w)
all_sprites.add(w)
w = Wall(350, 380, 640, 20)
barriers.add(w)
all_sprites.add(w)
w = Wall(-200, 590, 1600, 20)
barriers.add(w)
all_sprites.add(w)

# Crea el enemigo
en = Enemy(50, 480) 
all_sprites.add(en)
enemies.add(en)

# Crea la bomba
bomb = Enemy(520, 500, img_file_bomb, 60, 60)  
bombs.add(bomb)

# Crea la princesa
pr = FinalSprite(img_file_princess, win_width + 500, win_height - 150, 0)
all_sprites.add(pr)

run = True
finished =  False
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                speed = -5
            elif event.key == pygame.K_RIGHT:
                speed = 5
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                speed = 0
            elif event.key == pygame.K_RIGHT:
                speed = 0

    if not finished:
        all_sprites.update()

        pygame.sprite.groupcollide(bombs, all_sprites, True, True)

        if pygame.sprite.spritecollide(robin, enemies, False):
            robin.kill()
        if (robin.rect.x > right_bound and robin.x_speed > 0 or robin.rect.x < left_bound and robin.x_speed < 0): 
           shift -= robin.x_speed 
 
           for s in all_sprites:
               s.rect.x -= robin.x_speed 
           for s in bombs: 
               s.rect.x_speed -= robin.x_speed
  

           local_shift = shift % win_width
           window.blit(back, (local_shift, 0))
           if local_shift != 0:
               window.blit(back, (local_shift - win_width, 0))
           all_sprites.draw(window) 
         
           bombs.draw(window)

           if pygame.sprite.collide_rect(robin, pr):
                finished = True
                window.fill(C_BLACK)
                # escribimos texto en la pantalla
                text = font.render("¡GANASTE!", 1, C_RED)
                window.blit(text, (250, 250))
           if robin not in all_sprites or robin.rect.top > win_height:
                finished = True           
                window.fill(C_BLACK)
                # escribimos texto en la pantalla
                text = font.render("JUEGO TERMINADO", 1, C_RED)
                window.blit(text, (250, 250))
pygame.display.update()

 
