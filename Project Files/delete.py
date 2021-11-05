import pygame, random, os, pickle, Database, time
pygame.init()
pygame.display.set_caption("Network Simulator")
pygame.font.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 25)
clock = pygame.time.Clock()

FPS = 60
screenInfo = pygame.display.Info()
screen = pygame.display.set_mode((screenInfo.current_w, screenInfo.current_h - 64))
screen.fill((250, 250, 250))

packet_colours = [(255,0,0), (0,0,255), (255,0,255), (128,128,0), (255,69,0), (0,100,0), (139,69,19), (105,105,105)] # must be at top of program otherwise AttributeError

class Node(object):  # 'object' because it is parent class
    def __init__(self, (x, y), image, name, movable, text, compatible_nodes):
        self.name = str(name)
        self.x = x
        self.y = y
        self.default_x = x
        self.default_y = y
        self.image = pygame.image.load(image)
        self.default_image = pygame.image.load(image)
        self.text = text
        self.touching = False
        self.mouse_down = False
        self.clicked = False
        self.activated = False
        self.compatible_nodes = compatible_nodes
        self.current = False
        self.properties = []
        self.properties_window_activated = False
        self.movable = movable

    def updatePosition(self, (x, y)): # update position of node
        self.x = x
        self.y = y

    def returnSize(self): # return size of node icon
        return self.image.get_rect().size

    def returnActivated(self): # return if in use or not
        return self.activated

    def returnName(self): # return name of node (i.e. PC, printer, etc.)
        return self.name.lower()

    def returnPosition(self): # return position of node
        return self.x, self.y

    def returnStatus(self): # return whether currently selected
        return self.current

    def returnCompatibleNodes(self): # return nodes can connect to
        return self.compatible_nodes

    def blitToScreen(self): # draw onto screen
        screen.blit(self.image, (self.x, self.y))

    def hoveringOver(self): # check if hovering over node
        pygame.event.get()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if (mouse_x >= self.x) and (mouse_x <= self.x + 40):
            if (mouse_y > self.y) and (mouse_y < self.y + 40):
                self.touching = True
                return True

    def dragDrop(self, node): # drag and drop GUI function
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
                            if self.properties_window_activated:
                                self.selectProperty()
                            else:
                                self.createPropertiesWindow()
                    else:
                        screen.fill((250, 250, 250))
                        self.activated = True
                        if self.x < 100:  # to delete node
                            self.x, self.y = self.default_x, self.default_y
                            self.activated = False
                            adj_activated = NodeAdjacencyList.returnState()
                            if adj_activated:
                                NodeAdjacencyList.removeFromDict(node)
                                PacketPath.createPackets()
                                # old_x, old_y = self.x, self.y
                        elif PacketPath.returnActivated():
                            for packet in packets:
                                packet.calculateGradient()

                elif self.mouse_down and self.movable:
                    mouse_x, mouse_y = (pygame.mouse.get_pos())
                    self.x, self.y = mouse_x + offset_x, mouse_y + offset_y
                    screen.fill((250, 250, 250))

                callBlitToScreen()

    def createPropertiesWindow(self): # create window for selection of running apps. and to display node name and icon
        self.current = True
        self.checkbox_coordinates = []
        self.properties_window_activated = True
        x = 50
        y = 90
        callBlitToScreen()
        self.window_surface = pygame.Surface((400, 500))
        self.window_surface.fill((255, 255, 255))
        pygame.draw.rect(screen, (0, 0, 0), (500, 50, 400, 500), 8)
        text = pygame.font.SysFont('Comic Sans MS', 25)
        node_name_text = text.render(self.name, True, (0, 0, 0))
        text = pygame.font.SysFont('Comic Sans MS', 20)
        words = [word.split(' ') for word in self.text.splitlines()]  # 2D array where each row is a list of words.

        for line in words:  # pygame can't render line breaks
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
        self.selectProperty()

    def selectProperty(self): # get selection of running apps. checkbox
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

                                if selection in self.properties:

                                    self.properties.remove(selection)
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
                                    self.properties.append(selection)
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

        PacketPath.createPackets()

