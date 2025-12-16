#Including packages related to Amulet.
from amulet.api.selection import SelectionGroup
from amulet.api.level import BaseLevel
from amulet.api.data_types import Dimension
from amulet.api.block import Block

#Including packages for our algorithm.
from queue import PriorityQueue, Queue

from numpy import empty
import math
import heapq

#Including our own package that wrap Amulet's common functions.
import AmuletUtilities

#Declaring the operation entry point.
def operation(
    world: BaseLevel, dimension: Dimension, selection: SelectionGroup, options: dict
):  
    # print("selection:%s",selection)
    #First we compute the HeightMap.
    tileMap = getHeightMap(world, selection[0])
    # print("tilemap:%s",tileMap)

    start, end = findStartEnd(world, selection[0])
    print("start:",start)
    print("end:",end)
     #Then we compute our floodfill
    marks = astarFloodFill(world,tileMap, selection[0], start, end)
    #Then we compute our floodfill
    # marks = floodFill(tileMap, selection[0])
    print("marks:",marks)
    #Finally, we render our Floodfill result in the game world.
    render(world, start, end, marks)

#This function build the heightmao for a given selection.
def getHeightMap(level, box):
    xmin = box.min_x
    xmax = box.max_x
    # print("xmax:%s",xmax)
    # print("xmin:%s",xmin)
    zmin = box.min_z
    zmax = box.max_z

    width = xmax - xmin
    depth = zmax - zmin

    #We are storing our Heightmap in a 2D array.
    heightMap = empty((width, depth), dtype=int)

    #We are looping on every set of coordinates in our selection box, starting from the highest position to the lowest one.
    for x in range(xmin, xmax):
        for z in range(zmin, zmax):
            for y in range(255, - 1, -1):  #Y goes from 255 to 0        
                #For each location, we retrieve the block existing at these coordinates.
                block = AmuletUtilities.getBlockAt(x, y, z, level)
                if AmuletUtilities.isBlockAir(block) == False:
                    #If the block is not an empty block ("Air block"), it means we have reached the highest position.
                    #We are storing the Y coordinate in our HeightMap.
                    heightMap[x - xmin, z - zmin] = y
                    break

    #Once we have checked every coordinates, we return the completed Heightmap.
    return heightMap

#This function retrieve the neighbors block, using the 4 cardinal direction.
def neighbors(currBlock, box):
    #We declare our 4 direction.
    directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]
    neighborBlocks = []
    for direction in directions:
        #We retrieve the neighbor coordinates in each direction.
        neighbor = (currBlock[0] + direction[0], currBlock[1] + direction[1])
        if neighbor[0] >= box.min_x and neighbor[0] < box.max_x and neighbor[1] >= box.min_z and neighbor[1] < box.max_z:
            #If the new coordinates are in our selection box, we can append them to the list of valid neighbors.
            neighborBlocks.append(neighbor)
    
    #Once we have checked every coordinates, we return the completed lneighbors's list.
    return neighborBlocks

#This function runs the FloodFill algorithm.
def floodFill(heightMap, box):

    xmin = box.min_x
    zmin = box.min_z

    #We retrieve the starting point of the algorithm, which is the lowest coordinates of or selection box.
    start = (xmin, zmin)
    #We set up a queue for Breadth-first search, and imediatly enqueue our starting position.
    blockQueue = Queue()
    blockQueue.put(start)
    #We use a mark dictionnaries, which will keep track of the blocks that we have already visited, and also at which stage of the algorithm we visited it .
    #We imediatly add the starting position in our dictionnary, with the mark '0' since we checked it first.
    #Blocks are stored using their X,Z coordinates.
    marks = {}
    marks[start] = 0
    #We keep looping as long as our queue is not empty.
    while not blockQueue.empty():
        #We retrieve the top block in the queue.
        currentBlock = blockQueue.get()
        #Using the Heightmap, we also retrieve its Y coordinate.
        currY = heightMap[currentBlock[0] - xmin, currentBlock[1] - zmin]
        #We retrieve all its neighbors, and loop over them.
        for nextBlock in neighbors(currentBlock, box):
            if nextBlock not in marks:
                #If a neighbors has not been marked yet, we check its Y position.
                nextY = heightMap[nextBlock[0] - xmin, nextBlock[1] - zmin]
                diffY = abs(currY-nextY)
                #If the Y difference between the current block and the current neighbors is lower or equal to 1, we mark the neighbor and enqueue it.
                if diffY <= 1:
                    marks[nextBlock] = marks[currentBlock] + 1
                    blockQueue.put(nextBlock)

    #Once the queue is empty, we have made all the valid moves, and we can return the marks.
    return marks

