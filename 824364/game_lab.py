# підключаємо модуль
from pygame import *

# створення та іменування вікна
width = 1050
height = 750
window = display.set_mode((width, height))
display.set_caption('Лабіринт')

# інші змінні
ri = 'right'
le = 'left'

# музика
mixer.init()
mixer.music.load('main.wav')
mixer.music.play(-1)
over = mixer.Sound('over.wav')
shot = mixer.Sound('gunshot.wav')
bonus = mixer.Sound('mister-krabs.wav')
kill = mixer.Sound('kill.wav')
win = mixer.Sound('win.wav')
money = mixer.Sound('money.wav')
# змінні прапорці
bullets = sprite.Group()
finish = False
play = True
bulletsamount = 7
reloading = 0
door_open = False

# класи
class GameSprite(sprite.Sprite):
    def __init__(self, x, y, width, height, name):
        super().__init__()
        self.image = transform.scale(image.load(name), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, x, y, width, height, x_speed, y_speed, name, orien):
        super().__init__(x, y, width, height, name)
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.orien = orien

    def update(self):
        if ghost.rect.x <= width-50 and ghost.x_speed > 0 or ghost.rect.x >= 0 and ghost.x_speed < 0:
            self.rect.x += self.x_speed
        touched = sprite.spritecollide(self, walls, False)
        if self.x_speed > 0:
            for p in touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        if ghost.rect.y <= height-50 and ghost.y_speed > 0 or ghost.rect.y >= 0 and ghost.y_speed < 0:
            self.rect.y += self.y_speed
        touched = sprite.spritecollide(self, walls, False)
        if self.y_speed > 0:
            for p in touched:
                self.y_speed = 0
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
        elif self.y_speed < 0:
            for p in touched:
                self.y_speed = 0
                self.rect.top = max(self.rect.top, p.rect.bottom)

    def draw(self):
        if self.orien == 'right':
            window.blit(self.image, (self.rect.x, self.rect.y))
        elif self.orien == 'left':
            window.blit(transform.flip(self.image, True, False), (self.rect.x, self.rect.y))

    def fire(self):
        shot.play()
        if self.orien == 'right':
            bullets.add(Bullet(self.rect.right, self.rect.centery, 30, 25, "bullet_right.png", 15))
        elif self.orien == 'left':
            bullets.add(Bullet(self.rect.left, self.rect.centery, 30, 25, "bullet_left.png", -15))

class Enemy(GameSprite):
    def __init__(self, x, y, width, height, name, x1, x2, side):
        super().__init__(x, y, width, height, name)
        self.start = x1
        self.end = x2
        self.speed = 5
        self.side = side

    def update(self):
        if self.rect.x <= self.start:
            self.side = 'right'
        elif self.rect.x >= self.end:
            self.side = 'left'

        if self.side == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Bullet(GameSprite):
    def __init__(self, x, y, width, height, name, speed):
        super().__init__(x, y, width, height, name)
        self.speed = speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > width + 10 or self.rect.x < 0:
            self.kill()

collected_coins = 0

class Coin(GameSprite):
    def __init__(self, x, y):
        super().__init__(x, y, 20, 20, "coin.png")

# створення гравця
picture = GameSprite(0, 0, width, height, "display.jpg")
ghost = Player(75, 610, 50, 50, 0, 0, "ghost.png", ri)
final = GameSprite(900, 600, 75, 75, 'door.png')
holy_water = GameSprite(465, 380, 50, 50, "holy_water.png")
label = GameSprite(350, 675, 400, 100, "text_label.png")
coin_fail= GameSprite(350, 675, 400, 100, "text_label.png")
# створення демонів
demons = sprite.Group()
demons.add(Enemy(155, 10, 50, 60, 'enemy.png', 150, 850, 'right'))
demons.add(Enemy(230, 160, 50, 60, 'enemy.png', 225, 775, 'right'))
demons.add(Enemy(5, 310, 50, 60, 'enemy.png', 0, 325, 'right'))

