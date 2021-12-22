import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
# caption and icon
pygame.display.set_caption("fight")
icon = pygame.image.load("war.png")
pygame.display.set_icon(icon)
# backgroundimage
background = pygame.image.load("background.jpg")
bg_x=0
bg_y=0
# plyer and icon
playerimag = pygame.image.load("war.png")
playerx = 370
playery = 500
playerx_chng = 0

#
#fireimag = pygame.image.load("firescreen.png")
# bullet image
bulletimag = pygame.image.load("bullet1.PNG")
bulletx = 0
bullety = 500
bulletx_chng = 0
bullety_chng = 40
bullet_state = 'ready'

def player(x, y):
    screen.blit(playerimag, (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletimag, (x, y))
    #screen.blit(fireimag, (370, 475))


running = True
while running:
    screen.fill((0, 0, 0))  
    # backgroundimage
    screen.blit(background, (bg_x, bg_y))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # function call here
    player(playerx, playery)

    """ if bg_x>0 or bg_x<-800:
        bg_x=-800 """
    if bg_x<-1000:
        bg_x=50
    if bg_y>50:
        bg_y=-500
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        #playerx_chng = -2
        bg_x+=2
    elif keys[pygame.K_RIGHT]:
        bg_x-=2
    elif keys[pygame.K_UP]:
        bg_y+=2
    elif keys[pygame.K_DOWN]:
        bg_y-=2   

    if keys[pygame.K_SPACE]:
        bulletx = playerx+15
        fire_bullet(bulletx, bullety)
        #bg_y-=2
        #playerx_chng = 2
    
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            playerx_chng = 0
    # changing postion of spacecrft
    playerx += playerx_chng

    # bullet movement
    if bullety <= 0:
        bullety = 480
        bullet_state = 'ready'
    if bullet_state is 'fire': 
        fire_bullet(bulletx, bullety)
        bullety += -5

    pygame.display.update()
