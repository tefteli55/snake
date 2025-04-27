from pygame import *
from random import choice
from random import randint

window = display.set_mode((700,500))
display.set_caption('Длинная штука')

class GameSprite(sprite.Sprite):
    def __init__(self, img, x,y,w,h):
        super().__init__()
        self.image = transform.scale(image.load(img),(w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Snake(GameSprite):
    def __init__(self, img, x, y, w, h, t):
        super().__init__(img, x, y, w, h)
        self.type = t
        self.speed = 25
        self.direction = "0"
        self.cur_image = self.image
        self.wait = 30

    def update(self):
        if self.direction == 'l':
            self.rect.x -= self.speed
        elif self.direction == 'r':
            self.rect.x += self.speed
        elif self.direction == 'u':
            self.rect.y -= self.speed
        elif self.direction == 'd':
            self.rect.y += self.speed

    def get_direction(self):

        keys = key.get_pressed()
        if keys[K_LEFT]:
            self.direction = 'l'
            self.image = transform.rotate(self.cur_image, -90)
        elif keys[K_RIGHT]:
            self.direction = 'r'
            self.image = transform.rotate(self.cur_image, 90)
        elif keys[K_UP]:
            self.direction = 'u'
            self.image = transform.rotate(self.cur_image, 180)
        elif keys[K_DOWN]:
            self.direction = 'd'
            self.image = transform.rotate(self.cur_image, 0)

    def set_direct(self):
        if self.direction == 'l':
            self.image = transform.rotate(self.cur_image, -90)
        elif self.direction == 'r':
            self.image = transform.rotate(self.cur_image, 90)
        elif self.direction == 'u':
            self.image = transform.rotate(self.cur_image, 180)
        elif self.direction == 'd':
            self.image = transform.rotate(self.cur_image, 0)

    def eat(self, food):
        global speed
        speed +=1
        food.position()


class Food(GameSprite):
    def __init__(self, imgs, x, y, w, h):
        super().__init__(imgs[0], x,y,w,h)
        self.costumes = []
        self.costumes.append(self.image)
        for i in range(len(imgs)-1):
            self.image = transform.scale(image.load(imgs[i+1]), (w,h))
            self.costumes.append(self.image)

    def set_costume(self, n):
        self.image = self.costumes[n]

    def rand_costume(self):
        self.images = choice(self.costumes)

    def position(self):
        self.rect.x = int(randint(0, 700-self.rect.width)/25)*25
        self.rect.y = int(randint(0, 500-self.rect.height)/25)*25
        self.rand_costume()

font.init()
font1 = font.SysFont('Arial', 36, 15)

head = Snake('golova.png', 350, 250, 25, 25, 5)
tail = Snake('xvost.png', 350, 225, 25, 25, 5)
snake = [head, tail]
food = Food(['abloko.png', 'bonan.png', 'mango.png', 'ogyrez.png'], -100, -100, 25, 25)
food.position()
button = GameSprite('play.png', 250, 150, 200, 180)

game = True
clock = time.Clock()
FPS = 60
speed = 1
global_wait = 0
menu = True
finish = True

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if menu:
        window.fill((0,250,90))
        button.reset()
        pressed = mouse.get_pressed()
        pos = mouse.get_pos()
        if pressed[0]: 
            if button.rect.collidepoint(pos[0], pos[1]):
                menu = False
                finish = False
    
    if not finish:
        window.fill((0,250,90))
        score_text = font1.render('Счёт: ' +str(speed-1), 1, (0,0,0))
        window.blit(score_text, (10,10))

    head.get_direction()
    if global_wait == 0:
        global_wait = head.wait
        for e in range(len(snake)-1, 0, -1):
            snake[e].reset()
            snake[e].direction = snake[e-1].direction
            snake[e].rect.x = snake[e-1].rect.x
            snake[e].rect.y = snake[e-1].rect.y
            snake[e].set_direct()
        head.update()

    else:
        global_wait -= 1

    head.reset()
    food.reset()
    for s in snake:
        s.reset()

    if head.rect.colliderect(food):
        head.eat(food)
        s = Snake('telo.png', head.rect.x, head.rect.y, 25, 25, 0)
        snake.insert(1,s)
        if speed%5 == 0:
            head.wait -= 2
        if head.wait <10:
            head.wait = 0

    if head.rect.x < 0:
        head.rect.x += 700
    if head.rect.y <0:
        head.rect.y += 500
    if head.rect.x > 700:
        head.rect.x += 0
    if head.rect.y > 500:
        head.rect.y += 0

    if speed>1:
        for i in range(2, len(snake)+1):
            if head.rect.colliderect(snake[i]):
                finish = True
                
    clock.tick(FPS)
    display.update()