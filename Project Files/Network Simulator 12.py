import pygame, random, os

pygame.init()
pygame.display.set_caption("Network Simulator")
pygame.font.init()
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

    def UpdatePosition(self, x, y):
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

                pygame.draw.line(screen, (230, 30, 30), (90, 0), (90, 720), 6)
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

                                # print(self.Properties)
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


    def ReturnProperties(self):
        return self.Properties

class PC(Node):
    def __init__(self):
        self.text1 = "Applications running:\n Word processing\n Internet browsing\n Multimedia\n E-mailing\n Online intranet\n"
        self.CompatibleNodes = ["pc", "router", "switch", "hub", "printer"]
        super(PC, self).__init__((10, 15), "pc.png", "pc_selected.png", "PC", 1, True, self.text1, self.CompatibleNodes)
        # self.RunningApplications = None
        self.PropertyConnections = [{"Word processing": ["printer", "print server", "file server"]}, {"Internet browsing": ["router", "web cache"]},
                                    {"Multimedia": "FILESERVER"}]

    def FindPath(self):
        pass

    def SetHierachy(self):
        if self.RunningApplications == "Internet browsing":
            self.Hierachy = "router"
            # check teach-ict to see options

    def ReturnRunningApplications(self):
        return self.RunningApplications

    def CalculateNodeConnections(self):
        # refresh packets everytime change property
        for property in self.Properties:
            if property == "Word processing":
                return ["printer", "print server", "file server"]
            elif property == "Internet browsing":
                return ["router", "web cache"]
            elif property == "Multimedia":
                return ["multimedia server"]
            elif property == "E-mail":
                return ["e-mail server"]
            else: #intranet
                return ["file server"]

class Router(Node):
    def __init__(self):
        self.text1 = "Applications running:\n None"
        self.CompatibleNodes = ["pc", "switch", "hub", "printer"]
        super(Router, self).__init__((10, 60), "router.png", "router_selected.png", "Router", 1, True, self.text1,
                                     self.CompatibleNodes)


