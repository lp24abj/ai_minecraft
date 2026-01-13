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

# def GetHeightMap(level, selection):
#     # 1. Define bounds
#     xmin, xmax = selection.min_x, selection.max_x
#     zmin, zmax = selection.min_z, selection.max_z
#     width = xmax - xmin
#     depth = zmax - zmin
    
#     # Initialize heightmap with a default value (e.g., 0 or min_y)
#     heightMap = np.zeros((width, depth), dtype=int)

#     # 2. Iterate over chunks instead of blocks
#     # Amulet stores data in chunks (16x16 blocks). We process chunks that intersect our selection.
#     for cx in range(xmin >> 4, (xmax - 1 >> 4) + 1):
#         for cz in range(zmin >> 4, (zmax - 1 >> 4) + 1):
            
#             try:
#                 chunk = level.get_chunk(cx, cz, "minecraft:overworld") # Check your dimension name
#             except:
#                 continue # Chunk doesn't exist, skip
            
#             # 3. Get the 3D block palette index array
#             # This returns indices pointing to the block palette, not raw block names.
#             # Shape is typically (16, 256, 16) or similar (x, y, z)
#             blocks = chunk.blocks 
            
#             # 4. Determine overlap between chunk and selection
#             # Calculate local coordinates within the chunk (0-15)
#             # and global coordinates for the heightmap
            
#             # Global coordinates of the chunk
#             chunk_x_start = cx * 16
#             chunk_z_start = cz * 16
            
#             # Intersection logic
#             x_start_local = max(0, xmin - chunk_x_start)
#             x_end_local = min(16, xmax - chunk_x_start)
#             z_start_local = max(0, zmin - chunk_z_start)
#             z_end_local = min(16, zmax - chunk_z_start)
            
#             # Slice the chunk data relevant to our selection
#             # Note: Amulet block arrays are usually [x, y, z] or [y, x, z]. Check `blocks.shape`.
#             # Assuming [x, y, z] for this example:
#             chunk_slice = blocks[x_start_local:x_end_local, :, z_start_local:z_end_local]
            
#             # 5. Identify Block Types via Palette
#             # We need to find which IDs correspond to Air, Water/Lava, and Glass.
#             palette = chunk.block_palette
            
#             # Create boolean masks for the whole slice at once
#             # This is pseudo-code; implementation depends on how you look up IDs in AmuletUtilities
#             is_air = np.zeros(chunk_slice.shape, dtype=bool)
#             is_liquid = np.zeros(chunk_slice.shape, dtype=bool)
#             is_glass = np.zeros(chunk_slice.shape, dtype=bool)

#             # Map palette indices to your boolean categories efficiently
#             for i, block_obj in enumerate(palette):
#                 if AmuletUtilities.isBlockAir(block_obj):
#                     is_air[chunk_slice == i] = True
#                 elif AmuletUtilities.isBlockWater(block_obj) or AmuletUtilities.isBlockLava(block_obj) or AmuletUtilities.isBlockIce(block_obj):
#                     is_liquid[chunk_slice == i] = True
#                 elif AmuletUtilities.isBlockGlass(block_obj):
#                     is_glass[chunk_slice == i] = True
            
#             # 6. Calculate Heightmap for this slice
#             # Find the highest index where is_air is FALSE.
#             # We iterate top-down naturally by reversing the array or using max logic.
            
#             # Create a mask of "solid" blocks (anything not air)
#             is_solid = ~is_air
            
#             # Find indices of the highest solid block
#             # y indices range 0..255. 
#             # We multiply solid mask by y-indices to get heights, then take max over Y axis
#             y_indices = np.arange(chunk_slice.shape[1]).reshape(1, -1, 1)
            
#             # This gives the raw Y coordinate of the highest non-air block
#             # argmax finds the *first* occurrence, so we usually flip or use math tricks.
#             # Easier trick: (is_solid * y_indices).max(axis=1)
#             highest_y = (is_solid * y_indices).max(axis=1)
            
#             # Now checking the TYPE of that highest block to apply your rules
#             # We need to fetch the block type at the calculated (x, highest_y, z)
            
#             # Create a grid of x, z to sample the 3D array at specific heights
#             w_slice, d_slice = highest_y.shape
#             x_grid, z_grid = np.indices((w_slice, d_slice))
            
#             # Sample the property masks at the highest y found
#             top_is_liquid = is_liquid[x_grid, highest_y, z_grid]
#             top_is_glass = is_glass[x_grid, highest_y, z_grid]
            
#             # Apply rules
#             # Default is the y height
#             final_slice_heights = highest_y.copy()
            
#             # Rule 1: Liquid -> -1
#             final_slice_heights[top_is_liquid] = -1
            
#             # Rule 2: Glass -> y - 1
#             final_slice_heights[top_is_glass] -= 1
            
#             # 7. Write to main heightmap
#             hm_x_start = (chunk_x_start + x_start_local) - xmin
#             hm_x_end = (chunk_x_start + x_end_local) - xmin
#             hm_z_start = (chunk_z_start + z_start_local) - zmin
#             hm_z_end = (chunk_z_start + z_end_local) - zmin
            
#             heightMap[hm_x_start:hm_x_end, hm_z_start:hm_z_end] = final_slice_heights

#     return heightMap