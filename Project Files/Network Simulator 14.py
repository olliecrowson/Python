import pygame, random, os, pickle, Database, time
pygame.init()
pygame.display.set_caption("Network Simulator")
pygame.font.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 25)
clock = pygame.time.Clock()

colours = [(255,0,0), (0,0,255), (255,0,255), (128,128,0), (255,69,0), (0,100,0), (139,69,19), (105,105,105)]

FPS = 60
screenInfo = pygame.display.Info()
screen = pygame.display.set_mode((screenInfo.current_w, screenInfo.current_h - 64))
screen.fill((250, 250, 250))

# white_block = pygame.draw.rect(screen,(255,255,255),(pygame.mouse.get_pos(),(20,20)))
pygame.display.update()

'''
def menu():
    backgroundScreen = pygame.image.load(background)
    screen.blit(backgroundScreen, (0,0))
    pygame.display.update()
'''


class Node(object):  # object because it is parent class
    def __init__(self, (x, y), image, selected_image, name, number, movable, text, compatible_nodes):
        self.name = str(name)
        self.x = x
        self.y = y
        self.default_x = x
        self.default_y = y
        self.image = pygame.image.load(image)
        self.default_image = pygame.image.load(image)
        if selected_image:
            self.selected_image = pygame.image.load(selected_image)
        self.text = text
        self.touching = False
        self.mouse_down = False
        self.clicked = False
        self.number = number
        self.activated = False
        self.CompatibleNodes = compatible_nodes
        self.current = False
        self.Properties = []
        self.PropertiesWindowActivated = False
        self.movable = movable

    def UpdatePosition(self, (x, y)):
        self.x = x
        self.y = y

    def returnSize(self):
        return self.image.get_rect().size

    def returnActivated(self):
        return self.activated

    def returnName(self):
        return self.name.lower()

    def returnPosition(self):
        return self.x, self.y

    def returnStatus(self):
        return self.current

    def returnCompatibleNodes(self):
        return self.CompatibleNodes

    def blitToScreen(self):
        screen.blit(self.image, (self.x, self.y))

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
                last_click = pygame.time.get_ticks()
                self.mouse_down = True
                nodes.append(nodes.pop(nodes.index(node)))
                mouse_x, mouse_y = pygame.mouse.get_pos()
                offset_x = old_x - mouse_x
                offset_y = old_y - mouse_y

        while self.mouse_down:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouse_down = False
                    last_release = pygame.time.get_ticks()
                    if last_release - last_click < 100:  # track if dragged or clicked
                        if self.activated:
                            if self.PropertiesWindowActivated:
                                self.SelectProperty()
                            else:
                                self.CreatePropertiesWindow()
                    else:
                        screen.fill((250, 250, 250))
                        self.activated = True
                        if self.x < 85:  # to delete node
                            self.x, self.y = self.default_x, self.default_y
                            self.activated = False
                            adj_activated = NodeAdjacencyList.ReturnState()
                            if adj_activated:
                                NodeAdjacencyList.RemoveFromDict(node)
                                PacketPath.RemovePacket(node)
                                # old_x, old_y = self.x, self.y
                        elif PacketPath.returnActivated():
                            for packet in packets:
                                packet.CalculateGradient()

                elif self.mouse_down and self.movable:
                    mouse_x, mouse_y = (pygame.mouse.get_pos())
                    self.x, self.y = mouse_x + offset_x, mouse_y + offset_y
                    screen.fill((250, 250, 250))

                callBlitToScreen()

    def CreatePropertiesWindow(self):
        self.current = True
        self.checkbox_coordinates = []
        self.PropertiesWindowActivated = True
        x = 50
        y = 90
        self.image = self.selected_image
        callBlitToScreen()
        # print(node_image)  to get dimensions (send self.image)
        self.window_surface = pygame.Surface((400, 500))
        self.window_surface.fill((255, 255, 255))
        pygame.draw.rect(screen, (0, 0, 0), (500, 50, 400, 500), 8)
        text = pygame.font.SysFont('Comic Sans MS', 25)
        node_name_text = text.render(self.name, True, (0, 0, 0))
        text = pygame.font.SysFont('Comic Sans MS', 20)
        words = [word.split(' ') for word in self.text.splitlines()]  # 2D array where each row is a list of words.

        for line in words:  # can't render line breaks
            for word in line:
                node_properties_text = text.render(word, True, (0, 0, 0))
                word_width, word_height = node_properties_text.get_size()
                self.window_surface.blit(node_properties_text, (x, y))
                if word:  # if not new line
                    x = x + (word_width + 5)
            x = 50
            y = y + (word_height + 9)
            if not line[0]:  # do not create a button next to title
                pygame.draw.circle(self.window_surface, (0, 0, 0), (x - 16, y - 22), 12, 1)
                self.checkbox_coordinates.append([x - 16, y - 22, line])
                line.pop(0)

        self.window_surface.blit(self.default_image, (50, 10))
        self.window_surface.blit(node_name_text, (50, 50))
        screen.blit(self.window_surface, (500, 50))  # must be after blitting image to surface
        pygame.display.update()
        self.SelectProperty()

    def SelectProperty(self):
        done = False
        pygame.draw.rect(screen, (0, 0, 0), (500, 50, 400, 500), 8)
        screen.blit(self.window_surface, (500, 50))
        pygame.display.update()
        while not done:
            for event in pygame.event.get():
                for coordinate in self.checkbox_coordinates:
                    x, y = pygame.mouse.get_pos()
                    if event.type == pygame.MOUSEBUTTONUP:
                        if (x <= (coordinate[0] + 511)) and ((x >= coordinate[0] + 488)):
                            if (y <= (coordinate[1] + 61)) and ((y >= coordinate[1] + 38)):
                                selection = coordinate[2]

                                # selection.pop(0)
                                selection = ' '.join(str(x) for x in selection)

                                if selection in self.Properties:

                                    self.Properties.remove(selection)
                                    pygame.draw.rect(self.window_surface, (255, 255, 255),
                                                     (coordinate[0] - 12, coordinate[1] - 12, 24, 24))
                                    pygame.draw.circle(self.window_surface, (0, 0, 0), (coordinate[0], coordinate[1]),
                                                       12, 1)
                                    for server in Server_drives:
                                        if server.returnActivated():
                                            server.RemoveReduntantCables()

                                else:
                                    self.window_surface.blit(pygame.image.load("tick.png"),
                                                             (coordinate[0] - 9, coordinate[1] - 7))
                                    # self.Properties.append(' '.join(x) for x in properties)
                                    self.Properties.append(selection)
                                    # self.Properties = [''.join(x) for x in self.Properties]

                        elif (x < 500) or (x > 900) or (y < 50) or (y > 550):
                            done = True

                        screen.blit(self.window_surface, (500, 50))
                        pygame.display.update()

        screen.fill((250, 250, 250))
        callBlitToScreen()
        # if properties:
        # for item in properties:
        # item.pop(0)  # remove quotation marks at start of list

        self.current = False

        PacketPath.CreatePackets()

