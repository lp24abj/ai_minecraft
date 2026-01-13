from amulet.api.selection import SelectionGroup
from amulet.api.level import BaseLevel
from amulet.api.data_types import Dimension
import amulet

def my_schematic_paste(world: BaseLevel, dimension: Dimension, selection: SelectionGroup, options: dict):
    schem_path = f"C:\\Users\\phamt\\Desktop\\house\\house_10.schem"
    if not schem_path:
        return
        
    schem = amulet.load_level(schem_path)
    print("Schem loaded")
    schem_dimension = "minecraft:overworld"
    print("schem selection:", schem.dimensions[0])
    # schem_selection = schem.bounds('main')
    
    # Uses the minimum point of your current UI selection as the paste target
    target_pos = (206, 66, 318)
    
    yield from world.paste_iter(schem, schem.dimensions[0], schem.selection_bounds, dimension, target_pos,rotation=(0, 0, 0))
    schem.close()

export = {
    "name": "Paste External Schematic",
    "operation": my_schematic_paste
}