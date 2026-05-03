import pygame

pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

rect_surf = pygame.Surface((300, 232), pygame.SRCALPHA) 
rect_surf.fill((255, 255, 255))

angle = 0

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
            if event.key == pygame.K_RETURN:
                fling = True

    screen.fill((30, 30, 30))

    rotated_surf = pygame.transform.rotate(rect_surf, angle)
    
    if fling:
        count += 1
        angle += 20
        rx -= 40
        ry -= 40

    if fling:
        screen.blit(rotated_surf, (rx,ry))
    else:
        screen.blit(rect_surf, (rx, ry))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()