class PC(Node):
    def __init__(self):
        self.text1 = "Applications running:\n Word processing\n Internet browsing\n Multimedia\n E-mailing\n"
        self.CompatibleNodes = ["router", "switch", "hub", "printer"]
        super(PC, self).__init__((10, 15), "pc.png", "pc_selected.png", "PC", 1, True, self.text1, self.CompatibleNodes)
        try:
            self.colour = random.choice(colours)
            colours.remove(self.colour)
        except IndexError: # if not enough colours to choose from
            self.colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def FindPath(self):
        pass

    def ReturnRunningApplications(self):
        return self.Properties

    def UpdateApplications(self, property):
        self.Properties = property

    def CalculateNodeConnections(self, property):
        # refresh packets everytime change property
        if property == "Word processing":
            return ["printer", "print server", "file server"]
        elif property == "Internet browsing":
            return ["router", "web cache"]
        elif property == "Multimedia":
            return ["multimedia server"]
        elif property == "E-mailing":
            return ["e-mail server"]
        else: #intranet
            return ["file server"]

    def ReturnColour(self):
        return self.colour

class Router(Node):
    def __init__(self):
        self.text1 = "Applications running:\n None"
        self.CompatibleNodes = ["pc", "switch", "hub"]
        super(Router, self).__init__((10, 60), "router.png", "router_selected.png", "Router", 1, True, self.text1,
                                     self.CompatibleNodes)


class Switch(Node):
    def __init__(self):
        self.text1 = "Applications running:\n None"
        self.CompatibleNodes = ["pc", "switch", "router", "printer", "file server", "print server",
                                "e-mail server", "multimedia server", "web cache"]
        super(Switch, self).__init__((10, 105), "switch.png", "switch_selected.png", "Switch", 1, True, self.text1,
                                     self.CompatibleNodes)


class Hub(Node):
    def __init__(self):
        self.text1 = "Applications running:\n None"
        self.CompatibleNodes = ["pc", "router", "switch", "hub", "printer", "file server", "print server",
                                "e-mail server", "multimedia server", "web cache"]
        super(Hub, self).__init__((10, 170), "hub.png", "hub_selected.png", "Hub", 1, True, self.text1,
                                  self.CompatibleNodes)


class Printer(Node):
    def __init__(self):
        self.text1 = "Applications running:\n None"
        self.CompatibleNodes = ["pc", "switch", "hub"]
        super(Printer, self).__init__((10, 215), "printer.png", "printer_selected.png", "Printer", 1, True, self.text1,
                                      self.CompatibleNodes)