class PC(Node):
    def __init__(self):
        self.text1 = "Applications running:\n Word processing\n Internet browsing\n Multimedia\n E-mailing\n"
        self.CompatibleNodes = ["router", "switch", "hub", "printer"]
        super(PC, self).__init__((25, 15), "pc.png", "PC", True, self.text1, self.CompatibleNodes)
        try:
            self.colour = random.choice(packet_colours)
            packet_colours.remove(self.colour)  # so same colour is not used
        except IndexError:  # if not enough colours to choose from
            self.colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def returnRunningApplications(self):
        return self.properties

    def updateApplications(self, property):
        self.properties = property

    def calculateNodeConnections(self, property):   # return nodes packets should flow to based on running apps.
        if property == "Word processing":
            return ["printer", "print server", "file server"]
        elif property == "Internet browsing":
            return ["router", "web cache"]
        elif property == "Multimedia":
            return ["multimedia server"]
        elif property == "E-mailing":
            return ["e-mail server"]

    def returnColour(self): # return colour of the PC packets
        return self.colour

class Router(Node):
    def __init__(self):
        self.text1 = "Applications running:\n None"
        self.CompatibleNodes = ["pc", "switch", "hub"]
        super(Router, self).__init__((20, 60), "router.png", "Router", True, self.text1,
                                     self.CompatibleNodes)


class Switch(Node):
    def __init__(self):
        self.text1 = "Applications running:\n None"
        self.CompatibleNodes = ["pc", "switch", "router", "printer", "file server", "print server",
                                "e-mail server", "multimedia server", "web cache"]
        super(Switch, self).__init__((5, 120), "switch.png", "Switch", True, self.text1, self.CompatibleNodes)


class Hub(Node):
    def __init__(self):
        self.text1 = "Applications running:\n None"
        self.CompatibleNodes = ["pc", "router", "switch", "hub", "printer", "file server", "print server",
                                "e-mail server", "multimedia server", "web cache"]
        super(Hub, self).__init__((25, 170), "hub.png", "Hub", True, self.text1,
                                  self.CompatibleNodes)


class Printer(Node):
    def __init__(self):
        self.text1 = "Applications running:\n None"
        self.CompatibleNodes = ["pc", "switch", "hub"]
        super(Printer, self).__init__((25, 215), "printer.png", "Printer", True, self.text1,
                                      self.CompatibleNodes)


