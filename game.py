import pygame
pygame.init()

win = pygame.display.set_mode((1300, 688))

bg = pygame.image.load('grassbg.jpg')

screenWidth = 1300
screenHeight = 688

x = 0
y = 580
width = 32
height = 32
vel = 10

isJump = False
jumpCount = 10

def reloadWindow():
    global walkCount
    win.blit(bg, (0,0))
    pygame.draw.rect(win, (255, 255, 255), (x, y, width, height))
    pygame.display.update()

run = True
while run:
    pygame.time.delay(15)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    # if isJump:
    #     height = 24
    # if not isJump:
    #     height = 16
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and x >= 5:
        x -= vel
    if keys[pygame.K_RIGHT] and x < screenWidth - width:
        x += vel
    if not isJump:
        if keys[pygame.K_UP] and y >= vel:
            y -= vel
        if keys[pygame.K_DOWN] and y < 595 - height:
            y += vel
        if keys[pygame.K_SPACE]:
            isJump = True
    else:
        if jumpCount >= -10:
            neg = 1
            if jumpCount < 0:
                neg = -1
            y -= (jumpCount ** 2) * 0.2 * neg
            jumpCount -= 1
        else:
            isJump = False
            jumpCount = 10
    reloadWindow()

pygame.quit()