def findStartEnd(level, box):
    xmin = box.min_x
    zmin = box.min_z

    xmax = box.max_x
    zmax = box.max_z

    start = (xmin, zmin) #S start
    end = (xmax, zmax) #E end
    #find the start box fence_gate block
    for x in range(xmin, xmax):
        for z in range(zmin, zmax):
            block = AmuletUtilities.getBlockAt(x, 57, z, level) #fix 56 for flooded area
            # print("block:",block.base_name)
            if block.base_name != "air":
              if block.base_name == "command_block":
                  start = (x,z)
                  # AmuletUtilities.setBlockAt(start[0], 57, start[1], blackBlock, level)
              if block.base_name == "repeater":
                  end = (x,z)
                  # AmuletUtilities.setBlockAt(end[0], 57, end[1], goldBlock, level)
    return start, end



def astarFloodFill(level,heightMap, selectedArea,start, end):
    xmin = selectedArea.min_x
    zmin = selectedArea.min_z

    visited = set() #Visited nodes
    # queue = PriorityQueue() #Priority queue for A* search
    queue = []
    #queue.put((0, start, [],0)) #Enqueue starting position with priority 0
    heapq.heappush(queue, (0, 0,[],start))
    marks = []
    interity = 23
    count =0
    # while not queue.empty():
    while queue:
        # if count > interity:
        #     break
        # count = count + 1

        
        print("----------------------")
        # print("queue",queue.queue)
        print("queue", queue)

        # queue_obj=queue.get()
        queue_obj=heapq.heappop(queue)
        currentBlock = queue_obj[3] #Get the block with the highest priority
        marks = queue_obj[2]
        cost = queue_obj[1]
        diamondBlock = Block("minecraft", "diamond_block")
        AmuletUtilities.setBlockAt(currentBlock[0], 56, currentBlock[1], diamondBlock, level)
        # if len(queue)>=3:
        #   print("queue", queue)
        #   queue_obj2=heapq.heappop(queue)
        #   print("queue", queue)
        if currentBlock in visited:
            continue
        visited.add(currentBlock) #Mark the block as visited
        currentmarks = marks.copy()
        currentmarks.append(currentBlock)

        print("block location:",currentBlock)
        print("priority:",queue_obj[0])
        # print("cost:",cost)
        # print("heuristic:",queue_obj[4])
        # print("marks:",marks)
        
        currY = heightMap[currentBlock[0] - xmin, currentBlock[1] - zmin]
        # print("queue:", queue)
        # grassBlock = Block("minecraft", "grass_block")
        # AmuletUtilities.setBlockAt(currentBlock[0], 57, currentBlock[1], grassBlock, level)
        #get 4 neighbors
        for nextBlock in neighbors(currentBlock, selectedArea):
            if nextBlock not in visited: #If the neighbor has not been visited yet
                nextY = heightMap[nextBlock[0] - xmin, nextBlock[1] - zmin] #get hieght of neighbor
                diffY = abs(currY-nextY) #get difference in height
                if diffY <= 1: #If the height difference is acceptable can move to neighbor
                    
                    #Calculate priority using cost so far (g) + heuristic (h) (Manhattan distance)
                    # g = euclidean_distance(nextBlock, start) #Cost so far (number of steps taken)
                    # g = cost + 1 #Cost so far (number of steps taken)
                    g = diffY + manhattan_distance(nextBlock, start)
                    #g =0
                    # h = euclidean_distance(nextBlock, end) #Heuristic (Euclidean distance to start)
                    h = manhattan_distance(nextBlock, end)
                    priority = g + h
                    # marks.append(nextBlock)
                    #priority = math.sqrt((nextBlock[0]-start[0])**2 + (nextBlock[1]-start[1])**2)
                    # print("cost G:",h)
                    # queue.put((priority, nextBlock, marks,cost+1)) #Enqueue neighbor with calculated priority
                    heapq.heappush(queue, (priority,g , currentmarks,nextBlock))

            if nextBlock == end:
                # mark = []
                # mark.put
                marks = currentmarks + [nextBlock]
                # queue = PriorityQueue() #Clear the queue to exit the while loop
                queue = []
                break

    # blackBlock = Block("minecraft", "black_wool")
    # goldBlock = Block("minecraft", "gold_block")
    # AmuletUtilities.setBlockAt(start[0], 57, start[1], blackBlock, level)
    # AmuletUtilities.setBlockAt(end[0], 57, end[1], goldBlock, level)
    return marks
def manhattan_distance(a, b):
    # print("a:",a)
    # print("b:",b)
    # print(a[0] - b[0])
    # print(a[1] - b[1])
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
def euclidean_distance(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)
#This functions render the marks values in the Minecraft World.
def render(level, start, end, marks):
    for mark in marks:
        x = mark[0]
        z = mark[1]
        grassBlock = Block("minecraft", "grass_block")
        AmuletUtilities.setBlockAt(x, 56, z, grassBlock, level)
    blackBlock = Block("minecraft", "black_wool")
    goldBlock = Block("minecraft", "gold_block")
    AmuletUtilities.setBlockAt(start[0], 57, start[1], blackBlock, level)
    AmuletUtilities.setBlockAt(end[0], 57, end[1], goldBlock, level)
#Exporting the operation for Amulet.
export = {  
    "name": "Floodfill",
    "operation": operation,
}