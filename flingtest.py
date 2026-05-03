import pygame

pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

vent = pygame.image.load("img_keys/vent.png").convert_alpha()
rect_surf = pygame.Surface((300, 232), pygame.SRCALPHA) 
rect_surf.fill((255, 255, 255))

angle = 0

pressed = []

rx = 250
ry = 500
center_pos = (rx, ry)
count = 0

fling = False
        
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_4:
                pressed.append(4)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_3:
                pressed.append(3)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_2:
                pressed.append(2)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                pressed.append(1)


    screen.fill((30, 30, 30))
    

    if pressed == [4,1,2,3]:
        fling = True
    elif len(pressed) > 3:
        pressed = []
        
    if fling:
        count += 1
        angle += 20
        rx -= 40
        ry -= 40
    
    fvent = pygame.transform.rotate(vent, angle)

    if fling:
        screen.blit(fvent, (rx,ry))
    else:
        screen.blit(fvent, (rx, ry))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
