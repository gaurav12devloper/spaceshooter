import pygame
import random
import math
import time
import subprocess
from os import path
img_dir = path.join(path.dirname(__file__), 'assets')
sound_folder = path.join(path.dirname(__file__), 'sounds')
pygame.init()
pygame.mixer.init()
WIDTH=800
HEIGHT=600
FPS=60
BLACK = (0, 0, 0)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# caption and icon
pygame.display.set_caption("fight")
icon = pygame.image.load("war.png")
pygame.display.set_icon(icon)
# backgroundimage
background = pygame.image.load("background.jpg")
backgrounds = pygame.image.load("backgrounds2.jpg")
#background3 = pygame.image.load("background3.png")
bg_x=0
bg_y=0
# plyer and icon
playerimag = pygame.image.load("player.png")
playerx = 370
playery = 500
playerx_chng = 0

#fireimag = pygame.image.load("firescreen.png")
# bullet image
bulletimag = pygame.image.load("laserRed16.png")
bulletx = 0
bullety = 500
bulletx_chng = 0
bullety_chng = 40
bullet_state = 'ready'
# enemy icon
enemyimag = []
enemyimag3 = []
enemyx = []
enemyy = []
enemyx_chng = []
enemyy_chng = []
leval=1
meteor_list = [
    'meteorBrown_big1.png',
    'meteorBrown_big2.png', 
    'meteorBrown_med1.png', 
    'meteorBrown_med3.png',
    'meteorBrown_small1.png',
    'meteorBrown_small2.png',
    'meteorBrown_tiny1.png',
    'Ship_2_eng.png','tick.png','bird.png','bluebird-upflap.png','redbird-upflap.png'
]
meteor_list3 = ['Ship_2_eng.png','tick.png']
num_of_enemy = 6

def make(meteor_list,enemyimag):
    for image in meteor_list:
        enemyimag.append(pygame.image.load(image))
        img=pygame.image.load(image)
        rect=img.get_rect()
        enemyx.append(random.randint(0, WIDTH - rect.width))
        enemyy.append(random.randint(20, 150)) 

make(meteor_list,enemyimag)
# score
player_score = 0
font_name = pygame.font.match_font('arial')
font = pygame.font.Font('freesansbold.ttf', 32)
game_over = pygame.font.Font('freesansbold.ttf', 70)
fontx = 10
fonty = 10

def player(x, y):
    screen.blit(playerimag, (x, y))

def score_nd_leval(x, y,leval):
    score = font.render("score: " + str(player_score), True, (255, 255, 255))
    screen.blit(score,(x, y))
    if leval>3:
        leval=1
    leval_text = font.render("Leval: " + str(leval), True, (255, 255, 255))
    screen.blit(leval_text,(x+650, y))

# declare level variable
#leval=1
def levals(leval):
    screen.fill(BLACK)
    leval+=1
    if leval<4:
        lbl = font.render("LEVAL: " + str(leval), True, (255, 255, 255))
        screen.blit(lbl,(300, 300))
    if leval==2:
        lbl = font.render("This Leval have more number of Stone", True, (255, 255, 255))
        screen.blit(lbl,(100, 400))
    elif leval==3:
        lbl = font.render("if you kill birds your score will reduce by 2", True, (255, 255, 255))
        screen.blit(lbl,(100, 400))
    elif leval>3:
        lbl = font.render("Leval three completed successfully", True, (255, 255, 255))
        screen.blit(lbl,(100, 350))
        lbl = font.render("Your score:"+ str(player_score), True, (255, 255, 255))
        screen.blit(lbl,(100, 400))
    pygame.display.update()
    pygame.time.wait(3000)
    pygame.display.update()
    return leval

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_font = font.render(text, True, (255, 255, 255))
    text_rect = text_font.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_font, text_rect)

def enemy(x, y, i):
    screen.blit(enemyimag[i], (x, y))

def blast(enemyx, enemyy):
    ## meteor explosion
    for i in range(9):
        filename = 'regularExplosion0{}.png'.format(i)
        img = pygame.image.load(path.join(img_dir, filename)).convert()
        img.set_colorkey(BLACK)
        pygame.display.update()
        pygame.time.wait(1)
        ## resize the explosion
        img_lg = pygame.transform.scale(img, (75, 75))
        screen.blit(img_lg, (enemyx, enemyy))

def iscollision(enemyx, enemyy, bulletx, bullety,enmywidth):
    distance = math.sqrt(math.pow(enemyx - bulletx, 2) + math.pow(enemyy - bullety, 2))
    if distance <enmywidth:
        return True 

def text_over():
    over = game_over.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over,(240,300))
    pygame.display.update()
    pygame.time.wait(3000)

def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletimag, (x, y))
    #screen.blit(fireimag, (370, 475))