class Server(Node):
    def __init__(self):
        self.text1 = "Server functions:\n File server\n Print server\n E-mail server\n Multimedia server\n Web cache"
        self.CompatibleNodes = ["switch", "hub"]
        self.drive_image = pygame.image.load("server_drive.png")
        self.imported = False
        super(Server, self).__init__((10, 265), "server.png", "server_selected.png", "Server", 1, False, self.text1,
                                     self.CompatibleNodes)

    def CreateServer(self):
        done = True
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.image = self.selected_image
                self.blitToScreen()
                pygame.display.flip()
                done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.activated = True
                    done = True
                    self.server_x, self.server_y = pygame.mouse.get_pos()
                    self.surface = pygame.Surface((100, 350))
                    self.surface.fill((255, 255, 255))
                    pygame.draw.rect(screen, (0, 0, 0), (self.server_x, self.server_y, 100, 350), 8)

                    self.move_surface = pygame.Surface((100, 15))
                    self.move_surface.fill((80, 80, 80))
                    self.surface.blit(self.move_surface, (0, 0))
                    screen.blit(self.surface, (self.server_x, self.server_y))

                    pygame.display.flip()
                    clock.tick(0.9)
                    self.CreatePropertiesWindow()
                    self.image = self.default_image
                    self.blitToScreen()
                    pygame.display.flip()

    def DisplayDrives(self):
        text = pygame.font.SysFont('Comic Sans MS', 13)
        self.surface.fill((255, 255, 255))
        self.move_surface = pygame.Surface((100, 15))
        self.move_surface.fill((80, 80, 80))
        self.surface.blit(self.move_surface, (0, 0))

        for drive in self.Properties:
            if drive == "File server":
                node_name_text = text.render("File server", True, (0, 0, 0))
                screen.blit(node_name_text, (self.server_x + 13, self.server_y + 60))
                File_server.UpdatePosition((self.server_x + 10, self.server_y + 20))
                Server_drives[0].blitToScreen()

            elif drive == "Print server":
                node_name_text = text.render("Print server", True, (0, 0, 0))
                screen.blit(node_name_text, (self.server_x + 11, self.server_y + 125))
                Print_server.UpdatePosition((self.server_x + 10, self.server_y + 85))
                Print_server.blitToScreen()

            elif drive == "E-mail server":
                node_name_text = text.render("E-mail server", True, (0, 0, 0))
                screen.blit(node_name_text, (self.server_x + 8, self.server_y + 190))
                Email_server.UpdatePosition((self.server_x + 10, self.server_y + 150))
                Email_server.blitToScreen()

            elif drive == "Multimedia server":
                node_name_text = text.render("Media server", True, (0, 0, 0))
                screen.blit(node_name_text, (self.server_x + 8, self.server_y + 255))
                Multimedia_server.UpdatePosition((self.server_x + 10, self.server_y + 215))
                Multimedia_server.blitToScreen()

            elif drive == "Web cache":
                node_name_text = text.render("Web cache", True, (0, 0, 0))
                screen.blit(node_name_text, (self.server_x + 13, self.server_y + 320))
                Web_Cache_server.UpdatePosition((self.server_x + 10, self.server_y + 280))
                Web_Cache_server.blitToScreen()

    def RemoveReduntantCables(self):
        adj_activated = NodeAdjacencyList.ReturnState()  # Removing reduntant cables after deselection of servers
        if adj_activated:
            for drive in Server_drives:
                drive_name = drive.returnName()
                drive_name = drive_name[0].upper() + drive_name[1:]
                if drive_name not in self.Properties:
                    NodeAdjacencyList.RemoveFromDict(drive)


    def BlitServer(self):
        pygame.draw.rect(screen, (0, 0, 0), (self.server_x, self.server_y, 100, 350), 7)
        screen.blit(self.surface, (self.server_x, self.server_y))
        self.DisplayDrives()
        # pygame.display.flip()

    def ReturnProperties(self):
        return self.Properties

    def UpdateProperties(self, properties):
        self.Properties = properties

    def returnPosition(self):
        return self.server_x, self.server_y

    def UpdatePosition(self, (x, y)):
        self.imported = True
        self.activated = True
        self.server_x, self.server_y = x, y
        self.surface = pygame.Surface((100, 350))
        self.surface.fill((255, 255, 255))
        pygame.draw.rect(screen, (0, 0, 0), (self.server_x, self.server_y, 100, 350), 8)

        self.move_surface = pygame.Surface((100, 15))
        self.move_surface.fill((80, 80, 80))
        self.surface.blit(self.move_surface, (0, 0))
        screen.blit(self.surface, (self.server_x, self.server_y))

        pygame.display.flip()


    def CheckForMovementOrSelection(self):
        done = False
        x, y = pygame.mouse.get_pos()
        if self.server_x <= x <= self.server_x + 100:
            if self.server_y <= y <= self.server_y + 15:
                #clock.tick(FPS)
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        last_click = pygame.time.get_ticks()
                        x, y = pygame.mouse.get_pos()
                        offset_x = self.server_x - x
                        offset_y = self.server_y - y
                        while not done:
                            for event in pygame.event.get():
                                if event.type == pygame.MOUSEBUTTONUP:
                                    last_release = pygame.time.get_ticks()
                                    done = True
                                    if last_release - last_click < 100:
                                        if self.imported:
                                            self.CreatePropertiesWindow()
                                            self.imported = False
                                        self.SelectProperty()
                                        self.DisplayDrives()

                                    elif self.server_x < 85:
                                        self.activated = False
                                        screen.fill((250, 250, 250))
                                        callBlitToScreen()

                                    elif PacketPath.returnActivated():
                                        for packet in packets:
                                            packet.CalculateGradient()

                                else:
                                    x, y = pygame.mouse.get_pos()
                                    self.server_x, self.server_y = x + offset_x, y + offset_y
                                    screen.fill((250, 250, 250))
                                    callBlitToScreen()


class Cable(Node):
    def __init__(self):
        super(Cable, self).__init__((10, 315), "cable.png", "cable_selected.png", "Cable", 1, False, None, None)

    def ConnectCableToNodes(self):
        clock.tick(FPS)
        ev = pygame.event.get()  # must be on top!!
        done = True
        for event in ev:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.image = self.selected_image
                self.blitToScreen()
                pygame.display.flip()
                done = False

        while not done:
            mouse_down = False

            while not mouse_down:
                mouse_down, node_from = checkForMouseDown()
                if mouse_down and node_from != None:
                    if not node_from.returnActivated():
                        if not "server" in node_from.returnName():
                            mouse_down = False
                screen.fill((250,250,250))
                callBlitToScreen()

            exit_cable = False
            if node_from == None:
                exit_cable = True

            x1, y1 = pygame.mouse.get_pos()
            mouse_down = False
            node_to = None

            while not mouse_down and not exit_cable:
                mouse_down, node_to = checkForMouseDown()
                if mouse_down and node_to != None:
                    if not node_from.returnActivated():
                        if not "server" in node_from.returnName():
                            mouse_down = False
                    if node_to.returnName() not in node_from.returnCompatibleNodes():
                        mouse_down = False
                x2, y2 = pygame.mouse.get_pos()
                screen.fill((250, 250, 250))
                pygame.draw.aaline(screen, (0, 0, 255), (x1, y1), (x2, y2), 2)
                callBlitToScreen()
                pygame.display.flip()


            if node_from != None and node_to != None:
                #screen.fill((250, 250, 250))
                #pygame.display.flip()
                NodeAdjacencyList.AddToDict(node_from, node_to)
                callBlitToScreen()
                # pygame.draw.aaline(screen, (0, 0, 255), (x1, y1), (x2, y2), 2)

            else:
                done = True
                #screen.fill((250, 250, 250))
                self.image = pygame.image.load("cable.png")
                #callBlitToScreen()


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

    def AddToDict(self, NodeFrom, NodeTo):
        self.Activated = True
        if NodeFrom.returnName() == "pc":
            if NodeFrom in self.Node_Connections:
                self.Node_Connections[NodeFrom].append(NodeTo)
            else:
                self.Node_Connections[NodeFrom] = [NodeTo]
        elif NodeTo.returnName() == "pc":
            if NodeTo in self.Node_Connections:
                self.Node_Connections[NodeTo].append(NodeFrom)
            else:
                self.Node_Connections[NodeTo] = [NodeFrom]

        elif NodeFrom.returnName() in ("switch", "hub"):
            if NodeFrom in self.Node_Connections:
                self.Node_Connections[NodeFrom].append(NodeTo)
            else:
                self.Node_Connections[NodeFrom] = [NodeTo]
        else:
            if NodeTo in self.Node_Connections:
                self.Node_Connections[NodeTo].append(NodeFrom)
            else:
                self.Node_Connections[NodeTo] = [NodeFrom]

        PacketPath.CreatePackets()

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

    #def ImportCables(self):



