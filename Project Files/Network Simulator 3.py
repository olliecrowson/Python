import pygame, random, os
pygame.init()
pygame.display.set_caption("Network Simulator")
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,25)
clock = pygame.time.Clock()
nodes = ["cable","pc_1","pc_2","pc_3","pc_4","pc_5","pc_6","pc_7","pc_8","pc_9","pc_10","router_1","router_2","router_3","router_4","router_5","router_6","router_7","router_8","router_9","router_10","switch_1","switch_2","switch_3","switch_4","switch_5","switch_6","switch_7","switch_8","switch_9","switch_10","hub_1","hub_2","hub_3","hub_4","hub_5","hub_6","hub_7","hub_8","hub_9","hub_10","printer_1","printer_2","printer_3","printer_4","printer_5","printer_6","printer_7","printer_8","printer_9","printer_10",]
'''
number_of_pc = 1
number_of_router = 1
number_of_switch = 1
number_of_hub = 1
number_of_printer = 1
'''
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
    def __init__(self, (x, y), image, name, number):
        self.name = str(name)
        self.x = x
        self.y = y
        self.image = pygame.image.load(image)
        self.touching = False
        self.mouse_down = False
        self.clicked = False
        self.number = number
        self.default_x = x
        self.default_y = y

    def returnPosition(self):
        return self.x, self.y

    def blitToScreen(self):
        screen.blit(self.image, (self.x,self.y))
        pygame.draw.line(screen, (230, 30, 30), (90, 0), (90, 720), 6)

    def hoveringOver(self):
        pygame.event.get()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if (mouse_x >= self.x) and (mouse_x <= self.x+40):
            if (mouse_y > self.y) and (mouse_y < self.y+40):
                self.touching = True
                return True

    def dragDrop(self, node_string):
        clock.tick(60)
        ev = pygame.event.get()
        old_x, old_y = self.x, self.y
        for event in ev:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.mouse_down = True
                nodes.append(nodes.pop(nodes.index(node_string)))
                mouse_x, mouse_y = (pygame.mouse.get_pos())
                offset_x = old_x - mouse_x
                offset_y = old_y - mouse_y

        while self.mouse_down:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouse_down = False
                    screen.fill((250,250,250))
                    if self.x < 85: # to delete node
                        self.x, self.y = self.default_x, self.default_y
                        adj_activated = NodeAdjacencyList.ReturnState()
                        if adj_activated:
                            NodeAdjacencyList.RemoveFromDict(node_string)
                    #old_x, old_y = self.x, self.y

                elif self.mouse_down:
                    mouse_x, mouse_y = (pygame.mouse.get_pos())
                    self.x, self.y = mouse_x + offset_x, mouse_y + offset_y
                    screen.fill((250, 250, 250))

                pygame.draw.line(screen, (230, 30, 30), (90, 0), (90, 720), 6)
                callBlitToScreen()

    def ConnectCableToNodes(self):
        clock.tick(60)
        ev = pygame.event.get()
        for event in ev:
            print(event)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.image = pygame.image.load("cable_clicked.png")
                self.blitToScreen()
                pygame.display.flip()

                mouse_down = False
                while not mouse_down:
                    mouse_down, node_from = checkForMouseDown()

                x1, y1 = pygame.mouse.get_pos()
                mouse_down = False
                while not mouse_down:
                    mouse_down, node_to = checkForMouseDown()
                    x2, y2 = pygame.mouse.get_pos()
                    screen.fill((250, 250, 250))
                    pygame.draw.aaline(screen, (0, 0, 255), (x1, y1), (x2, y2), 2)
                    callBlitToScreen()
                    pygame.display.update()

                screen.fill((250, 250, 250))
                callBlitToScreen()
                pygame.display.flip()
                NodeAdjacencyList.AddToDict(node_from, node_to, x1, y1)
                NodeAdjacencyList.DisplayCables()
                self.image = pygame.image.load("cable.png")
                pygame.display.flip()
                #pygame.draw.aaline(screen, (0, 0, 255), (x1, y1), (x2, y2), 2)
                callBlitToScreen()


