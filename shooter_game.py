#Створи власний Шутер!

from pygame import *
from random import randint
lost = 0


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
class GameSprite(sprite.Sprite):
    def  __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed 
        self.rect = self.image.get_rect()
        self.rect.x=player_x
        self.rect.y=player_y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x >5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x <650:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.x, self.rect.y,20,40,50)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        global lost 
        self.rect.y +=5
        if self.rect.y >500:
            self.rect.x =randint(80,600)
            self.rect.y = 0
            lost=lost+1
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= 10
        if self.rect.y <0:
            self.kill()
window=display.set_mode((700,500))
display.set_caption('Shooter')
background = transform.scale(image.load('galaxy.jpg'),(700,500))

#змінна ігрового циклу
game=True
clock=time.Clock()
FPS=60
finish = False
score = 0

ship = Player('rocket.png',300,400,60,100, 10)
monsters = sprite.Group()
for i in range(1,3):
    monster = Enemy('ufo.png',randint(80,600),-80,60,60,randint(1,5))
    monsters.add(monster)
bullets = sprite.Group()

font.init()
font1 = font.SysFont('Arial', 80)
win = font1.render('U WIN!!!', True, (255,255,255))
lose  = font1.render("U LOSE!", True, (180,0,0))

font2 = font.SysFont('Arial',36)


while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire()
                fire_sound.play()
    if finish !=True:
        window.blit(background,(0,0))
        text = font2.render('Счет:'+str(score), 1,(255,255,255))
        window.blit(text, (10,20))

        text_lose = font2.render('пропущено:'+str(lost), 1,(255,255,255))
        window.blit(text_lose, (10,50))





        ship.reset()
        bullets.draw(window)
        monsters.draw(window)
        monsters.update()
        ship.update()
        bullets.update()
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy('ufo.png', randint(80,600), -40,60,60, randint(1,5))
            monsters.add(monster)
        if sprite.spritecollide(ship, monsters, False) or lost >=4:
            finish = True
            window.blit(lose, (200,200))
        if score >=10:
            finish = True
            window.blit(win,(200,200))


    display.update()
    time.delay(60)
    clock.tick(FPS)