'''
        if not NodeFrom or not NodeTo in self.Node_Connections:
            if NodeTo.returnName() in ("switch", "hub"):
                self.Node_Connections[NodeTo] = [NodeFrom]  # values are list so can add multiple values to one key
            else:
                self.Node_Connections[NodeFrom] = [NodeTo]
        elif NodeTo.returnName() in ("switch", "hub"):
            self.Node_Connections[NodeTo].append(NodeFrom) ## Node from or Switch from?
            print("HUB")
        else:
            print("Switch")
            self.Node_Connections[NodeFrom].append(NodeTo)
'''

'''
class CalculatePacketPath:
    def __init__(self):
        self.NodeHierarchy = ["pc"]
        self.Path = {}  # list or dict?

    def CalculatePath(self):
        adjacency_list = NodeAdjacencyList.ReturnDict()
        #adjacency_list = sorted(adjacency_list.items(), key=lambda pair: self.NodeHierarchy.index(pair[0]))
        print(adjacency_list)

    def CalculateRequirements(self):
        for node in nodes[1:]:
            if node.returnName() == "pc":
                application = node.ReturnRunningApplications()
'''

class CreatePacketPath:
    def __init__(self):
        self.connections = []
        self.activated = False
        self.index = 0
        self.pc_complete = False

    def returnActivated(self):
        return self.activated

    def CreatePackets(self):
        self.route_number = 0
        self.activated = True
        self.temp_packets = []
        del packets[0:]
        self.adjacency_list = NodeAdjacencyList.ReturnDict()
        for node_from in self.adjacency_list:
            if node_from.returnName() == "pc":
                self.visited = []
                if node_from.ReturnRunningApplications():
                    self.RecursiveDepthSearch(node_from)


    def RecursiveDepthSearch(self, node_from): # this is used to find the path to take between all the nodes
        self.visited.append(node_from)
        #print(node_from)
        temp_nodes = []
        for node_to in self.adjacency_list[node_from]:
            if node_from.returnName() == "pc":
                self.colour = node_from.ReturnColour()
                self.root_node = node_from
                self.route_number += 1
                properties = node_from.ReturnRunningApplications()
                self.connections = []
                for property in properties:
                    self.connections.extend(node_from.CalculateNodeConnections(property))

                if node_to.returnName() in self.connections:
                    packets.append(Packets(node_from, node_to, self.colour, 1))
                elif node_to.returnName() in ("switch", "hub"):
                    self.temp_packets.append([self.route_number, node_from, node_to, 1])

            elif node_to.returnName() in self.connections:
                unique_temp_packets = []
                for elem in self.temp_packets:
                    if elem not in unique_temp_packets:
                        unique_temp_packets.append(elem)
                for temp_list in unique_temp_packets:
                    #print(temp_list)
                    if temp_list[0] == self.route_number:
                        packets.append(Packets(temp_list[1], temp_list[2], self.colour, temp_list[3]))
                if node_to.returnName() in ("file server", "print server", "e-mail server", "multimedia server", "web cache"):
                    if node_from.returnName() == "hub":
                        num = 2
                    else:
                        num = 3
                    packets.append(Packets(node_from, node_to, self.colour, num))
                    self.hierarchy = num
                    self.server = None
                    self.unsecure_network = False
                    self.ReverseRecursiveSearch(node_to)
                elif node_from.returnName() in ("hub", "switch"):
                    if node_to.returnName() == "printer": # check if connected to print server. If so - go there then printer
                        for nodes in self.adjacency_list.values():
                            for node in nodes:
                                temp_nodes.append(node)

                        if not any(node.returnName() == "print server" for node in temp_nodes):
                            if node_from.returnName() == "hub":
                                packets.append(Packets(node_from, node_to, self.colour, 2))
                            elif node_from.returnName() == "switch":
                                packets.append(Packets(node_from, node_to, self.colour, 3))

                    elif node_from.returnName() == "hub":
                        packets.append(Packets(node_from, node_to, self.colour, 2))
                    else:
                        packets.append(Packets(node_from, node_to, self.colour, 3))

            elif node_to.returnName() in ("switch", "hub"):
                self.temp_packets.append([self.route_number, node_from, node_to, 2])

            #print(node_to, self.adjacency_list)
            if node_to in self.adjacency_list:
                self.RecursiveDepthSearch(node_to)

    def ReverseRecursiveSearch(self, node_from):
        if not self.unsecure_network:
            self.hierarchy += 1
        self.temp_2 = []
        if node_from.returnName() == "print server":
            self.server = "print server"

        if node_from == self.root_node:
            if self.server == "print server":
                self.hierarchy_2 = self.hierarchy
                self.targetedSearch(node_from, "printer")

        else:
            for key, value in self.adjacency_list.items():
                add_route = True
                if node_from in value:
                    if key not in self.visited:
                        if not node_from.returnName() == "hub":
                            add_route = False
                        else:
                            self.unsecure_network = True

                    elif node_from.returnName() == "hub":
                        self.unsecure_network = True

                    if add_route:
                        packets.append(Packets(node_from, key, self.colour, self.hierarchy))
                        self.ReverseRecursiveSearch(key)

    def targetedSearch(self, node_from, node_to):
        self.hierarchy_2 += 1
        #print(node_from, node_to, self.hierarchy_2)
        for connected_node in self.adjacency_list[node_from]:
            if connected_node.returnName() == node_to:
                if not print_stack.isEmpty():
                    self.hierarchy_2 = print_stack.pop() + 2
                if node_from.returnName() == "hub" and self.hierarchy_2 > 9:
                    print_stack.push(self.hierarchy_2-1)
                    packets.append(Packets(node_from, connected_node, self.colour, self.hierarchy_2-1))
                else:
                    print_stack.push(self.hierarchy_2)

                    packets.append(Packets(node_from, connected_node, self.colour, self.hierarchy_2))
                unique_temp_packets = []
                for elem in self.temp_2:
                    if elem not in unique_temp_packets:
                        unique_temp_packets.append(elem)
                for temp_list in unique_temp_packets:
                    print(self.hierarchy, temp_list[2])
                    packets.append(Packets(temp_list[0], temp_list[1], self.colour, temp_list[2]))

            elif connected_node.returnName() in ("switch", "hub"):
                if not any(connected_node.returnName() == node_to for connected_node in self.adjacency_list[node_from]):
                    if not print_stack.isEmpty():
                        self.hierarchy_2 += print_stack.size()
                    self.temp_2.append([node_from, connected_node, self.hierarchy_2])
                    self.targetedSearch(connected_node, node_to)

                #for packet in packets:
            #print(packet.ReturnNodeFrom())
        #print("HELLO")

    def RemovePacket(self, node):
        for packet in list(packets):
            if node in (packet.ReturnNodeFrom(), packet.ReturnNodeTo()):
                packets.remove(packet)

    def CheckIfMovable(self, hierarchy):
        if any(packet.returnHierarchy() == (hierarchy, False) for packet in packets):
            return False
        else:
            return True

    def ControlPackets(self):
        for packet in packets:
            if any(packet.returnHierarchy()[0] == 1 for packet in packets):
                hierarchy, cycle_status = packet.returnHierarchy()
                if not cycle_status:
                    for a in range(0, hierarchy):
                        movable = self.CheckIfMovable(a)
                        if not movable:
                            break
                    if movable:
                        packet.blitToScreen()
                #print(movable)
        if not any(packet.returnHierarchy()[1] == False for packet in packets):
            for packet in packets:
                packet.UpdateCycleStatus()