class Server(Node):
    def __init__(self):
        self.text1 = "Server functions:\n File server\n Print server\n E-mail server\n Multimedia server\n Web cache"
        self.CompatibleNodes = ["switch", "hub"]
        self.drive_image = pygame.image.load("server_drive.png")
        self.selected_image = pygame.image.load("server_selected.png")
        self.imported = False
        super(Server, self).__init__((28, 265), "server.png", "Server", False, self.text1,
                                     self.CompatibleNodes)

    def createServer(self): # create server selection box
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
                    self.createPropertiesWindow()
                    self.image = self.default_image
                    self.blitToScreen()
                    pygame.display.flip()

    def displayDrives(self): # calculate which server drives to show and where
        text = pygame.font.SysFont('Comic Sans MS', 13)
        self.surface.fill((255, 255, 255))
        self.move_surface = pygame.Surface((100, 15))
        self.move_surface.fill((80, 80, 80))
        self.surface.blit(self.move_surface, (0, 0))

        for drive in self.properties:
            if drive == "File server":
                node_name_text = text.render("File server", True, (0, 0, 0))
                screen.blit(node_name_text, (self.server_x + 13, self.server_y + 60))
                File_server.updatePosition((self.server_x + 10, self.server_y + 20))
                Server_drives[0].blitToScreen()

            elif drive == "Print server":
                node_name_text = text.render("Print server", True, (0, 0, 0))
                screen.blit(node_name_text, (self.server_x + 11, self.server_y + 125))
                Print_server.updatePosition((self.server_x + 10, self.server_y + 85))
                Print_server.blitToScreen()

            elif drive == "E-mail server":
                node_name_text = text.render("E-mail server", True, (0, 0, 0))
                screen.blit(node_name_text, (self.server_x + 8, self.server_y + 190))
                Email_server.updatePosition((self.server_x + 10, self.server_y + 150))
                Email_server.blitToScreen()

            elif drive == "Multimedia server":
                node_name_text = text.render("Media server", True, (0, 0, 0))
                screen.blit(node_name_text, (self.server_x + 8, self.server_y + 255))
                Multimedia_server.updatePosition((self.server_x + 10, self.server_y + 215))
                Multimedia_server.blitToScreen()

            elif drive == "Web cache":
                node_name_text = text.render("Web cache", True, (0, 0, 0))
                screen.blit(node_name_text, (self.server_x + 13, self.server_y + 320))
                Web_Cache_server.updatePosition((self.server_x + 10, self.server_y + 280))
                Web_Cache_server.blitToScreen()

    def removeReduntantCables(self): # remove cables if drive is removed
        adj_activated = NodeAdjacencyList.returnState()  # Removing reduntant cables after deselection of servers
        if adj_activated:
            for drive in Server_drives:
                drive_name = drive.returnName()
                drive_name = drive_name[0].upper() + drive_name[1:]
                if drive_name not in self.properties:
                    NodeAdjacencyList.removeFromDict(drive)


    def blitServer(self): # display server icon to screen
        pygame.draw.rect(screen, (0, 0, 0), (self.server_x, self.server_y, 100, 350), 7)
        screen.blit(self.surface, (self.server_x, self.server_y))
        self.displayDrives()
        # pygame.display.flip()

    def returnProperties(self): # return which drives are in use
        return self.properties

    def updateProperties(self, properties): # update drives in use (when importing network)
        self.properties = properties

    def returnPosition(self): # return position of RAID server
        return self.server_x, self.server_y

    def updatePosition(self, (x, y)): # update position (when importing network)
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


    def checkForMovementOrSelection(self): # check for selection of top fill bar
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
                                            self.createPropertiesWindow()
                                            self.imported = False
                                        self.selectProperty()
                                        self.displayDrives()

                                    elif self.server_x < 100:
                                        self.activated = False
                                        screen.fill((250, 250, 250))
                                        callBlitToScreen()

                                    elif PacketPath.returnActivated():
                                        for packet in packets:
                                            packet.calculateGradient()

                                else:
                                    x, y = pygame.mouse.get_pos()
                                    self.server_x, self.server_y = x + offset_x, y + offset_y
                                    screen.fill((250, 250, 250))
                                    callBlitToScreen()