class Switch(Node):
    def __init__(self):
        self.text1 = "Applications running:\n None"
        self.CompatibleNodes = ["pc", "router", "switch", "printer", "file server", "print server",
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
        self.CompatibleNodes = ["pc", "router", "switch", "hub"]
        super(Printer, self).__init__((10, 215), "printer.png", "printer_selected.png", "Printer", 1, True, self.text1,
                                      self.CompatibleNodes)


class Server(Node):
    def __init__(self):
        self.text1 = "Server functions:\n File server\n Print server\n E-mail server\n Multimedia server\n Web cache"
        self.CompatibleNodes = ["switch", "hub"]
        self.drive_image = pygame.image.load("server_drive.png")
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
                    self.CheckForMovementOrSelection()

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
                File_server.UpdatePosition(self.server_x + 10, self.server_y + 20)
                Server_drives[0].blitToScreen()

            elif drive == "Print server":
                node_name_text = text.render("Print server", True, (0, 0, 0))
                screen.blit(node_name_text, (self.server_x + 11, self.server_y + 125))
                Print_server.UpdatePosition(self.server_x + 10, self.server_y + 85)
                Print_server.blitToScreen()

            elif drive == "E-mail server":
                node_name_text = text.render("E-mail server", True, (0, 0, 0))
                screen.blit(node_name_text, (self.server_x + 8, self.server_y + 190))
                Email_server.UpdatePosition(self.server_x + 10, self.server_y + 150)
                Email_server.blitToScreen()

            elif drive == "Multimedia server":
                node_name_text = text.render("Media server", True, (0, 0, 0))
                screen.blit(node_name_text, (self.server_x + 8, self.server_y + 255))
                Multimedia_server.UpdatePosition(self.server_x + 10, self.server_y + 215)
                Multimedia_server.blitToScreen()

            elif drive == "Web cache":
                node_name_text = text.render("Web cache", True, (0, 0, 0))
                screen.blit(node_name_text, (self.server_x + 13, self.server_y + 320))
                Web_Cache_server.UpdatePosition(self.server_x + 10, self.server_y + 280)
                Web_Cache_server.blitToScreen()

    def RemoveReduntantCables(self):
        adj_activated = NodeAdjacencyList.ReturnState()  # Removing reduntant cables after deselection of servers
        if adj_activated:
            for drive in Server_drives:
                drive_name = drive.returnName()
                drive_name = drive_name[0].upper() + drive_name[1:]
                if drive_name not in self.Properties:
                    NodeAdjacencyList.RemoveFromDict(drive)

        '''
        for drive_index, drive in enumerate(self.Properties):
            for drive_object in self.drives:
                print(drive, drive_object.returnName())
                if drive_object.returnName() == drive.lower():
                    y = 30 + ((len(self.Properties)-1) - drive_index) * 50
                    drive_object.UpdatePosition(self.server_x + 10, self.server_y + y)
                    drive_object.blitToScreen()


        for drive_index, drive in enumerate(self.Properties):
            print(self.drives[drive_index].returnNumber(), drive_index)
            y = (len(self.Properties) - self.drives[drive_index].returnNumber()) * 100
            self.drives[drive_index].UpdatePosition(self.server_x + 10, self.server_y + y)
            self.drives[drive_index].blitToScreen()
            #text = text.render(drive, True, (0,0,0))
            #self.surface.blit(text, (10, 60))
        '''


        # self.drives[drive_index].returnPosition()

    def BlitServer(self):
        pygame.draw.rect(screen, (0, 0, 0), (self.server_x, self.server_y, 100, 350), 7)
        screen.blit(self.surface, (self.server_x, self.server_y))
        self.DisplayDrives()
        # pygame.display.flip()

    def CheckForMovementOrSelection(self):
        done = False
        x, y = pygame.mouse.get_pos()
        if self.server_x <= x <= self.server_x + 100:
            if self.server_y <= y <= self.server_y + 15:
                clock.tick(FPS)
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
                NodeAdjacencyList.AddToDict(node_from, node_to, x1, y1)
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

    def AddToDict(self, NodeFrom, NodeTo, x1, y1):
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
        self.visited = []
        self.connections = []
        self.activated = False
        self.index = 0
        self.pc_complete = False
        self.temp_packets = []

    def returnActivated(self):
        return self.activated

    def CreatePackets(self):
        self.activated = True
        del packets[0:]
        self.adjacency_list = NodeAdjacencyList.ReturnDict()

        '''
        for node_from in list(adjacency_list):
            if node_from.returnName() == "pc":
                for node_to in adjacency_list[node_from]:
                    packets.append(Packets(node_from, node_to))
                    if node_to in adjacency_list:
                        for nodes in adjacency_list[node_to]:
                            print(nodes)
                            packets.append(Packets(node_to, nodes))
        '''
        for node_from in self.adjacency_list:
            if node_from.returnName() == "pc":
                for node_to in self.adjacency_list[node_from]:
                    self.RecursiveDepthSearch(node_from, node_to)


    def RecursiveDepthSearch(self, node_from, node_to): # this is used to find the path to take between all the nodes
        for node_to in self.adjacency_list[node_from]:
            if node_from.returnName() == "pc":
                self.connections.append(node_from.CalculateNodeConnections())
                try:
                    if node_to.returnName() in self.connections:
                        packets.append(Packets(node_from, node_to))
                    elif node_to.returnName() in ("switch", "hub"):
                        if self.temp_packets:
                            for temp_packet_list in self.temp_packets:
                                if node_to not in temp_packet_list:
                                    self.temp_packets.append([node_from, node_to])
                        else:
                            self.temp_packets.append([node_from, node_to])

                except TypeError:
                    pass

            elif node_to.returnName() in self.connections:
                packets.append(Packets(node_from, node_to))

            if node_to in self.adjacency_list:
                self.RecursiveDepthSearch(node_to, self.adjacency_list[node_to])

        try:
            for temp_packet_list in self.temp_packets:
                for packet in packets:
                    if packet.ReturnNodeTo().returnName() in self.connections: # error here?? Nearly complete algorithm
                        packets.append(Packets(temp_packet_list[0], temp_packet_list[1]))

        except TypeError:
            pass

        #for packet in packets:
            #print(packet.ReturnNodeFrom())
        #print("HELLO")

    def RemovePacket(self, node):
        for packet in list(packets):
            if node in (packet.ReturnNodeFrom(), packet.ReturnNodeTo()):
                packets.remove(packet)

    def ControlPackets(self):
        for packet in packets:
            # print(packet.returnHierarchy())
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

            if not any(packet.returnHierarchy()[1] == False for packet in packets):
                for packet in packets:
                    packet.UpdateCycleStatus()



    '''
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
    def __init__(self, node_from, node_to):
        self.node_from = node_from
        self.node_to = node_to
        self.x, self.y = node_from.returnPosition()
        self.completed_cycle = False
        self.last_move = 0
        self.CalculateGradient()
        self.CalculateHierarchy()
        self.CalculateTimestamp()

    def CalculateHierarchy(self):
        if self.node_from.returnName() == "pc":
            self.hierarchy_position = 1
        elif self.node_from.returnName() == "hub":
            self.hierarchy_position = 2
        elif self.node_from.returnName() == "switch":
            self.hierarchy_position = 3
        else:
            self.hierarchy_position = 4

    def returnHierarchy(self):
        return self.hierarchy_position, self.completed_cycle

    def CalculateGradient(self):
        self.x1, self.y1 = self.node_from.returnPosition()
        self.x, self.y = self.x1, self.y1
        self.x2, self.y2 = self.node_to.returnPosition()
        self.dx, self.dy = (self.x2 - self.x1, self.y2 - self.y1)
        self.stepx, self.stepy = (self.dx / 15., self.dy / 15.)
        self.CalculateStartPosition()

    def CalculateStartPosition(self):
        self.x += 2 * self.stepx
        self.y += 2 * self.stepy
        self.x1, self.y1 = self.x, self.y #wrong

    def blitToScreen(self):
        if int(round(self.x)) != self.x2 or int(round(self.y)) != self.y2:
            self.completed_cycle = False
            pygame.draw.circle(screen, (0, 0, 255), (int(self.x), int(self.y)), 4)
            self.x += self.stepx
            self.y += self.stepy
            #clock.tick(20)
        else:
            self.completed_cycle = True
            self.currently_moving = False
            self.x = self.x1
            self.y = self.y1
        #pygame.display.update()

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


def checkForMouseDown():
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for node in nodes:
                if node.hoveringOver():
                    return True, node

            return True, None

    return False, None


def callBlitToScreen():
    if Server.returnActivated():
        Server.RemoveReduntantCables()
    if NodeAdjacencyList.Activated:
        NodeAdjacencyList.DisplayCables()
    for node in nodes[5:]:  # not server drives
        node.blitToScreen()
    if Server.returnActivated():  # must be separate to similar statement above so that the servers are above the cables
        Server.BlitServer()
    if PacketPath.returnActivated():
        PacketPath.ControlPackets()
    pygame.display.flip()



PacketPath = CreatePacketPath()

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
    pygame.draw.line(screen, (230, 30, 30), (90, 0), (90, 720), 6)
    for node in nodes:
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
        if Server.returnActivated():
            Server.CheckForMovementOrSelection()

    pygame.display.flip()


done = False

while not done:
    ev = pygame.event.get()
    for event in ev:
        if event.type == pygame.QUIT:
            done = True
    runProgram()