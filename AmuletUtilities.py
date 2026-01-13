
from amulet.api.selection import SelectionGroup
from amulet.api.level import BaseLevel
from amulet.api.data_types import Dimension
from amulet.api.block import Block


game_version = ("java", (1, 21, 0))
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

def isBlockTypeByList(block, blocktype):
    if not isinstance(block, Block):
        print("Object is not a block")
        return False
    return blocktype.count(block.base_name) > 0


def isBlockAir(block):
    return isBlockType(block, "air")

def isBlockGlass(block):
    return isBlockType(block, "short_grass") 
def isBlockWater(block):
    return isBlockType(block, "water")
def isBlockLava(block):
    return isBlockType(block, "lava")
def isBlockIce(block):
    return isBlockType(block, "ice")

def setBlockAt(x, y, z, block, level):
    level.set_version_block(
    x,  # x location
    y,  # y location
    z,  # z location
    "minecraft:overworld",  # dimension
    game_version,
    block
    )
def pasteBlockAt(x, y, z, block, level):
    yield from level.paste_iter(block, block.dimensions[0], block.selection_bounds, "minecraft:overworld", (x, y, z))