'''
    def ControlPackets(self):
        for packet in packets:
            #print(packet.returnHierarchy())
            if packet.returnHierarchy() == (1, False):
                packet.blitToScreen()

            #print(pygame.time.get_ticks() - packet.ReturnTimestamp())
                #if 30 > (pygame.time.get_ticks() - packet.ReturnTimestamp()) < 19:
                    #packet.blitToScreen()
                #else:
                    #packet.CalculateTimestamp()
                # completed_paths.append(packet)
                # packets.remove(packet)
            if any(packet.returnHierarchy()[0] == 1 for packet in packets):
                if packet.returnHierarchy() == (2, False):
                    if not any(packet.returnHierarchy() == (1, False) for packet in packets):
                        packet.blitToScreen()

                elif packet.returnHierarchy() == (3, False):
                    if not any(packet.returnHierarchy() == (1, False) for packet in packets) and not any(packet.returnHierarchy() == (2, False) for packet in packets):
                        packet.blitToScreen()

                elif packet.returnHierarchy() == (4, False): #file servers
                    if not any(packet.returnHierarchy() == (1, False) for packet in packets) and not any(packet.returnHierarchy() == (2, False) for packet in packets) and not any(packet.returnHierarchy() == (3, False) for packet in packets):
                        packet.blitToScreen()
                elif packet.returnHierarchy() == (5, False):
                    if not any(packet.returnHierarchy() == (1, False) for packet in packets) and not any(packet.returnHierarchy() == (2, False) for packet in packets) and not any(packet.returnHierarchy() == (3, False) for packet in packets) and not any(packet.returnHierarchy() == (4, False) for packet in packets):
                        packet.blitToScreen()
                elif packet.returnHierarchy() == (6, False):
                    if not any(packet.returnHierarchy() == (1, False) for packet in packets) and not any(packet.returnHierarchy() == (2, False) for packet in packets) and not any(packet.returnHierarchy() == (3, False) for packet in packets) and not any(packet.returnHierarchy() == (4, False) for packet in packets) and not any(packet.returnHierarchy() == (5, False) for packet in packets):
                        packet.blitToScreen()
                elif packet.returnHierarchy() == (7, False):
                    if not any(packet.returnHierarchy() == (1, False) for packet in packets) and not any(packet.returnHierarchy() == (2, False) for packet in packets) and not any(packet.returnHierarchy() == (3, False) for packet in packets) and not any(packet.returnHierarchy() == (4, False) for packet in packets) and not any(packet.returnHierarchy() == (5, False) for packet in packets) and not any(packet.returnHierarchy() == (6, False) for packet in packets):
                        packet.blitToScreen()
                elif packet.returnHierarchy() == (8, False):
                    if not any(packet.returnHierarchy() == (1, False) for packet in packets) and not any(packet.returnHierarchy() == (2, False) for packet in packets) and not any(packet.returnHierarchy() == (3, False) for packet in packets) and not any(packet.returnHierarchy() == (4, False) for packet in packets) and not any(packet.returnHierarchy() == (5, False) for packet in packets) and not any(packet.returnHierarchy() == (6, False) for packet in packets) and not any(packet.returnHierarchy() == (7, False) for packet in packets):
                        packet.blitToScreen()
                elif packet.returnHierarchy() == (9, False):
                    if not any(packet.returnHierarchy() == (1, False) for packet in packets) and not any(packet.returnHierarchy() == (2, False) for packet in packets) and not any(packet.returnHierarchy() == (3, False) for packet in packets) and not any(packet.returnHierarchy() == (4, False) for packet in packets) and not any(packet.returnHierarchy() == (5, False) for packet in packets) and not any(packet.returnHierarchy() == (6, False) for packet in packets) and not any(packet.returnHierarchy() == (7, False) for packet in packets) and not any(packet.returnHierarchy() == (8, False) for packet in packets):
                        packet.blitToScreen()
                elif packet.returnHierarchy() == (10, False):
                    if not any(packet.returnHierarchy() == (1, False) for packet in packets) and not any(packet.returnHierarchy() == (2, False) for packet in packets) and not any(packet.returnHierarchy() == (3, False) for packet in packets) and not any(packet.returnHierarchy() == (4, False) for packet in packets) and not any(packet.returnHierarchy() == (5, False) for packet in packets) and not any(packet.returnHierarchy() == (6, False) for packet in packets) and not any(packet.returnHierarchy() == (7, False) for packet in packets) and not any(packet.returnHierarchy() == (8, False) for packet in packets) and not any(packet.returnHierarchy() == (9, False) for packet in packets):
                        packet.blitToScreen()






        for index, packet in enumerate(packets):
            self.RecursivePacketTiming(index, packet)

            packet.blitToScreen()
            for next_packet in packets[(index+1):]:
                if packet.ReturnNodeFrom().returnName() == next_packet.ReturnNodeFrom().returnName():
                    next_packet.blitToScreen()
                else:
                    next_packet.blitToScreen()


        #self.RecursivePacketTiming(0)
        #index = 0




                #for packet in packets:
                    #packet.UpdateCycleStatus()
                if len(packets) == 1:
                    index = 0
                else:
                    index = 1
                for a in range(index, len(packets)):
                    if packets[index].ReturnNodeFrom().returnName() == packets[a].ReturnNodeFrom().returnName():
                        print("HELLODD")
                        #packets[index+1].blitToScreen()
                        self.RecursivePacketTiming(a)
                        #self.index = a
                    else:
                        self.RecursivePacketTiming(index)
                        self.index = index


            else:
                print(self.index)
                self.RecursivePacketTiming(self.index)

        except IndexError:
            pass
    '''