def main_menu():
    global screen
    menu_song = pygame.mixer.music.load(path.join(sound_folder, "menu.ogg"))
    pygame.mixer.music.play(-1)
    pygame.display.update()

    while True:
        ev = pygame.event.poll()
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RETURN:
                break
            elif ev.key == pygame.K_q:
                pygame.quit()
                quit()
        elif ev.type == pygame.QUIT:
                pygame.quit()
                quit() 
        else:
            draw_text(screen, "Press [ENTER] To Begin", 30, WIDTH/2, HEIGHT/2)
            draw_text(screen, "or [Q] To Quit", 30, WIDTH/2, (HEIGHT/2)+40)
            pygame.display.update()
    ready = pygame.mixer.Sound(path.join(sound_folder,'getready.ogg'))
    ready.play()
    screen.fill(BLACK)
    draw_text(screen, "GET READY!", 40, WIDTH/2, HEIGHT/2)
    pygame.display.update()

expl_sounds = []
for sound in ['expl3.wav', 'expl6.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(sound_folder, sound)))

player_die_sound = pygame.mixer.Sound(path.join(sound_folder, 'rumble1.ogg'))

running = True
menu_display = True
enemy_sy=1.2
enemy_increase=0.2
#if leval>1:
    #enemy_sy=0.05
start = time.time()
player_die=False
while running:
    clock.tick(FPS)
    screen.fill((0, 0, 0))  
    if menu_display:
        main_menu()
        pygame.time.wait(3000)
        #Stop menu music
        pygame.mixer.music.stop()
        #Play the gameplay music
        pygame.mixer.music.load(path.join(sound_folder, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
        pygame.mixer.music.play(-1) 
        menu_display = False

    # backgroundimage
    if leval==1:
        screen.blit(background, (bg_x, bg_y))
    #elif leval==2:
        #screen.blit(backgrounds, (bg_x, bg_y))
    else:
        screen.blit(backgrounds, (bg_x, bg_y))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # function call here
    if player_die==False:
        player(playerx, playery)
    
    #called level
    done = time.time()
    elapsed = done - start

    randomv=random.randint(2,10)
    if leval>=1:
        randomv=randomv+leval*10
    if player_score>elapsed +randomv+10:
        enemy_sy+=enemy_sy
        if leval<5:
            leval=levals(leval)
            pygame.display.update()
        
        playerTime=False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        playerx_chng = -5

    elif keys[pygame.K_RIGHT]:
        playerx_chng = +5

    elif keys[pygame.K_UP]:
        playery_chng = +5

    elif keys[pygame.K_DOWN]: 
        playery_chng = -5

    if keys[pygame.K_SPACE]:
        bulletSound = pygame.mixer.Sound(path.join(sound_folder, 'laser.wav')).play()
        bulletx = playerx+15
        fire_bullet(bulletx, bullety)
        #bg_y-=2
        #playerx_chng = 2
    
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            playerx_chng = 0
    # changing postion of spacecrft
    playerx += playerx_chng
    # changing postion of enemy
    
    if num_of_enemy==0:
        text_over()
        bullet_state = 'done'
    for i in range(num_of_enemy):
        enmywidth=enemyimag[i].get_width()
        collision = iscollision(enemyx[i], enemyy[i], playerx, playery,enmywidth)
        if collision:
            player_die=True
            player_die_sound.play()
            blast(playerx, playery)
            enemyy[i] = 2000
            num_of_enemy=0
            text_over()
            subprocess.Popen('python spacefight.py')
            #os.system('python spacefight.py')
            #os._exit(0)
            pygame.quit()
            quit()

        # collision
        enmywidth=enemyimag[i].get_width()
        if i in range(9,12):
            enemyx[i] += enemy_sy
        else:
            enemyy[i]+= enemy_sy
        collision = iscollision(enemyx[i], enemyy[i], bulletx, bullety,enmywidth)
        if collision:
            random.choice(expl_sounds).play()  
            blast(enemyx[i], enemyy[i])
            player_score += 1
            if i in range(9,12):
                player_score += -3
            bullety = 480
            bullet_state = 'ready'
            enemyx[i] = random.randint(0,670)
            enemyy[i] = random.randint(50, 150)
        # function call
        #if random.random() > 0.1:
        enemy(enemyx[i], enemyy[i], i)

        if enemyy[i]>600 or enemyx[i]>800:
            enemyx[i] = random.randint(0, 780)
            enemyy[i] = random.randint(50, 150)
            #if random.random() > 0.9:
            enemy(enemyx[i], enemyy[i], i)

    # bullet movement
    if bullety <= 0:
        bullety = 480
        bullet_state = 'ready'
    if bullet_state is 'fire': 
        fire_bullet(bulletx, bullety)
        bullety += -25
    score_nd_leval(fontx,fonty,leval)
    if leval>1 and num_of_enemy!=0:
        num_of_enemy=len(meteor_list)-3
    if leval>2 and num_of_enemy!=0:
        num_of_enemy=len(meteor_list)
    if leval>3 and num_of_enemy!=0:
        level=1
        enemy_sy=1.2
    pygame.display.update()