'''
    def DrawLine(self):
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.image = pygame.image.load("cable_clicked.png")
                self.blitToScreen()
                pygame.display.flip()
                clickedOnceAgain = False
                while clickedOnceAgain != True:
                    ev = pygame.event.get()
                    for event in ev:
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            clickedOnceAgain = True
                            x1, y1 = pygame.mouse.get_pos()
                            clickedTwiceAgain = False
                            while clickedTwiceAgain != True:
                                x2, y2 = pygame.mouse.get_pos()
                                screen.fill((250,250,250))
                                pygame.draw.line(screen, (0,0,255), (x1, y1), (x2, y2))
                                callBlitToScreen()
                                pygame.display.update()
                                ev = pygame.event.get()
                                for event in ev:
                                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                                        clickedTwiceAgain = True
                                        self.image = pygame.image.load("cable.png")
                                        pygame.display.flip()
                                        pygame.draw.line(screen, (0, 0, 255), (x1, y1), (x2, y2))
                                        callBlitToScreen()

class Vertex:
    def __init__(self):
        self.ConnectedTo = []

    def addNeighbor(self,neighbour,weight=0):
        self.ConnectedTo.append(neighbour)

    def getConnections(self):
        return self.ConnectedTo

    def getWeight(self,neighbour):
        return self.ConnectedTo[neighbour]
'''

class AdjacencyList():
    def __init__(self):
        self.Node_Connections = {} # must use dictionary. Dont use list of dicts!
        self.Activated = False

    def AddToDict(self, NodeFrom, NodeTo, x1, y1):
        self.Activated = True
        if not NodeFrom in self.Node_Connections:
            self.Node_Connections[NodeFrom] = [NodeTo] # values are list so can add multiple values to one key
        else:
            self.Node_Connections[NodeFrom].append(NodeTo)

        self.DisplayCables()

    def RemoveFromDict(self, Node):
        for key in self.Node_Connections.keys():
            if key == Node:
                del self.Node_Connections[key]

        for k, v in self.Node_Connections.items(): # k = key, v = values
            self.Node_Connections[k] = filter(lambda x: x != Node, v)

        for k, v in self.Node_Connections.items(): # checks for value empty
            if not v:
                del self.Node_Connections[k]

        self.DisplayCables()

    def ReturnDict(self):
        return self.Node_Connections

    def ReturnState(self):
        return self.Activated

    def DisplayCables(self):
        keys = self.Node_Connections.keys()
        for key in keys:
            for value in self.Node_Connections[key]:
                x1, y1 = eval(value).returnPosition()
                x, y = eval(key).returnPosition()
                pygame.draw.aaline(screen, (0, 0, 255), (x1+20, y1+20), (x+20, y+20), 2)

class PC(Node):
    pass

class Router(Node):
    pass

class Switch(Node):
    pass

class Hub(Node):
    pass

class Printer(Node):
    pass

def callBlitToScreen():
    if NodeAdjacencyList.Activated:
        NodeAdjacencyList.DisplayCables()
    for node in nodes:
        node = eval(node)
        node.blitToScreen()
    pygame.display.flip()

cable = Node((10, 265), "cable.png","cable",1)

pc_1 = Node((10,15),"pc.png","pc",1)
pc_2 = Node((10,15),"pc.png","pc",2)
pc_3 = Node((10,15),"pc.png","pc",3)
pc_4 = Node((10,15),"pc.png","pc",4)
pc_5 = Node((10,15),"pc.png","pc",5)
pc_6 = Node((10,15),"pc.png","pc",6)
pc_7 = Node((10,15),"pc.png","pc",7)
pc_8 = Node((10,15),"pc.png","pc",8)
pc_9 = Node((10,15),"pc.png","pc",9)
pc_10 = Node((10,15),"pc.png","pc",10)