class Packets:
    def __init__(self, node_from, node_to, colour, hierarchy):
        self.node_from = node_from
        self.node_to = node_to
        self.x, self.y = node_from.returnPosition()
        self.speed = float(speed_slider.ReturnPacketSpeed())
        self.completed_cycle = False
        self.last_move = 0
        self.hierarchy_position = hierarchy
        self.colour = colour
        self.CalculateGradient()
        self.CalculateTimestamp()

    def returnHierarchy(self):
        return self.hierarchy_position, self.completed_cycle

    def CalculateGradient(self):
        self.x1, self.y1 = self.node_from.returnPosition()
        self.x, self.y = self.x1, self.y1
        self.x2, self.y2 = self.node_to.returnPosition()
        self.dx, self.dy = (self.x2 - self.x1, self.y2 - self.y1)
        self.stepx, self.stepy = (self.dx / self.speed, self.dy / self.speed)
        self.CalculateStartPosition()

    def CalculateStartPosition(self):
        self.x += 20
        self.y += 20
        self.x1, self.y1 = self.x, self.y #wrong

    def blitToScreen(self):
        if int(round(self.x)) != self.x2+20 or int(round(self.y)) != self.y2+20:
            self.completed_cycle = False
            pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), 4)
            self.x += self.stepx
            self.y += self.stepy
            #clock.tick(20)
        else:
            self.completed_cycle = True
            self.currently_moving = False
            self.x = self.x1
            self.y = self.y1
        #pygame.display.update()

    def UpdateSpeed(self, speed):
        self.speed = float(speed)
        self.CalculateGradient()

    def UpdateCycleStatus(self):
        self.completed_cycle = False

    def ReturnCycleStatus(self):
        return self.completed_cycle

    def ReturnNodeFrom(self):
        return self.node_from

    def ReturnNodeTo(self):
        return self.node_to

    def CalculateTimestamp(self):
        self.last_move = pygame.time.get_ticks()

    def ReturnTimestamp(self):
        return self.last_move

class TextInputBox(object):
    def __init__(self, x, y, w, h, box_name, box_type, text=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.colour = (0, 0, 0)
        self.font = pygame.font.SysFont('Arial', 15)
        self.text = text
        self.txt_surface = self.font.render(text, True, self.colour)
        self.box_name = self.font.render(box_name, True, self.colour)
        self.active = True
        self.box_type = box_type

    def handle_event(self):
        self.text = ""
        while self.active:
            #clock.tick(FPS)
            event = pygame.event.get()
            for ev in event:
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    # If the user clicked on the input_box rect.
                    if not self.rect.collidepoint(ev.pos):
                        self.active, self.text = False, None
                    # Change the current color of the input box.
                elif ev.type == pygame.KEYDOWN:
                    if self.active:
                        if ev.key == pygame.K_RETURN:
                            self.active = False
                        elif ev.key == pygame.K_BACKSPACE:
                            self.text = self.text[:-1]
                        else:
                            self.text += ev.unicode
                        # Re-render the text.
                        self.txt_surface = self.font.render(self.text, True, self.colour)

            self.update()
            self.draw()
            callBlitToScreen()

            pygame.display.flip()

        self.active = True
        if self.text:
            return self.text
        else:
            return None


    def update(self):
        pass
        # Resize the box if the text is too long.
        width = max(100, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self):
        screen.fill((250, 250, 250))
        if self.box_type == "open":
            view_all = self.font.render("'all' to view all networks", True, (0, 0, 0))
            delete_net = self.font.render("'delete <network name>' to delete", True, (0, 0, 0))
            screen.blit(view_all, (1150, 140))
            screen.blit(delete_net, (1150, 155))
        screen.blit(self.box_name, (self.rect.x, self.rect.y-30))
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.colour, self.rect, 2)

class DisplayAllNetworks(TextInputBox):
    def __init__(self, text):
        self.files = text
        super(DisplayAllNetworks, self).__init__(1150, 200, 60, 32, None, None)

    def draw(self):
        y = 60
        screen.fill((250, 250, 250))
        for file in self.files:
            text = ''.join(str(e) for e in file)
            files_surface = self.font.render(text, True, self.colour)
            screen.blit(files_surface, (self.rect.x, y))
            y += 20
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.colour, self.rect, 2)