class Cable(Node):
    def __init__(self):
        super(Cable, self).__init__((23, 318), "cable.png", "Cable", False, None, None)
        self.selected_image = pygame.image.load("cable_selected.png")

    def connectCableToNodes(self): # simulation of connecting cables
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
                mouse_down, node_from = self.checkForMouseDown()
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
                mouse_down, node_to = self.checkForMouseDown()
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
                NodeAdjacencyList.addToDict(node_from, node_to)
                callBlitToScreen()

            else:
                done = True
                self.image = pygame.image.load("cable.png")

    def checkForMouseDown(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for node in nodes:
                    if node.hoveringOver():
                        return True, node

                return True, None

        return False, None


class AdjacencyList(object):
    def __init__(self):
        self.node_connections = {}  # must use dictionary. Dont use list of dicts!
        self.activated = False

    def addToDict(self, node_from, node_to): # add route to dict
        self.activated = True
        if node_from.returnName() == "pc":
            if node_from in self.node_connections:
                self.node_connections[node_from].append(node_to)
            else:
                self.node_connections[node_from] = [node_to]
        elif node_to.returnName() == "pc":
            if node_to in self.node_connections:
                self.node_connections[node_to].append(node_from)
            else:
                self.node_connections[node_to] = [node_from]

        elif node_from.returnName() in ("switch", "hub"):
            if node_from in self.node_connections:
                self.node_connections[node_from].append(node_to)
            else:
                self.node_connections[node_from] = [node_to]
        else:
            if node_to in self.node_connections:
                self.node_connections[node_to].append(node_from)
            else:
                self.node_connections[node_to] = [node_from]

        PacketPath.createPackets()

    def removeFromDict(self, Node): # remove route
        for key in self.node_connections.keys():
            if key == Node:
                del self.node_connections[key]

        for k, v in self.node_connections.items():  # k = key, v = values
            self.node_connections[k] = filter(lambda x: x != Node, v)

        for k, v in self.node_connections.items():  # checks for value empty
            if not v:
                del self.node_connections[k]

    def returnDict(self): # return adjacency matrix
        return self.node_connections

    def returnState(self): # return if matrix is empty or not
        return self.activated

    def displayCables(self): # display cables between nodes
        keys = self.node_connections.keys()
        for key in keys:
            for value in self.node_connections[key]:
                x1, y1 = value.returnPosition()
                x, y = key.returnPosition()
                pygame.draw.aaline(screen, (0, 0, 255), (x1 + 20, y1 + 20), (x + 20, y + 20), 2)


class CreatePacketPath:
    def __init__(self):
        self.connections = []
        self.activated = False
        self.index = 0
        self.pc_complete = False
        self.print_cycle_complete = True
        self.print_queue = []

    def returnActivated(self): # return if any packets are flowing
        return self.activated

    def createPackets(self): # instantiate temporary variables and prepare for creation of packets
        self.route_number = 0
        self.activated = True
        self.temp_packets = []
        del packets[0:]
        print_queue.emptyQueue()
        self.adjacency_list = NodeAdjacencyList.returnDict()
        for node_from in self.adjacency_list:
            if node_from.returnName() == "pc":
                self.visited = []
                if node_from.returnRunningApplications():
                    self.recursiveBreadthSearch(node_from)


    def recursiveBreadthSearch(self, node_from): # finds the path packets should take over network
        self.visited.append(node_from)
        temp_nodes = []
        for node_to in self.adjacency_list[node_from]:
            if node_from.returnName() == "pc":
                self.colour = node_from.returnColour()
                self.root_node = node_from
                self.route_number += 1
                properties = node_from.returnRunningApplications()
                self.connections = []
                for property in properties:
                    self.connections.extend(node_from.calculateNodeConnections(property))

                if node_to.returnName() in self.connections:
                    packets.append(Packets(node_from, node_to, self.colour, 1))
                elif node_to.returnName() in ("switch", "hub"):
                    self.temp_packets.append([self.route_number, node_from, node_to, 1])

            elif node_to.returnName() in self.connections:
                unique_temp_packets = []
                for elem in self.temp_packets: # remove duplicates from temp list
                    if elem not in unique_temp_packets:
                        unique_temp_packets.append(elem)
                for temp_list in unique_temp_packets:
                    if temp_list[0] == self.route_number: # if bridging device from same route
                        packets.append(Packets(temp_list[1], temp_list[2], self.colour, temp_list[3]))
                if node_to.returnName() in ("file server", "print server", "e-mail server", "multimedia server", "web cache"):
                    if node_from.returnName() == "hub": # packets flowing from hub always run before switch
                        num = 2
                    else:
                        num = 3
                    packets.append(Packets(node_from, node_to, self.colour, num))
                    self.hierarchy, self.server, self.unsecure_network = num, None, False # set up variables for next search
                    self.reverseRecursiveSearch(node_to)
                elif node_from.returnName() in ("hub", "switch"):
                    if node_to.returnName() == "printer":
                        for nodes in self.adjacency_list.values(): # ready for 'any' line below
                            for node in nodes:
                                temp_nodes.append(node)

                    if not any(node.returnName() == "print server" for node in temp_nodes): # if bridging device not connected to any print servers
                        if node_from.returnName() == "hub":
                            packets.append(Packets(node_from, node_to, self.colour, 2))
                        elif node_from.returnName() == "switch":
                            packets.append(Packets(node_from, node_to, self.colour, 3))

            elif node_to.returnName() in ("switch", "hub"):
                self.temp_packets.append([self.route_number, node_from, node_to, 2])

            if node_to in self.adjacency_list: # if node_to has other node connections
                self.recursiveBreadthSearch(node_to)

    def reverseRecursiveSearch(self, node_from): # calculates path to return to root PC
        if not self.unsecure_network: # if unsecure, will send same packet to each device connected to hub
            self.hierarchy += 1

        if node_from.returnName() == "print server":
            self.server = "print server"

        if node_from == self.root_node: # if returned to root node
            if self.server == "print server": # always will be here
                self.findPrinters(node_from, "printer") # to find closest printers

        else:
            for key, value in self.adjacency_list.items():
                add_route = True
                if node_from in value:
                    if key not in self.visited: # self.visited meaning if it was visited on way out
                        if not node_from.returnName() == "hub":
                            add_route = False
                        else:
                            self.unsecure_network = True # hub sends packets to all connected devices

                    elif node_from.returnName() == "hub":
                        self.unsecure_network = True

                    if add_route:
                        packets.append(Packets(node_from, key, self.colour, self.hierarchy))
                        self.reverseRecursiveSearch(key) # search next node in matrix

    def findPrinters(self, node_from, node_to): # finds closest printer on network
        for connected_node in self.adjacency_list[node_from]:
            if connected_node.returnName() == node_to:
                print_queue.enqueue(Packets(node_from, connected_node, self.colour, None))

            elif connected_node.returnName() in ("switch", "hub"):
                print_queue.enqueue(Packets(node_from, connected_node, self.colour, None))
                self.findPrinters(connected_node, node_to)
                # if not any(connected_node.returnName() == node_to for connected_node in self.adjacency_list[node_from]):
        print_queue.checkValid()

    def checkIfMovable(self, hierarchy): # checks if packet can move
        if any(packet.returnHierarchy() == (hierarchy, False) for packet in packets):
            return False
        else:
            return True

    def controlPackets(self): # controls flow of packets
        movable = False
        for packet in packets:
            if any(packet.returnHierarchy()[0] == 1 for packet in packets):
                hierarchy, cycle_status = packet.returnHierarchy()
                if not cycle_status:
                    for a in range(0, hierarchy):
                        movable = self.checkIfMovable(a)
                        if not movable:
                            break
                    if movable:
                        packet.blitToScreen()

        if not any(packet.returnHierarchy()[1] == False for packet in packets):
            if not print_queue.isEmpty() or not self.print_cycle_complete:
                if self.print_cycle_complete:
                    self.packet = print_queue.dequeue()
                    self.print_queue.append(self.packet)
                    self.print_cycle_complete = False
                elif self.packet.returnHierarchy()[1] == False:
                    self.packet.blitToScreen()
                else:
                    self.print_cycle_complete = True

            elif self.print_cycle_complete:
                for packet in self.print_queue:
                    packet.updateCycleStatus()
                    print_queue.enqueue(packet)
                self.print_queue = []
                for packet in packets:
                    packet.updateCycleStatus()


class Packets:
    def __init__(self, node_from, node_to, colour, hierarchy):
        self.node_from = node_from
        self.node_to = node_to
        self.x, self.y = node_from.returnPosition()
        self.speed = float(SpeedSlider.returnPacketSpeed())
        self.completed_cycle = False
        self.last_move = 0
        self.hierarchy_position = hierarchy
        self.colour = colour
        self.calculateGradient()

    def calculateGradient(self): # calculate direction and speed of packet
        self.x1, self.y1 = self.node_from.returnPosition()
        self.x, self.y = self.x1, self.y1
        self.x2, self.y2 = self.node_to.returnPosition()
        self.dx, self.dy = (self.x2 - self.x1, self.y2 - self.y1)
        self.stepx, self.stepy = (self.dx / self.speed, self.dy / self.speed)
        self.calculateStartPosition()

    def calculateStartPosition(self):
        self.x += 20
        self.y += 20
        self.x1, self.y1 = self.x, self.y

    def blitToScreen(self): # move packet on one step
        if int(round(self.x)) != self.x2+20 or int(round(self.y)) != self.y2+20:
            self.completed_cycle = False
            pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), 4)
            self.x += self.stepx
            self.y += self.stepy
        else:
            self.completed_cycle = True
            self.currently_moving = False
            self.x = self.x1
            self.y = self.y1

    def updateSpeed(self, speed): # update speed of packet
        self.speed = float(speed)
        self.calculateGradient()

    def updateCycleStatus(self): # node is ready to run again
        self.completed_cycle = False

    def returnHierarchy(self): # return hierarchy number and if ready to run again
        return self.hierarchy_position, self.completed_cycle

    def returnNodeFrom(self): # return node packet flows from
        return self.node_from

    def returnNodeTo(self): # return node packet flows to
        return self.node_to


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

    def handleEvent(self): # allow user to type in entry box
        self.text = ""
        while self.active:
            event = pygame.event.get()
            for ev in event:
                if ev.type == pygame.MOUSEBUTTONDOWN:
                    # If the user clicked on the input_box rect.
                    if not self.rect.collidepoint(ev.pos):
                        self.active, self.text = False, None

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

    def update(self):   # resize the box if the text is too long
        width = max(100, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self): # display text in box
        screen.fill((250, 250, 250))
        if self.box_type == "open":
            view_all = self.font.render("'all' to view all networks", True, (0, 0, 0))
            delete_net = self.font.render("'delete <network name>' to delete", True, (0, 0, 0))
            screen.blit(view_all, (1150, 140))
            screen.blit(delete_net, (1150, 155))
        screen.blit(self.box_name, (self.rect.x, self.rect.y-30))
        # Blit the text
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect
        pygame.draw.rect(screen, self.colour, self.rect, 2)

