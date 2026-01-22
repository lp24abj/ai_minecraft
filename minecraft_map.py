import AmuletUtilities
import random
import numpy as np

#HEIGHT MAP FUNCTION
def GetHeightMap(world, selection):
    xmin = selection.min_x
    xmax = selection.max_x

    zmin = selection.min_z
    zmax = selection.max_z

    width = xmax - xmin
    depth = zmax - zmin

    #We are storing our Heightmap in a 2D array.
    heightMap = np.empty((width, depth), dtype=int)
    type_block_glass = ["dandelion","short_grass","poppy","blue_orchid","allium","azure_bluet","red_tulip","orange_tulip","white_tulip","pink_tulip","oxeye_daisy","cornflower","lily_of_the_valley","wither_rose","sunflower_head","lilac","rose_bush","peony","tall_grass","large_fern"]
    for x in range(xmin, xmax):
        for z in range(zmin, zmax):
            for y in range(255, - 1, -1):  #Y goes from 255 to 0        
                #For each location, we retrieve the block existing at these coordinates.
                block = AmuletUtilities.getBlockAt(x, y, z, world)
                # print(block)
                if AmuletUtilities.isBlockAir(block) == False:
                    # print(block.base_name, " found at: ", x, y, z)
                    if  AmuletUtilities.isBlockWater(block) == True or AmuletUtilities.isBlockLava(block) == True or AmuletUtilities.isBlockIce(block) == True:
                        heightMap[x - xmin, z - zmin] = -1
                    elif AmuletUtilities.isBlockTypeByList(block, type_block_glass) == True:
                        heightMap[x - xmin, z - zmin] = y - 1
                    else:
                        heightMap[x - xmin, z - zmin] = y
                    break
                

    return heightMap