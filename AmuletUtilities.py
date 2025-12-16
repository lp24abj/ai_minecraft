
from amulet.api.selection import SelectionGroup
from amulet.api.level import BaseLevel
from amulet.api.data_types import Dimension
from amulet.api.block import Block


game_version = ("java", (1, 19, 1))
def getBlockAt(x,y,z, level):
    block, block_entity = level.get_version_block(
    x,  # x location
    y,  # y location
    z,  # z location
    "minecraft:overworld",  # dimension
    game_version,
    )
    return block

def isBlockType(block, blocktype):
    if not isinstance(block, Block):
        print("Object is not a block")
        return False
    return block.base_name == blocktype

def isBlockAir(block):
    return isBlockType(block, "air")

def setBlockAt(x, y, z, block, level):
    level.set_version_block(
    x,  # x location
    y,  # y location
    z,  # z location
    "minecraft:overworld",  # dimension
    game_version,
    block
    )