from amulet.api.selection import SelectionGroup
from amulet.api.level import BaseLevel
from amulet.api.data_types import Dimension
import amulet
import numpy as np
import AmuletUtilities

def my_schematic_paste(world: BaseLevel, dimension: Dimension, selection: SelectionGroup, options: dict):
    xmin = selection.min_x
    xmax = selection.max_x

    zmin = selection.min_z
    zmax = selection.max_z

    width = xmax - xmin
    depth = zmax - zmin

    #We are storing our Heightmap in a 2D array.
    heightMap = np.empty((width, depth), dtype=int)

    for x in range(xmin, xmax):
        for z in range(zmin, zmax):
            for y in range(255, - 1, -1):  #Y goes from 255 to 0        
                #For each location, we retrieve the block existing at these coordinates.
                block = AmuletUtilities.getBlockAt(x, y, z, world)
                # print(block)
                if AmuletUtilities.isBlockAir(block) == False:
                    print(block.base_name, " found at: ", x, y, z)
                    break
                    # if  AmuletUtilities.isBlockWater(block) == True or AmuletUtilities.isBlockLava(block) == True or AmuletUtilities.isBlockIce(block) == True:
                    #     # print("Water or Lava found at: ", x, y, z)
                    #     heightMap[x - xmin, z - zmin] = -1
                    #     break
                    # elif AmuletUtilities.isBlockGlass(block) == True:
                    #     print("takll Glass found at: ", x, y, z)
                    #     heightMap[x - xmin, z - zmin] = y - 1
                    #     break
                    # else:
                    #     heightMap[x - xmin, z - zmin] = y
                    #     break


export = {
    "name": "Check block types in area",
    "operation": my_schematic_paste
}