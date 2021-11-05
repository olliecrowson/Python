import pygame, random, os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,25)
pygame.init()
clock = pygame.time.Clock()
screenInfo = pygame.display.Info()
screen = pygame.display.set_mode((screenInfo.current_w, screenInfo.current_h-64))
screen.fill((250,250,250))
pygame.display.update()

'''
def menu():
    backgroundScreen = pygame.image.load(background)
    screen.blit(backgroundScreen, (0,0))
    pygame.display.update()
'''

class Node:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image)
        self.touching = False
        self.mouse_down = False
        screen.blit(self.image, (x, y))
    def hoveringOver(self):
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        #print(self.mouse_x,self.mouse_y)
        #print(self.x,self.y)
        if (self.mouse_x >= self.x) and (self.mouse_x <= self.x+40):
            if (self.mouse_y > self.y) and (self.mouse_y < self.y+40):
                self.touching = True
                return True
    def drop(self):
        screen.blit(self.image, (pygame.mouse.get_pos()))


def drag_drop():
    mouse_down = False
    while not mouse_down:
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_down = True

    while mouse_down:
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return True
            else:
                mouse_down = False





pc_1 = Node(10,15,"pc.png")
router_1 = Node(10,60,"router.png")
switch_1 = Node(10, 105,"switch.png")
hub_1 = Node(10,170,"hub.png")
printer_1 = Node(10,215,"printer.png")

done = False
while not done:
    ev = pygame.event.get()
    for event in ev:
        if event.type == pygame.QUIT:
            done = True
    touching = pc_1.hoveringOver()
    if touching == True:
        dragging = drag_drop()
        if dragging == True:
            pc_1.drop()
    else:
        touching = router_1.hoveringOver()
        if touching == True:
            drag_drop()
            if dragging == True:
                router_1.drop()
        else:
            touching = switch_1.hoveringOver()
            if touching == True:
                drag_drop()
                if dragging == True:
                    switch_1.drop()
            else:
                touching = hub_1.hoveringOver()
                if touching == True:
                    drag_drop()
                    if dragging == True:
                        hub_1.drop()
                else:
                    touching = printer_1.hoveringOver()
                    if touching == True:
                        drag_drop()
                        if dragging == True:
                            printer_1.drop()
    pygame.display.flip()
    clock.tick(60)