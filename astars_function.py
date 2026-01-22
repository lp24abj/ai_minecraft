from amulet.api.block import Block
import AmuletUtilities
import math
import heapq
def findStartEnd(first,second,box):
    xmin = box.min_x
    zmin = box.min_z

    xmax = box.max_x
    zmax = box.max_z

    start = (first.startPoint.x + xmin,first.startPoint.z + zmin,first.startPoint.y)
    end = (second.startPoint.x + xmin,second.startPoint.z + zmin,second.startPoint.y)
    return start, end
def astarFloodFill(level,heightMap, selectedArea,start, end):
    xmin = selectedArea.min_x
    zmin = selectedArea.min_z

    visited = set() #Visited nodes
    queue = []
    heapq.heappush(queue, (0, 0, [], start))
    marks = []
    while queue:
        
        queue_obj=heapq.heappop(queue)
        currentBlock = queue_obj[3] #Get the block with the highest priority
        marks = queue_obj[2]
        if currentBlock in visited:
            continue
        visited.add(currentBlock) #Mark the block as visited
        currentmarks = marks.copy()
        currentmarks.append(currentBlock)
        currY = currentBlock[2]
        for nextBlock in neighbors(currentBlock, selectedArea):
            if nextBlock not in visited:
                # print("Current Block: ", currentBlock, " Next Block: ", nextBlock)
                nextY = heightMap[nextBlock[0] - xmin, nextBlock[1] - zmin]
                diffY = abs(currY-nextY) #get difference in height
                
                if diffY <= 1:
                    g = diffY + euclidean_distance(nextBlock, start)
                    # print("nextBlock: ", nextBlock, " end: ", end )
                    h = euclidean_distance(nextBlock, end)
                    # print(h)
                    priority = g + h
                    heapq.heappush(queue, (priority,h , currentmarks,(nextBlock[0], nextBlock[1], nextY)))

            if nextBlock[0] == end[0] and nextBlock[1] == end[1]:
                # print("Path found!")
                marks = currentmarks + [nextBlock]
                queue = []
                break
    return marks
def euclidean_distance(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
def neighbors(currBlock, box):
    directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]
    neighborBlocks = []
    for direction in directions:
        neighbor = (currBlock[0] + direction[0], currBlock[1] + direction[1],0)
        if neighbor[0] >= box.min_x and neighbor[0] < box.max_x and neighbor[1] >= box.min_z and neighbor[1] < box.max_z:
            neighborBlocks.append(neighbor)
    return neighborBlocks
def render(level, marks):
    for mark in marks:
        x = mark[0]
        z = mark[1]
        y = mark[2]
        diamondBlock = Block("minecraft", "diamond_block")
        AmuletUtilities.setBlockAt(x, y, z, diamondBlock, level)
class DSU:
    def __init__(self, edges):
        self.parent = {obj: obj for obj in edges}
        self.rank = {obj: 0 for obj in edges}

    def find(self, obj):
        # print("Finding root of: ", obj)
        # print(self.parent)
        if self.parent[obj] == obj:
            return obj
        # Path compression
        self.parent[obj] = self.find(self.parent[obj])
        return self.parent[obj]

    def union(self, obj1, obj2):
        root1 = self.find(obj1)
        root2 = self.find(obj2)
        if root1 != root2:
            # print("rank before union: ", self.rank)
            # Union by rank
            if self.rank[root1] < self.rank[root2]:
                self.parent[root1] = root2
            elif self.rank[root1] > self.rank[root2]:
                self.parent[root2] = root1
            else:
                self.parent[root1] = root2
                self.rank[root2] += 1
            return True
        return False
def mst_kruskal(object, edges):
    sorted_edges =sorted(edges, key=lambda x: x[0], reverse=False)
    # print("Sorted edges for MST: ", sorted_edges)

    dsu = DSU(object)
    mst = []
    total_cost = 0
    num_v = len(sorted_edges)
    for weight, u, v ,marks in sorted_edges:
        # print("Processing edge: ", u.name, " - ", v.name, " with weight: ", weight)
        if dsu.union(u, v):
            mst.append((weight,u, v, marks))
            total_cost += weight
            if len(mst) == num_v - 1:
                break
    # print("Total cost of MST: ", total_cost)      
    return mst, total_cost