class DisplayAllNetworks(TextInputBox):
    def __init__(self, text):
        self.files = text
        super(DisplayAllNetworks, self).__init__(1150, 200, 60, 32, None, None)

    def draw(self): # modified version of inherited method to display all networks on screen
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

    def checkForSelection(self, event): # check if button clicked
        for ev in event:
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if self.rect.collidepoint(ev.pos):
                    if self.name == "open" or NodeAdjacencyList.returnDict():  # Check canvas isn't empty
                        self.getNetworkName()
                        if self.name == "save":
                            self.exportNetwork()
                        else:
                            self.retrieveData()

    def blitToScreen(self): # display on screen
        screen.blit(self.image, (self.x, self.y))

    def exportNetwork(self): # save network to pickle file
        if not self.network_name:
            self.text = self.font.render("Network not saved", True, (0,0,0))
        else:
            self.text = self.font.render(self.network_name+ " saved", True, (0,0,0))
            self.database_file = self.network_name + ".pkl"

            self.node_positions = []
            adj_list = NodeAdjacencyList.returnDict()
            for key, value in adj_list.items():
                for v in value:
                    application_running, server_properties = None, None
                    if key.returnName() == "pc":
                        application_running = key.returnRunningApplications()
                    if v.returnName() in ("file server", "print server", "e-mail server", "multimedia server", "web cache"):
                        v = Server
                        server_properties = v.returnProperties()
                    self.node_positions.append([key.returnName(), key.returnPosition(), v.returnName(), v.returnPosition(), application_running, server_properties])

            with open(self.database_file, "wb") as file:
                pickle.dump(self.node_positions, file) # create network file
                file.close()
            self.saveToDatabase()

        pygame.draw.rect(screen, (250,250,250), (1150, 60, 150, 100))
        screen.blit(self.text, (1170,70))
        pygame.display.flip()
        time.sleep(2)

    def getNetworkName(self): # get user input of network name
        text = "Enter network name:"
        self.input_box = TextInputBox(1150, 100, 60, 32, text, self.name)
        self.network_name = self.input_box.handleEvent()

    def saveToDatabase(self): # insert network name and file name to DB
        self.database.insertData(self.network_name, self.database_file)

    def retrieveData(self): # get network location from DB/ check for deletion and 'all' keywords
        if self.network_name:
            display_text = False
            if self.network_name.lower() == "all":
                self.displayAll()
            elif "delete" in self.network_name.lower():
                self.deleted = False
                self.deleteNetwork()
                if self.deleted:
                    self.text = self.font.render(self.network_name+ " deleted", True, (0,0,0))
                else:
                    self.text = self.font.render(self.network_name+ " does not exist", True, (0,0,0))
                display_text = True

            else:
                self.file_location = self.database.retrieveNetwork(self.network_name)
                file_exists = self.formatNetworkLocation()
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

    def displayAll(self): # display all network names and their dates
        files = self.database.displayAll()
        display_networks = DisplayAllNetworks(files)
        self.network_name = display_networks.handleEvent()
        self.retrieveData()

    def formatNetworkLocation(self): # format returned file name for importation
        for file_location in self.file_location:
            for f in file_location:
                openNetwork = ImportNetwork(f)
        try:
            openNetwork.importNetwork()
            return True
        except UnboundLocalError: # if no networks
            return False

    def deleteNetwork(self): # delete network from DB
        self.network_name = self.network_name.replace('delete ', '') # remove 'delete' keyword from network name
        self.deleted = self.database.deleteNetwork(self.network_name)