class SaveAndLoadButtons:
    def __init__(self, image, name, x, y):
        self.image = pygame.image.load(image)
        self.name = name
        self.rect = pygame.Rect(x, y, 20, 20)
        self.database = Database.Network_Database()
        self.x = x
        self.y = y
        self.font = pygame.font.SysFont('Ariel', 20)

    def CheckForSelection(self, event):
        #mouse_x, mouse_y = pygame.mouse.get_pos()
        for ev in event:
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if self.rect.collidepoint(ev.pos):
                    if self.name == "open" or NodeAdjacencyList.ReturnDict():  # Check canvas isn't empty
                        self.GetNetworkName()
                        if self.name == "save":
                            self.ExportNetwork()
                        else:
                            self.RetrieveData()

    def BlitToScreen(self):
        screen.blit(self.image, (self.x, self.y))

    def ExportNetwork(self):
        if not self.network_name:
            self.text = self.font.render("Network not saved", True, (0,0,0))
        else:
            self.text = self.font.render(self.network_name+ " saved", True, (0,0,0))
            self.database_file = self.network_name + ".pkl"

            self.node_positions = []
            adj_list = NodeAdjacencyList.ReturnDict()
            for key, value in adj_list.items():
                for v in value:
                    application_running, server_properties = None, None
                    if key.returnName() == "pc":
                        application_running = key.ReturnRunningApplications()
                    if v.returnName() in ("file server", "print server", "e-mail server", "multimedia server", "web cache"):
                        v = Server
                        server_properties = v.ReturnProperties()
                    self.node_positions.append([key.returnName(), key.returnPosition(), v.returnName(), v.returnPosition(), application_running, server_properties])

            with open(self.database_file, "wb") as file:
                pickle.dump(self.node_positions, file)
                file.close()
            self.SaveToDatabase()

        pygame.draw.rect(screen, (250,250,250), (1150, 60, 150, 100))
        screen.blit(self.text, (1170,70))
        pygame.display.flip()
        time.sleep(2)

    def GetNetworkName(self):
        text = "Enter network name:"
        self.input_box = TextInputBox(1150, 100, 60, 32, text, self.name)
        self.network_name = self.input_box.handle_event()

    def SaveToDatabase(self):
        self.database.insert_data(self.network_name, self.database_file)

    def RetrieveData(self):
        if self.network_name:
            display_text = False
            if self.network_name.lower() == "all":
                self.DisplayAll()
            elif "delete" in self.network_name.lower():
                self.deleted = False
                self.DeleteNetwork()
                if self.deleted:
                    self.text = self.font.render(self.network_name+ " deleted", True, (0,0,0))
                else:
                    self.text = self.font.render(self.network_name+ " does not exist", True, (0,0,0))
                display_text = True

            else:
                self.file_location = self.database.retrieve_network(self.network_name)
                file_exists = self.FormatNetworkLocation()
                if not file_exists:
                    self.text = self.font.render(self.network_name + " does not exist", True, (0, 0, 0))
                else:
                    self.text = self.font.render(self.network_name + " opened", True, (0, 0, 0))
                display_text = True
            if display_text:
                pygame.draw.rect(screen, (250, 250, 250), (1100, 60, 245, 110))
                screen.blit(self.text, (1180, 70))
                pygame.display.flip()
                time.sleep(2)

    def DisplayAll(self):
        files = self.database.display_all()
        display_networks = DisplayAllNetworks(files)
        self.network_name = display_networks.handle_event()
        self.RetrieveData()

    def FormatNetworkLocation(self):
        for file_location in self.file_location:
            for f in file_location:
                open_network = ImportNetwork(f)
        try:
            open_network.import_network()
            return True
        except UnboundLocalError: # if no networks
            return False

    def DeleteNetwork(self):
        self.network_name = self.network_name.replace('delete ', '')
        self.deleted = self.database.delete_network(self.network_name)

class ImportNetwork:
    def __init__(self, file_location):
        self.file_location = file_location

    def import_network(self):
        with open(self.file_location, "rb") as file:
            self.node_positions = pickle.load(file)
        self.position_nodes()
        self.sort_adjacency_list()

    def position_nodes(self):
        used_nodes = []
        for node_pos in self.node_positions:
            for node in nodes:
                unique = True
                if node.returnName() == node_pos[0]:
                    for used_node in used_nodes:
                        if node_pos[1] == used_node[1]:
                            node_pos[0] = used_node[0]
                            node.UpdatePosition((node_pos[1]))
                            unique = False
                        if node == used_node[0]:
                            unique = False
                    if unique:
                        used_nodes.append([node, node_pos[1]])
                        if node_pos[0] == "pc":
                            node.UpdateApplications(node_pos[4])
                        node_pos[0] = node
                        node.UpdatePosition((node_pos[1]))

                elif node.returnName() == node_pos[2]:
                    for used_node in used_nodes:
                        if node_pos[3] == used_node[1]:
                            node_pos[2] = used_node[0]
                            node.UpdatePosition((node_pos[3]))
                            unique = False
                        if node == used_node[0]:
                            unique = False
                    if unique:
                        used_nodes.append([node,node_pos[3]])
                        if node_pos[2] == "server":
                            Server.UpdateProperties(node_pos[5])
                            Server.UpdatePosition((node_pos[3]))
                            Server.DisplayDrives()
                            Server.BlitServer()
                        node_pos[2] = node
                        node.UpdatePosition((node_pos[3]))

    def sort_adjacency_list(self):
        print(self.node_positions)
        for node_pos in self.node_positions:
            if node_pos[5]:
                for drive in node_pos[5]:
                    for server in Server_drives:
                        if server.returnName() == drive.lower():
                            NodeAdjacencyList.AddToDict(node_pos[0], server)
            else:
                NodeAdjacencyList.AddToDict(node_pos[0], node_pos[2])

