import pygame
pygame.init()
SCREEN_WIDTH=1023
SCREEN_HEIGHT=862
win=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Character moving")
bg=pygame.image.load('bg1.jpg')
bgx=0
bgx1=bg.get_width()

walkRight=[pygame.image.load('R1.png'),pygame.image.load('R2.png'), pygame.image.load('R3.png'),
             pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'),
             pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft=[pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'),
            pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'),
            pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
char=pygame.image.load('standing.png')
clock=pygame.time.Clock()

class player:
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.vel=5
        self.isJump=False
        self.jumpCount=10
        self.left=False
        self.right=False
        self.walkCount=0
        self.standing=True

    def draw(self,win):

        if self.walkCount +1>=27:
            self.walkCount=0
        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//3],(self.x,self.y))
                self.walkCount+=1
            elif self.right:
                win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.left:
                win.blit(walkLeft[0],(self.x,self.y))
            else:
                win.blit(walkRight[0], (self.x, self.y))

class projectile:
    def __init__(self,x,y,radius,color,facing):
        self.x=x
        self.y=y
        self.radius=radius
        self.color=color
        self.facing=facing
        self.vel=10*facing

    def draw(self,win):
        pygame.draw.circle(win,self.color,(self.x,self.y),self.radius)

class enemy:
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'),
                 pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'),
                 pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'),
                 pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'),
                pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'),
                pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'),
                pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True

    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            # pygame.draw.rect(win, (255,0,0), self.hitbox,2)

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        print('hit')

class friend:
    walkRight=[pygame.image.load('friend/agent1.png'),pygame.image.load('friend/agent2.png'),
               pygame.image.load('friend/agent3.png'),pygame.image.load('friend/agent4.png'),
               pygame.image.load('friend/agent5.png'),pygame.image.load('friend/agent6.png'),
               pygame.image.load('friend/agent7.png'),pygame.image.load('friend/agent8.png')]
    def __init__(self,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.vel=3
        self.walkCount=0

    def draw(self,win):
        if self.walkCount +1>=24:
            self.walkCount=0
        if self.vel>0:
            win.blit(self.walkRight[self.walkCount//3],(self.x,self.y))
            self.walkCount+=1
            self.x+=self.vel
        else:
            self.vel=self.vel*-1
           # win.blit(self.walkRight[0],(self.x,self.y))

def redrawGameWindow():
    win.blit(bg,(0,0))
    man.draw(win)
    satish.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()

man=player(50,430,70,70)
goblin=enemy(100, 430, 64, 64, 450)
satish=friend(200,430,64,64)
bullets=[]
run=True
speed=30
while run:
    clock.tick(speed)
    bgx -=1.4
    bgx1 -=1.4
    if bgx <bg.get_width()* -1:
        bgx=bg.get_width()
    if bgx <bg.get_width()* -1:
        bgx=bg.get_width()
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT :
            run=False

    for bullet in bullets:
        if bullet.x<SCREEN_WIDTH and bullet.x >0:
            bullet.x +=bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    key=pygame.key.get_pressed()

    if key[pygame.K_SPACE]:
        if man.left:
            facing=-1
        else:
            facing=1
        if len(bullets)<5:
            bullets.append(projectile(round(man.x+man.width//2),round(man.y+man.height//2),6,(0,0,0),facing))

    if key[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left=True
        man.right=False
        man.standing=False

    elif key[pygame.K_RIGHT] and man.x <SCREEN_WIDTH-man.vel-man.width:
        man.x += man.vel
        man.left = False
        man.right = True
        man.standing=False

    else:
        man.standing=True
        man.walkCount=0

    if not(man.isJump):
        if key[pygame.K_UP]:
            man.isJump=True
            man.right=False
            man.left=False
            man.walkCount=0
    else:
        if man.jumpCount>=-10:
            neg=1
            if man.jumpCount<0:
                neg=-1
            man.y -=(man.jumpCount**2)*0.5*neg
            man.jumpCount -=1
        else:
            man.jumpCount=10
            man.isJump=False
    redrawGameWindow()
pygame.quit()