router_1 = Node((10,60),"router.png","router",1)
router_2 = Node((10,60),"router.png","router",1)
router_3 = Node((10,60),"router.png","router",1)
router_4 = Node((10,60),"router.png","router",1)
router_5 = Node((10,60),"router.png","router",1)
router_6 = Node((10,60),"router.png","router",1)
router_7 = Node((10,60),"router.png","router",1)
router_8 = Node((10,60),"router.png","router",1)
router_9 = Node((10,60),"router.png","router",1)
router_10 = Node((10,60),"router.png","router",1)

switch_1 = Node((10,105),"switch.png","switch",1)
switch_2 = Node((10,105),"switch.png","switch",1)
switch_3 = Node((10,105),"switch.png","switch",1)
switch_4 = Node((10,105),"switch.png","switch",1)
switch_5 = Node((10,105),"switch.png","switch",1)
switch_6 = Node((10,105),"switch.png","switch",1)
switch_7 = Node((10,105),"switch.png","switch",1)
switch_8 = Node((10,105),"switch.png","switch",1)
switch_9 = Node((10,105),"switch.png","switch",1)
switch_10 = Node((10,105),"switch.png","switch",1)

hub_1 = Node((10,170),"hub.png","hub",1)
hub_2 = Node((10,170),"hub.png","hub",1)
hub_3 = Node((10,170),"hub.png","hub",1)
hub_4 = Node((10,170),"hub.png","hub",1)
hub_5 = Node((10,170),"hub.png","hub",1)
hub_6 = Node((10,170),"hub.png","hub",1)
hub_7 = Node((10,170),"hub.png","hub",1)
hub_8 = Node((10,170),"hub.png","hub",1)
hub_9 = Node((10,170),"hub.png","hub",1)
hub_10 = Node((10,170),"hub.png","hub",1)

printer_1 = Node((10,215),"printer.png","printer",1)
printer_2 = Node((10,215),"printer.png","printer",1)
printer_3 = Node((10,215),"printer.png","printer",1)
printer_4 = Node((10,215),"printer.png","printer",1)
printer_5 = Node((10,215),"printer.png","printer",1)
printer_6 = Node((10,215),"printer.png","printer",1)
printer_7 = Node((10,215),"printer.png","printer",1)
printer_8 = Node((10,215),"printer.png","printer",1)
printer_9 = Node((10,215),"printer.png","printer",1)
printer_10 = Node((10,215),"printer.png","printer",1)

NodeAdjacencyList = AdjacencyList()

def checkForMouseDown():
    nodes.remove("cable")
    for node in nodes:
        node_string = node
        node = eval(node)
        touching = node.hoveringOver()
        while touching:
            touching = node.hoveringOver()
            clock.tick(60)
            ev = pygame.event.get()
            for event in ev:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    nodes.append("cable")
                    return True, node_string
    nodes.append("cable")
    return False, None

def runProgram():
    pygame.draw.line(screen, (230, 30, 30), (90, 0), (90, 720), 6)
    for node in nodes:
        node_string = node
        node = eval(node)
        node.blitToScreen()
        touching = node.hoveringOver()
        while touching:
            touching = node.hoveringOver()
            if node_string != "cable":
                node.dragDrop(node_string)
            else:
                node.ConnectCableToNodes()

    pygame.display.flip()






    '''
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
    '''


'''
def refreshNodes():

    # ERROR IS BECAUSE PC_2 IS NOT DEFINED OUTSIDE CLASS AND THEREFORE IT WILL RUN WHEN SENT TO IT BUT AFTER 1 ITERATION BACK TO SQUARE 1
    # WHEN THE nextNode IS NOT SENT
    pygame.display.flip()
    runProgram()

refreshNodes()
'''

done = False

while not done:
    done = runProgram()
    ev = pygame.event.get()
    for event in ev:
        if event.type == pygame.QUIT:
            done = True