class ImportNetwork:
    def __init__(self, file_location):
        self.file_location = file_location

    def importNetwork(self): # import network from pickle file
        with open(self.file_location, "rb") as file:
            self.node_positions = pickle.load(file)
        self.positionNodes()
        self.sortAdjacencyList()

    def positionNodes(self): # position imported nodes on screen
        used_nodes = []
        for node_pos in self.node_positions:
            for node in nodes:
                unique = True
                if node.returnName() == node_pos[0]: # if node is correct type
                    for used_node in used_nodes:
                        if node_pos[1] == used_node[1]: # check if node been used
                            node_pos[0] = used_node[0] # replace node name with packet instance
                            node.updatePosition((node_pos[1])) # update node position
                            unique = False
                        if node == used_node[0]:
                            unique = False
                    if unique: # if node not already used
                        used_nodes.append([node, node_pos[1]]) # add node to used nodes
                        if node_pos[0] == "pc":
                            node.updateApplications(node_pos[4]) # update PC apps
                        node_pos[0] = node # replace node name in list with packet instance
                        node.updatePosition((node_pos[1])) # update node position

                elif node.returnName() == node_pos[2]: # run again checking nodeTo
                    for used_node in used_nodes:
                        if node_pos[3] == used_node[1]:
                            node_pos[2] = used_node[0]
                            node.updatePosition((node_pos[3]))
                            unique = False
                        if node == used_node[0]:
                            unique = False
                    if unique:
                        used_nodes.append([node,node_pos[3]])
                        if node_pos[2] == "server": # update server
                            Server.updateProperties(node_pos[5])
                            Server.updatePosition((node_pos[3]))
                            Server.displayDrives()
                            Server.blitServer()
                        node_pos[2] = node # replace nodeTo in list with packet instance
                        node.updatePosition((node_pos[3]))

    def sortAdjacencyList(self): # add imported node connections to matrix
        for node_pos in self.node_positions: # for each item in imported list
            if node_pos[5]: # if nodeTo is a server (has drive properties)
                for drive in node_pos[5]:
                    for server in Server_drives: # file server, print server, etc.
                        if server.returnName() == drive.lower():
                            NodeAdjacencyList.addToDict(node_pos[0], server) # add nodeFrom and server to matrix
            else:
                NodeAdjacencyList.addToDict(node_pos[0], node_pos[2]) # connect nodeFrom and nodeTo to server

