Function recursiveBreadthSearch
Pass in: node_from
Add node_from to list of visited nodes
if node_from is a PC:
    Add one to the route number
    Get devices packets can visit based on PC's running apps.
    Get colour of PC packet
for nodes connected to node_from:
    if any nodes can be visited:
        Create packet route with node_from, connected node and route number
    if any servers connected to node_from:
        run reverseRecursiveSearch()
if all connected nodes have been visited:
    if any connected bridging devices:
        call recursiveBreathSearch()
        Pass in: next bridging device
Endfunction



Function AddToDict (NodeFrom, NodeTo)
    if NodeFrom = PC:
        Create new entry with NodeFrom as key and add NodeTo to
    elif NodeTo = PC:
        Dict[NodeTo] = NodeFrom
    elif NodeFrom = switch or hub:
        Add NodeTo to Dict[NodeFrom]
    elif NodeTo = switch or hub:
        Add NodeFrom to Dict[NodeTo]
End function


Function importNetwork
    Get name of network to open from text input box.
    Check it exists in the database.
    If exists, get the file name of the network from SQL database.
    Open pickle file.
    Replace the name of each node with an actual class instance from the nodes list.
    For every pair of connected nodes, get the position of each node from the imported list.
    Update these positions using the updatePosition() function in the Node class.
    Update any PC’s running applications using the updateRunningApplications() function in the PC class.
    Add each connection to the adjacency matrix.
    Run the createPacketPath() function to create the packet routes between imported nodes.
Endfunction



Function
recursiveBreadthSearch
Pass in: node_from
Add
node_from
to
visited
For
all
nodes(node_to)
connected
to
node_from:
if node_from is a PC:
    Set
    node_from as root
    node
    Add
    one
    to
    the
    route
    number
    Get
    devices
    packets
    can
    flow
    to
    based
    on
    PC’s
    running
    applications1

    Get
    colour
    of
    PC
    packets
    if node_to is in connectable nodes:
        Add
        packet
        route
    elif node_to is a bridging device:
        Add
        packet
        route and route
        number
        to
        temporary
        list
elif node_to is a connectable node:
    Remove
    duplicates
    from temporary list

    For
    each
    packet in the
    temporary
    list:
    if packet's route number is the current route number:
    Add
    packet
    route
if node_to is a server:
    Add
    packet
    route
    run
    reverseRecursiveSearch()
elif node_from is a bridging device:
    if node_to is a printer:
        if there are no print servers in network:
            Add
            packet
            route
elif node_to is a bridging device:
    Add
packet
route

if node_to has other connections:
    recursiveBreadthSearch(node_to)
Endfuction

Function exportNetwork
    Get the name of the network from user
    Create new pickle file based on network name

    From adjacency matrix, get the names of the nodes connected to each other.
    Get the position on screen of each node.
    Get details of any running applications and servers.

    Add the name, position and any running applications to a new list within a list called node_properties.

    Dump this list to the pickle file.
Endfunction