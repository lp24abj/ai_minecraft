#Including packages related to Amulet.
from amulet.api.selection import SelectionGroup
from amulet.api.level import BaseLevel
from amulet.api.data_types import Dimension
from amulet.api.block import Block

from minecraft_map import GetHeightMap

def operation(
    world: BaseLevel, dimension: Dimension, selection: SelectionGroup, options: dict
): 
    tileMap = GetHeightMap(world, selection[0])
export = {  
    "name": "Floodfill",
    "operation": operation,
}