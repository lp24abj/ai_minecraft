#Including packages related to Amulet.
from amulet.api.selection import SelectionGroup
from amulet.api.level import BaseLevel
from amulet.api.data_types import Dimension
from amulet.api.block import Block
import numpy as np
import logging

import amulet

import astars_function
import algorithms
import minecraft_map

# Select area 
# x1 = 212
# y1 = 63
# z1 = 329
# x2 = 264
# y2 = 63
# z2 = 257

NUMBER_GENERATIONS = 50
DIR_PATH = "C:\\Users\\phamt\\Desktop\\house\\"

def operation(
    world: BaseLevel, dimension: Dimension, box: SelectionGroup, options: dict
): 
    height_map = minecraft_map.GetHeightMap(world, box[0])
    
    # np.save('C:\\Users\\phamt\\Desktop\\house\\array_file.npy', height_map)
    # logging.basicConfig(filename="C:\\Users\\phamt\\Desktop\\house\\ai-log.log", filemode="w",
                    # format="%(name)s → %(levelname)s: %(message)s")
    # print(height_map)
    #genetic algorithm to place house in the area
    #step 1: create population
    population = algorithms.InitialPopulation()
    for generation in range(0, NUMBER_GENERATIONS):
        # print("Generation: ", generation)
        # print(population)
        house_withFitness = algorithms.GenerticAlgorithm(box,height_map, population)
        # logging.warning("House fitness in generation %d:", house_withFitness)
        avg_fitness = sum(chromosome.fitness for chromosome in house_withFitness) / len(house_withFitness)
        # logging.warning("Generation %d - Average Fitness: %.4f", generation, avg_fitness)
        population = algorithms.NextGeneration(house_withFitness,avg_fitness)
    
    #get the best house
    house_withFitness = algorithms.GenerticAlgorithm(box,height_map, population)
    thebest_population = algorithms.GetTheBestGenome(box, height_map, house_withFitness)
    dir_path = DIR_PATH
    for house in thebest_population.genes:
        # print("House: ", house.name, " at ", house.startPoint.x, house.startPoint.z,house.startPoint.y)
        # print("House size: ", house.width, house.length, house.height)  
        # print("isHouseBlock: ", house.isBlock)
        if house.isBlock == False:
            # #for debugging purpose, we only render the floor of the house
            algorithms.renderHouseFloor(house, box, world)
            #render house
            schem_path = f"{dir_path}{house.schem}"
            structure = amulet.load_level(schem_path)
            central_x = house.startPoint.x + house.width // 2
            central_z = house.startPoint.z + house.length // 2
            central_y = house.startPoint.y + house.height // 2 +1
            target_pos = (box.min_x + central_x, central_y, box.min_z+central_z)
            yield from world.paste_iter(structure, structure.dimensions[0], structure.selection_bounds, dimension, target_pos)
            print("Render done:")
            structure.close()
    #get hight map again after placing houses
    height_map = minecraft_map.GetHeightMap(world, box[0])
    visited_houses = []
    edges = []

    for house in thebest_population.genes:
      if house.isBlock == False:
        visited_houses.append(house)
        for other_house in thebest_population.genes:
          # print("Finding path from house ",other_house)
          # print("List of visited houses: ", visited_houses)
          if house.isBlock == False and other_house not in visited_houses:
            start,end = astars_function.findStartEnd(other_house,house,box[0])
            marks = astars_function.astarFloodFill(world,height_map, box[0], start, end)
            if(len(marks) > 0):
              # print("Path length: ", len(marks))
              edges.append((len(marks), house, other_house, marks))
    # print("All edges: ")
    all_houses = list(set([e[1] for e in edges] + [e[2] for e in edges]))
    mstedges, total_weight = astars_function.mst_kruskal(all_houses, edges)
    # print("MST edges: ", mstedges)
    for mst_edge in mstedges:
      marks = mst_edge[3]
      astars_function.render(world, marks)
    return
            

export = {  
    "name": "Generate Robin Hood",
    "operation": operation,
}