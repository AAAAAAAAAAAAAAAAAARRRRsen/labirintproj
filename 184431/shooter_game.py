from pygame import *
from random import randint

window = display.set_mode((700, 500))
display.set_caption('Догонялки')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
clock = time.Clock()
FPS = 30

font.init()
font1 = font.Font(None, 80)
font2 = font.Font(None, 36)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x 
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 595:
            self.rect.x += self.speed

    


    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, - 15, 15, 20)
        bullets.add(bullet)





lost = 0
class Enemy(GameSprite):
    def update(self):    
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(80, 700 - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
    
class Asteroid(GameSprite):
    def update(self):
         self.rect.y += self.speed
         if self.rect.y > 500:
            self.rect.x = randint(50, 700 - 80)
            self.rect.y = 0
      
            
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
mixer.music.set_volume(0.1)
fire_sound = mixer.Sound('fire.ogg')
fire_sound.set_volume(0.1)
img_back = 'galaxy.jpg'
img_bullet = 'bullet.png'
img_hero = 'rocket.png'
img_enemy = 'ufo.png'
img_ast = 'asteroid.png' 
max_lost = 3
lost = 0
goal = 10
score = 0

           
font.init()
font1 = font.Font(None, 36)

player = Player('rocket.png', 200, 440, 8, 40, 60)
bonus = GameSprite('donut-clip-art-4.png', randint(100, 600), 440, 0, 50, 50)

enemies = sprite.Group()
for i in range (5):
    enemy = Enemy('ufo.png', randint(150, 600), -40, randint(1, 2), 80, 50)
    enemies.add(enemy)
   
asteroids = sprite.Group()
for i in range (3):
    asteroid = Asteroid('asteroid.png', randint(300, 600), -40, randint(1, 2), 50, 45)
    asteroids.add(asteroid)
    
bullets = sprite.Group()
    
















game = True
finish = False



while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                    fire_sound.play()
                    player.fire()

   

    if finish != True:
        window.blit(background, (0, 0))
        text_lose = font1.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        text_win = font1.render('Сбито: ' + str(score), 1, (250, 250, 250))
        window.blit(text_win, (10, 30))

        collides = sprite.groupcollide(enemies, bullets, True, True)
        for c in collides:
            score = score + 1
            enemy = Enemy(img_enemy, randint(80, 700 - 80), -40, randint(1, 2), 80, 50)
            enemies.add(enemy)


        if sprite.spritecollide(player, enemies, False) or sprite.spritecollide(player, asteroids, False):
            sprite.spritecollide(players, enemies, True)
            sprite.spritecollide(player, asteroids, True)
            finish = True
            window.blit(lose, (200, 200))


        if score >= goal:
            finish = True
            window.blit(win, (200, 200))
        

        player.update()
        enemies.update()
        bullets.update()
        asteroids.update()

        player.reset()
        bonus.reset()
        bullets.draw(window)
        enemies.draw(window)
        asteroids.draw(window)
        clock.tick(FPS)
        display.update()