class PrinterStack:
    def __init__(self):
        self.print_queue = []

    def isEmpty(self):
        return self.size() == 0

    def push(self, item):
        self.print_queue.append(item)

    def pop(self):
        return self.print_queue.pop()

    def highest_item(self):
        return max(xrange(len(self.print_queue)), key = lambda x: self.print_queue[x])

    def size(self):
        return len(self.print_queue)

class PacketSpeed:
    def __init__(self):
        self.x = 1065
        self.packet_speed = 30
        self.pressed = False
        self.font = pygame.font.SysFont('Ariel', 22)
        self.text = self.font.render("Packet flow speed:", True, (0, 0, 0))

    def Slider(self):
        if pygame.mouse.get_pressed()[0] != 0:
            for ev in pygame.event.get():
                if self.circle.collidepoint(ev.pos) or self.pressed:
                    self.pressed = True
                    self.x = pygame.mouse.get_pos()[0]
                    if self.x < 1000:
                        self.x = 1000
                    elif self.x > 1130:
                        self.x = 1130
                    self.packet_speed = (130 - (self.x - 900)/2)
                    print(self.packet_speed)
                    screen.fill((250, 250, 250))
                    callBlitToScreen()
                    self.BlitToScreen()
                    for packet in packets:
                        packet.UpdateSpeed(self.packet_speed)

        else:
            self.pressed = False
        self.BlitToScreen()

    def BlitToScreen(self):
        screen.blit(self.text, (1000, 20))
        pygame.draw.rect(screen, (255,69,0), (1000, 50, 130, 10))
        self.circle = pygame.draw.circle(screen, (0,0,0), (self.x, 55), 8)
        pygame.display.update()

    def ReturnPacketSpeed(self):
        return self.packet_speed

def checkForMouseDown():
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for node in nodes:
                if node.hoveringOver():
                    return True, node

            return True, None

    return False, None

def DisplaySideBar():
    bar_colour = (0, 0, 0)
    pygame.draw.line(screen, bar_colour, (85, 0), (85, 380), 5)
    pygame.draw.line(screen, bar_colour, (0, 378), (85, 378), 5)

def callBlitToScreen():
    if Server.returnActivated():
        Server.RemoveReduntantCables()
    if NodeAdjacencyList.Activated:
        NodeAdjacencyList.DisplayCables()
    for node in nodes[5:]:  # not server drives
        node.blitToScreen()
    if Server.returnActivated():  # must be separate to similar statement above so that the servers are above the cables
        Server.BlitServer()
        Server.CheckForMovementOrSelection()
    if PacketPath.returnActivated():
        PacketPath.ControlPackets()
    DisplaySideBar()
    SaveButton.BlitToScreen()
    OpenButton.BlitToScreen()
    speed_slider.Slider()
    pygame.display.flip()


speed_slider = PacketSpeed()
print_stack = PrinterStack()
PacketPath = CreatePacketPath()
SaveButton = SaveAndLoadButtons("save_button.png", "save", 1200, 20)
OpenButton = SaveAndLoadButtons("open_button.png", "open", 1250, 20)

NUMBER_PCS = 15
NUMBER_ROUTERS = 5
NUMBER_SWITCHES = 5
NUMBER_HUBS = 5
NUMBER_PRINTERS = 5
# NUMBER_CONNECTABLE_SERVERS = 5

PCs = [PC() for x in range(NUMBER_PCS)]
Routers = [Router() for x in range(NUMBER_ROUTERS)]
Switches = [Switch() for x in range(NUMBER_SWITCHES)]
Hubs = [Hub() for x in range(NUMBER_HUBS)]
Printers = [Printer() for x in range(NUMBER_PRINTERS)]
Server = Server()
Cable = Cable()

File_server = Node((-100, -100), "server_drive.png", None, "File server", x, None, None, ["switch", "hub"])
Print_server = Node((-100, -100), "server_drive.png", None, "Print server", x, None, None, ["switch", "hub"])
Email_server = Node((-100, -100), "server_drive.png", None, "E-mail server", x, None, None, ["switch", "hub"])
Multimedia_server = Node((-100, -100), "server_drive.png", None, "Multimedia server", x, None, None, ["switch", "hub"])
Web_Cache_server = Node((-100, -100), "server_drive.png", None, "Web cache", x, None, None, ["switch", "hub"])

Server_drives = []
Server_drives.append(File_server)
Server_drives.append(Print_server)
Server_drives.append(Email_server)
Server_drives.append(Multimedia_server)
Server_drives.append(Web_Cache_server)
##CHANGE THIS TO SINGLE ONES -- IE TO DETECT WHICH ONE IS WHICH FOR PATH FINDING, -100 because otherwise clickable

nodes = []
packets = []
# combine all nodes into one list for easy iteration
nodes.extend(Server_drives)
nodes.append(Server)
nodes.append(Cable)
nodes.extend(PCs)
nodes.extend(Routers)
nodes.extend(Switches)
nodes.extend(Hubs)
nodes.extend(Printers)

NodeAdjacencyList = AdjacencyList()


def runProgram():
    screen.fill((250,250,250))
    callBlitToScreen()
    for node in nodes:
        event = pygame.event.get()
        SaveButton.CheckForSelection(event)
        OpenButton.CheckForSelection(event)
        touching = node.hoveringOver()
        while touching:
            touching = node.hoveringOver()
            screen.fill((250, 250, 250))
            callBlitToScreen()
            if node.returnName() == "cable":
                node.ConnectCableToNodes()
            elif node.returnName() == "server":
                if not node.returnActivated():
                    node.CreateServer()
            else:
                node.dragDrop(node)
                '''
                if node.returnActivated():
                    node.SelectNode()
                '''

    pygame.display.flip()


done = False

while not done:
    ev = pygame.event.get()
    for event in ev:
        if event.type == pygame.QUIT:
            done = True
    runProgram()