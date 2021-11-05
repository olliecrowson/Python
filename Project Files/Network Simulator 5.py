import pygame, random, os

pygame.init()
pygame.display.set_caption("Network Simulator")
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 25)
clock = pygame.time.Clock()

FPS = 60
screenInfo = pygame.display.Info()
screen = pygame.display.set_mode((screenInfo.current_w, screenInfo.current_h - 64))
screen.fill((250, 250, 250))
pygame.draw.line(screen, (230, 30, 30), (90, 0), (90, 720), 6)
# white_block = pygame.draw.rect(screen,(255,255,255),(pygame.mouse.get_pos(),(20,20)))
pygame.display.update()

'''
def menu():
    backgroundScreen = pygame.image.load(background)
    screen.blit(backgroundScreen, (0,0))
    pygame.display.update()
'''


class Node(object):  # object because it is parent class
    def __init__(self, (x, y), image, name, number, CompatibleNodes):
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
        self.activated = False
        self.CompatibleNodes = CompatibleNodes

    def returnActivated(self):
        return self.activated

    def returnName(self):
        return self.name

    def returnPosition(self):
        return self.x, self.y

    def returnCompatibleNodes(self):
        return self.CompatibleNodes

    def blitToScreen(self):
        screen.blit(self.image, (self.x, self.y))
        pygame.draw.line(screen, (230, 30, 30), (90, 0), (90, 720), 6)

    def hoveringOver(self):
        pygame.event.get()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if (mouse_x >= self.x) and (mouse_x <= self.x + 40):
            if (mouse_y > self.y) and (mouse_y < self.y + 40):
                self.touching = True
                return True

    def dragDrop(self, node):
        clock.tick(FPS)
        ev = pygame.event.get()
        old_x, old_y = self.x, self.y
        for event in ev:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.mouse_down = True
                nodes.append(nodes.pop(nodes.index(node)))
                mouse_x, mouse_y = (pygame.mouse.get_pos())
                offset_x = old_x - mouse_x
                offset_y = old_y - mouse_y

        while self.mouse_down:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouse_down = False
                    screen.fill((250, 250, 250))
                    if self.x < 85:  # to delete node
                        self.x, self.y = self.default_x, self.default_y
                        self.activated = False
                        adj_activated = NodeAdjacencyList.ReturnState()
                        if adj_activated:
                            NodeAdjacencyList.RemoveFromDict(node)
                            # old_x, old_y = self.x, self.y

                elif self.mouse_down:
                    mouse_x, mouse_y = (pygame.mouse.get_pos())
                    self.x, self.y = mouse_x + offset_x, mouse_y + offset_y
                    screen.fill((250, 250, 250))
                    self.activated = True

                pygame.draw.line(screen, (230, 30, 30), (90, 0), (90, 720), 6)
                callBlitToScreen()

    def ConnectCableToNodes(self):
        clock.tick(FPS)
        ev = pygame.event.get()  # must be on top!!
        done = True
        for event in ev:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.image = pygame.image.load("cable_clicked.png")
                self.blitToScreen()
                pygame.display.flip()
                done = False

        while not done:
            mouse_down = False

            while not mouse_down:
                mouse_down, node_from = checkForMouseDown(1)
                if mouse_down and node_from != None:
                    if node_from.returnActivated() == False:
                        mouse_down = False

            exit_cable = False
            if node_from == None:
                exit_cable = True

            x1, y1 = pygame.mouse.get_pos()
            mouse_down = False
            node_to = None
            while not mouse_down and not exit_cable:
                mouse_down, node_to = checkForMouseDown(1)
                if mouse_down and node_to != None:
                    if not node_to.returnActivated():
                        mouse_down = False
                    elif node_to.returnName() not in node_from.returnCompatibleNodes():
                        mouse_down = False
                x2, y2 = pygame.mouse.get_pos()
                screen.fill((250, 250, 250))
                pygame.draw.aaline(screen, (0, 0, 255), (x1, y1), (x2, y2), 2)
                callBlitToScreen()
                pygame.display.update()

            if node_from != None and node_to != None:
                screen.fill((250, 250, 250))
                pygame.display.flip()
                NodeAdjacencyList.AddToDict(node_from, node_to, x1, y1)
                NodeAdjacencyList.DisplayCables()
                callBlitToScreen()
                pygame.display.flip()
                # pygame.draw.aaline(screen, (0, 0, 255), (x1, y1), (x2, y2), 2)

            else:
                done = True
                screen.fill((250, 250, 250))
                self.image = pygame.image.load("cable.png")
                callBlitToScreen()
                pygame.display.flip()


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