# створення стін
walls = sprite.Group()
walls.add(GameSprite(0, 450, 225, 75, "wall2.png"))
walls.add(GameSprite(225, 675, 225, 75, "wall2.png"))
walls.add(GameSprite(450, 675, 225, 75, "wall2.png"))
walls.add(GameSprite(375, 525, 225, 75, "wall2.png"))
walls.add(GameSprite(225, 75, 225, 75, "wall2.png"))
walls.add(GameSprite(225, 225, 225, 75, "wall2.png"))
walls.add(GameSprite(450, 75, 225, 75, "wall2.png"))
walls.add(GameSprite(675, 75, 225, 75, "wall2.png"))
walls.add(GameSprite(825, 450, 225, 75, "wall2.png"))
walls.add(GameSprite(525, 225, 225, 75, "wall2.png"))
walls.add(GameSprite(225, 375, 75, 225, "wall1.png"))
walls.add(GameSprite(675, 300, 75, 225, "wall1.png"))
walls.add(GameSprite(375, 300, 75, 225, "wall1.png"))
walls.add(GameSprite(525, 300, 75, 225, "wall1.png"))
walls.add(GameSprite(150, 75, 75, 225, "wall1.png"))
walls.add(GameSprite(825, 150, 75, 225, "wall1.png"))
walls.add(GameSprite(675, 525, 75, 225, "wall1.png"))

# створення монеток
coins = sprite.Group()
coins.add(Coin(55, 265))
coins.add(Coin(650, 35))
coins.add(Coin(320, 450))
coins.add(Coin(630, 317))
coins.add(Coin(375, 167))

# основний ігровий цикл
while play:
    font.init()
    font1= font.SysFont('arial',25)
    for e in event.get():
        if e.type == QUIT:
            play = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                ghost.x_speed = -7
                ghost.orien = le
            elif e.key == K_RIGHT:
                ghost.x_speed = 7
                ghost.orien = ri
            elif e.key == K_UP:
                ghost.y_speed = -7
            elif e.key == K_DOWN:
                ghost.y_speed = 7
            elif e.key == K_SPACE:
                if bulletsamount > 0:
                    ghost.fire()
                    bulletsamount -= 1
        elif e.type == KEYUP:
            if e.key == K_LEFT:
                ghost.x_speed = 0
            elif e.key == K_RIGHT:
                ghost.x_speed = 0
            elif e.key == K_UP:
                ghost.y_speed = 0
            elif e.key == K_DOWN:
                ghost.y_speed = 0

    if not finish:
        picture.draw()
        final.draw()
        ghost.draw()
        walls.draw(window)
        demons.draw(window)
        bullets.draw(window)
        coins.draw(window)

        coins.update()
        bullets.update()
        demons.update()
        ghost.update()

        sprite.groupcollide(bullets, walls, True, False)
        sprite.groupcollide(bullets, demons, True, True)

        if bulletsamount == 0:
            reloading += 1
            if reloading >= 35:
                bulletsamount += 7
                reloading = 0

        if not door_open:
            holy_water.draw()
            if sprite.collide_rect(ghost, holy_water):
                door_open=True
                bonus.play()
                holy_water.kill()
        if sprite.spritecollide(ghost, coins, True):
            collected_coins += 1
            money.play()
        coin = font1.render(f'Монеток : {collected_coins}', True , (0,0,0))
        window.blit(coin, (10,10))

        if sprite.spritecollide(ghost, demons, False):
            finish = True
            mixer.music.stop()
            over.play()
            img = image.load('game_over.png')
            window.blit(transform.scale(img, (width, height)), (0, 0))

        if collected_coins==5 and sprite.collide_rect(ghost, final):
            if door_open:
                mixer.music.stop()
                finish = True
                win.play()
                img = image.load('winner.png')
                window.blit(transform.scale(img, (width, height)), (0, 0))
            else:
                label.draw()    
        

        time.delay(30)
        display.update()
