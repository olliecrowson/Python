import pygame, random, os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,25)
pygame.init()
clock = pygame.time.Clock()
screenInfo = pygame.display.Info()
screen = pygame.display.set_mode((screenInfo.current_w, screenInfo.current_h-64))
screen.fill((250,250,250))
pygame.draw.line(screen,(230,30,30),(90,0),(90,720),6)
#white_block = pygame.draw.rect(screen,(255,255,255),(pygame.mouse.get_pos(),(20,20)))
pygame.display.update()
'''
def menu():
    backgroundScreen = pygame.image.load(background)
    screen.blit(backgroundScreen, (0,0))
    pygame.display.update()
'''

class Node:
    def __init__(self, (x, y), image, name):
        self.name = name
        self.x = x
        self.y = y
        self.image = pygame.image.load(image)
        self.touching = False
        self.mouse_down = False

    def blitToScreen(self):
        screen.blit(self.image, (self.x,self.y))

    def hoveringOver(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if (mouse_x >= self.x) and (mouse_x <= self.x+40):
            if (mouse_y > self.y) and (mouse_y < self.y+40):
                self.touching = True
                return True

    def dragDrop(self, ev):
        for event in ev:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.mouse_down = True

        while self.mouse_down:
            ev = pygame.event.get()
            for event in ev:
                if event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_down = False
                else:
                    screen.fill((250,250,250))
                    self.x,self.y = (pygame.mouse.get_pos())
                    refreshNodes()
                    pygame.display.flip()


def refreshNodes():
    pygame.draw.line(screen, (230, 30, 30), (90, 0), (90, 720), 6)
    pc_1.blitToScreen()
    router_1.blitToScreen()
    switch_1.blitToScreen()
    hub_1.blitToScreen()
    printer_1.blitToScreen()

pc_1 = Node((10,15),"pc.png","pc_1")
router_1 = Node((10,60),"router.png","router_1")
switch_1 = Node((10,105),"switch.png","switch_1")
hub_1 = Node((10,170),"hub.png","hub_1")
printer_1 = Node((10,215),"printer.png","printer_1")
refreshNodes()

done = False
while not done:
    ev = pygame.event.get()
    for event in ev:
        if event.type == pygame.QUIT:
            done = True
    touching = pc_1.hoveringOver()
    if touching == True:
        pc_1.dragDrop(ev)
    else:
        touching = router_1.hoveringOver()
        if touching == True:
            router_1.dragDrop(ev)
        else:
            touching = switch_1.hoveringOver()
            if touching == True:
                switch_1.dragDrop(ev)
            else:
                touching = hub_1.hoveringOver()
                if touching == True:
                    hub_1.dragDrop(ev)
                else:
                    touching = printer_1.hoveringOver()
                    if touching == True:
                        printer_1.dragDrop(ev)
    pygame.display.flip()
    clock.tick(60)