class PrintQueue:
    def __init__(self):
        self.print_queue = []

    def enqueue(self, packet): # add packet to rear of queue
        print(self.print_queue)
        self.print_queue.insert(0, packet)

    def dequeue(self): # remove and return packet from front of queue
        if self.isEmpty():
            return None
        else:
            return self.print_queue.pop()

    def size(self): # return size of queue
        return len(self.print_queue)

    def isEmpty(self): # check if queue is empty
        return self.size() == 0

    def emptyQueue(self): # clear print queue
        self.print_queue = []

    def updateSpeed(self, speed): # update speed of packets in print queue
        for packet in self.print_queue:
            packet.updateSpeed(speed)

    def checkValid(self): # check if any printers in queue. If not, empty queue.
        if not any(packet.returnNodeTo().returnName() == "printer" for packet in self.print_queue):
            self.emptyQueue()

class SpeedSlider:
    def __init__(self):
        self.x = 1065
        self.packet_speed = 30
        self.pressed = False
        self.font = pygame.font.SysFont('Ariel', 22)
        self.text = self.font.render("Packet flow speed:", True, (0, 0, 0))

    def checkForSelection(self): # check for movement of slider
        if pygame.mouse.get_pressed()[0] != 0:
            for ev in pygame.event.get():
                try:
                    if self.circle.collidepoint(ev.pos) or self.pressed:
                        self.pressed = True
                        self.x = pygame.mouse.get_pos()[0]
                        if self.x < 1000:
                            self.x = 1000
                        elif self.x > 1130:
                            self.x = 1130
                        self.packet_speed = (130 - (self.x - 900)/2)
                        screen.fill((250, 250, 250))
                        callBlitToScreen()
                        self.blitToScreen()
                        for packet in packets:
                            packet.updateSpeed(self.packet_speed)
                        print_queue.updateSpeed(self.packet_speed)
                except AttributeError: # if no network saved
                    pass

        else:
            self.pressed = False

    def blitToScreen(self): # draw slider on screen
        screen.blit(self.text, (1000, 20))
        pygame.draw.rect(screen, (255,69,0), (1000, 50, 130, 10))
        self.circle = pygame.draw.circle(screen, (0,0,0), (self.x, 55), 8)

    def returnPacketSpeed(self): # return new packet speed
        return self.packet_speed