class AdjacencyList(object):
    def __init__(self):
        self.Node_Connections = {}  # must use dictionary. Dont use list of dicts!
        self.Activated = False

    def AddToDict(self, NodeFrom, NodeTo, x1, y1):
        self.Activated = True
        if not NodeFrom in self.Node_Connections:
            self.Node_Connections[NodeFrom] = [NodeTo]  # values are list so can add multiple values to one key
        else:
            self.Node_Connections[NodeFrom].append(NodeTo)

    def RemoveFromDict(self, Node):
        for key in self.Node_Connections.keys():
            if key == Node:
                del self.Node_Connections[key]

        for k, v in self.Node_Connections.items():  # k = key, v = values
            self.Node_Connections[k] = filter(lambda x: x != Node, v)

        for k, v in self.Node_Connections.items():  # checks for value empty
            if not v:
                del self.Node_Connections[k]

    def ReturnDict(self):
        return self.Node_Connections

    def ReturnState(self):
        return self.Activated

    def DisplayCables(self):
        keys = self.Node_Connections.keys()
        for key in keys:
            for value in self.Node_Connections[key]:
                x1, y1 = value.returnPosition()
                x, y = key.returnPosition()
                pygame.draw.aaline(screen, (0, 0, 255), (x1 + 20, y1 + 20), (x + 20, y + 20), 2)


class CalculatePacketPath(AdjacencyList):
    def __init__(self):
        super(AdjacencyList, self).__init__()
    def CalculateRequirements(self):
        for node in nodes[1:]:
            node.returnPropert





def checkForMouseDown(starting_node):
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for node in nodes[starting_node:]:  # [1:] means skip first element (Cable)
                if node.hoveringOver():
                    return True, node

            return True, None

    return False, None



class PC(Node):
    def __init__(self, RunningApplications):
        self.CompatibleNodes = []
        super(PC, self).__init__
        self.RunningApplications = RunningApplications
        self.name = "pc"

    def ReturnRunningApplications(self):
        return self.RunningApplications


class Router(Node):
    def __init__(self):
        super(Node, self).__init__()


class Switch(Node):
    def __init__(self):
        super(Node, self).__init__()


class Hub(Node):
    def __init__(self):
        super(Node, self).__init__()


class Printer(Node):
    def __init__(self):
        super(Node, self).__init__()

class Cable(Node):
    def __init__(self):
        super(Node, self).__init__()

def callBlitToScreen():
    if NodeAdjacencyList.Activated:
        NodeAdjacencyList.DisplayCables()
    for node in nodes:
        node.blitToScreen()
    pygame.display.flip()


NUMBER_PCS = 15
NUMBER_ROUTERS = 5
NUMBER_SWITCHES = 5
NUMBER_HUBS = 5
NUMBER_PRINTERS = 5

PC_COMPATIBLE_NODES = ["pc", "router", "switch", "hub", "printer"]
ROUTER_COMPATIBLE_NODES = ["pc", "switch", "hub", "printer"]
SWITCH_COMPATIBLE_NODES = ["pc", "router", "switch", "hub", "printer"]
HUB_COMPATIBLE_NODES = ["pc", "router", "switch", "hub", "printer"]
PRINTER_COMPATIBLE_NODES = ["pc", "router", "switch", "hub"]


PCs = [Node((10, 15), "pc.png", "pc", 1, PC_COMPATIBLE_NODES) for x in range(NUMBER_PCS)]
Routers = [Node((10, 60), "router.png", "router", 1, ROUTER_COMPATIBLE_NODES) for x in range(NUMBER_ROUTERS)]
Switches = [Node((10, 105), "switch.png", "switch", 1, SWITCH_COMPATIBLE_NODES) for x in range(NUMBER_SWITCHES)]
Hubs = [Node((10, 170), "hub.png", "hub", 1, HUB_COMPATIBLE_NODES) for x in range(NUMBER_HUBS)]
Printers = [Node((10, 215), "printer.png", "printer", 1, PRINTER_COMPATIBLE_NODES) for x in range(NUMBER_PRINTERS)]
Cable = Node((10, 265), "cable.png", "cable", 1, None)

nodes = []

# combine all nodes into one list for easy iteration
nodes.append(Cable)
nodes.extend(PCs)
nodes.extend(Routers)
nodes.extend(Switches)
nodes.extend(Hubs)
nodes.extend(Printers)

NodeAdjacencyList = AdjacencyList()


def runProgram():
    pygame.draw.line(screen, (230, 30, 30), (90, 0), (90, 720), 6)
    for node in nodes:
        node.blitToScreen()
        touching = node.hoveringOver()
        while touching:
            touching = node.hoveringOver()
            if node.returnName() != "cable":
                node.dragDrop(node)
            else:
                node.ConnectCableToNodes()

    pygame.display.flip()


done = False

while not done:
    ev = pygame.event.get()
    for event in ev:
        if event.type == pygame.QUIT:
            done = True
    runProgram()