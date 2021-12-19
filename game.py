import pygame
from pygame import font
from random import randrange as rd

pygame.init()
screen_color=(32, 141, 150)
ball_color=(44, 17, 51)
player_color=(94, 79, 22)
WHITE =(255,255,255)
RED=(255,0,0)
GREEN=(0,255,0)
BLACK=(0,0,0)
SCREEN_WIDTH=700
SCREEN_HEIGHT=500
size = (SCREEN_WIDTH,SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('pong')
done = False
clock = pygame.time.Clock()
score=0
font=pygame.font.SysFont('Calibri',25,True,False)
sound=pygame.mixer.Sound('sound.ogg')
start_image=pygame.image.load('1.png')
end_image=pygame.image.load('2.png')

class Player(pygame.sprite.Sprite):
    def __init__(self,color,width,x,y):
        super().__init__()
        self.color=color
        self.image = pygame.Surface([width,50])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft=[x,y]
    def update(self, topleft):
        new_width=self.rect.width-50
        self.image=pygame.Surface([new_width,50])
        self.image.fill(self.color)
        self.rect=self.image.get_rect()
        self.rect.topleft=topleft

class Ball(pygame.sprite.Sprite):
    def __init__(self,color,x,y):
        super().__init__()
        self.image=pygame.Surface([50,50])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        pygame.draw.circle(self.image,color,[25,25],25) #surface,color,center_coordinates,radious
        self.rect = self.image.get_rect()
        self.rect.topleft=[x,y]
    def update(self):
        global dx, dy, score
        if self.rect.y<0:
            sound.play()
            dy*=-1
        if self.rect.x>SCREEN_WIDTH-50 or self.rect.x<0:
            dx*=-1
            sound.play()
        self.rect.x+=dx
        self.rect.y+=dy
    def bounce(self):
        global dy
        dy*=-1
        sound.play()
        self.update()
    def reappear(self):
        self.rect.x=rd(10,SCREEN_WIDTH)
        self.rect.y=10

class Game():
    def __init__(self):
        self.state='start'
    def start(self):
        global done
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                done=True
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    self.state='main_game'
        #set background color
        screen.fill(WHITE)
        op_str='Press SPACE to start the game'
        text=font.render(op_str,True,BLACK)
        screen.blit(start_image,(0,0))
        screen.blit(text,[SCREEN_WIDTH//2-50,SCREEN_HEIGHT//2-240])
        #update screen
        pygame.display.flip()
    def state_manager(self):
        if self.state=='start':
            self.start()
        elif self.state=='endgame':
            self.endgame()
        elif self.state=='main_game':
            self.main_game()
    def endgame(self):
        global done, score
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                done=True
        #set background color
        screen.fill(WHITE)
        op_str='you are DEAD, Last score: {}'.format(score)
        text=font.render(op_str,True,BLACK)
        screen.blit(end_image,[SCREEN_WIDTH//2-100,SCREEN_HEIGHT//2-100])
        screen.blit(text,[250,50])
        #update screen
        pygame.display.flip()
    def main_game(self):
        global score,done,x_speed,player_list,current_time,button_press_time,ball
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                done=True
            elif event.type==pygame.KEYDOWN:
                # button_press_time=pygame.time.get_ticks()
                if event.key == pygame.K_LEFT:
                    x_speed=-player_speed
                elif event.key == pygame.K_RIGHT:
                    x_speed=player_speed
            elif event.type==pygame.KEYUP:
                if event.key==pygame.K_RIGHT or event.key==pygame.K_LEFT:
                    x_speed=0
        # print('current time: {}, button press time: {}'.format(current_time,button_press_time))
        
        #set background color
        screen.fill(screen_color)
        #draw things
        ball_list.draw(screen)
        player_list.draw(screen)
        op_str="SCORE: {}".format(score)
        text=font.render(op_str,True,BLACK)
        screen.blit(text,[SCREEN_WIDTH-150,SCREEN_HEIGHT-450])
        #game logic
        player.rect.x+=x_speed
        if player.rect.x>SCREEN_WIDTH-player.rect.width:
            player.rect.x = SCREEN_WIDTH-player.rect.width
        elif player.rect.x<0:
            player.rect.x = 0
        ball_list.update()
        hits_list = pygame.sprite.spritecollide(player,ball_list,False)
        for hit_ball in hits_list:
            score+=1
            hit_ball.bounce()
        for ball in ball_list:
            if ball.rect.y>SCREEN_HEIGHT-50:
                score-=1
                player_list.update(player.rect.topleft)
                if player.rect.width==0:
                    self.state='endgame'
                ball.reappear()
        #update screen
        pygame.display.flip()

player_life=400
player=Player(player_color,player_life,150,440)
x_speed=0 # players speed
player_speed=10

ball = Ball(ball_color,rd(0,SCREEN_WIDTH),10)
dx=5
dy=5

player_list = pygame.sprite.Group()
ball_list = pygame.sprite.Group()

player_list.add(player)
ball_list.add(ball)

game=Game()

while not done:
    game.state_manager()
    clock.tick(60) #frame per seconds
pygame.quit()