def displaySideBar(): # display bar enclosing nodes in
    bar_colour = (0, 0, 0)
    pygame.draw.line(screen, bar_colour, (110, 0), (110, 380), 5)
    pygame.draw.line(screen, bar_colour, (0, 378), (110, 378), 5)

def callBlitToScreen(): # runs multiple checks and calls objects to be drawn to screen
    SpeedSlider.checkForSelection()
    event = pygame.event.get()
    displaySideBar()

    if Server.returnActivated():
        Server.removeReduntantCables()
    SpeedSlider.blitToScreen()
    if NodeAdjacencyList.activated:
        NodeAdjacencyList.displayCables()
    for node in nodes[5:]:  # so server drives are not drawn
        node.blitToScreen()
    SaveButton.blitToScreen()
    OpenButton.blitToScreen()

    if Server.returnActivated():  # must be separate to similar statement above so that the servers are displayed above the cables
        Server.blitServer()
        Server.checkForMovementOrSelection()

    if PacketPath.returnActivated():
        PacketPath.controlPackets()
    OpenButton.checkForSelection(event)

    SaveButton.checkForSelection(event)

    pygame.display.flip()

NodeAdjacencyList = AdjacencyList()
SpeedSlider = SpeedSlider()
PacketPath = CreatePacketPath()
SaveButton = SaveAndLoadButtons("save_button.png", "save", 1200, 20)
OpenButton = SaveAndLoadButtons("open_button.png", "open", 1250, 20)

# define number of each node
NUMBER_PCS = 15
NUMBER_ROUTERS = 5
NUMBER_SWITCHES = 5
NUMBER_HUBS = 5
NUMBER_PRINTERS = 5

# instantiate each node and add to list
PCs = [PC() for x in range(NUMBER_PCS)]
Routers = [Router() for x in range(NUMBER_ROUTERS)]
Switches = [Switch() for x in range(NUMBER_SWITCHES)]
Hubs = [Hub() for x in range(NUMBER_HUBS)]
Printers = [Printer() for x in range(NUMBER_PRINTERS)]
Server = Server()
Cable = Cable()

# instantiate each server
File_server = Node((-100, -100), "server_drive.png", "File server", None, None, ["switch", "hub"])
Print_server = Node((-100, -100), "server_drive.png", "Print server", None, None, ["switch", "hub"])
Email_server = Node((-100, -100), "server_drive.png", "E-mail server", None, None, ["switch", "hub"])
Multimedia_server = Node((-100, -100), "server_drive.png", "Multimedia server", None, None, ["switch", "hub"])
Web_Cache_server = Node((-100, -100), "server_drive.png", "Web cache", None, None, ["switch", "hub"])

Server_drives = []
Server_drives.extend((File_server, Print_server, Email_server, Multimedia_server, Web_Cache_server))

nodes = []
packets = []
print_queue = PrintQueue()

# combine all nodes into one list for easy iteration
nodes.extend(Server_drives)
nodes.append(Server)
nodes.append(Cable)
nodes.extend(PCs)
nodes.extend(Routers)
nodes.extend(Switches)
nodes.extend(Hubs)
nodes.extend(Printers)

def runProgram(): # main
    screen.fill((250,250,250))
    callBlitToScreen()
    for node in nodes:
        touching = node.hoveringOver()
        while touching:
            touching = node.hoveringOver()
            screen.fill((250, 250, 250))
            callBlitToScreen()
            if node.returnName() == "cable":
                node.connectCableToNodes()
            elif node.returnName() == "server":
                if not node.returnActivated():
                    node.createServer()
            else:
                node.dragDrop(node)


done = False

while not done:
    runProgram()