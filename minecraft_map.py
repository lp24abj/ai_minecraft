import AmuletUtilities
from numpy import empty
#This function build the heightmao for a given selection.
def GetHeightMap(level, box):
    xmin = box.min_x
    xmax = box.max_x

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
