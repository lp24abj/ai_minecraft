#Including packages related to Amulet.
from amulet.api.selection import SelectionGroup
from amulet.api.level import BaseLevel
from amulet.api.data_types import Dimension
from amulet.api.block import Block

import enviroment

# Select area 
# x1 = 212
# y1 = 63
# z1 = 329
# x2 = 264
# y2 = 63
# z2 = 257

NUMBER_GENERATIONS = 200

def operation(
    world: BaseLevel, dimension: Dimension, box: SelectionGroup, options: dict
): 
    height_map = enviroment.GetHeightMap(world, box[0])
    print(height_map)
    #genetic algorithm to place house in the area
    #step 1: create population
    population = enviroment.InitialPopulation()
    for generation in range(0, NUMBER_GENERATIONS):
        print("Generation: ", generation)
        # print(population)
        house_withFitness = enviroment.GenerticAlgorithm(box,height_map, population)
        population = enviroment.NextGeneration(house_withFitness)
    
    #get the best house
    house_withFitness = enviroment.GenerticAlgorithm(box,height_map, population)
    selected_population = enviroment.selection(house_withFitness)
    thebest_population = selected_population[0]
    print("Final population: ")
    print("Best fitness: ", thebest_population.fitness)
    for house in thebest_population.genes:
        print("House: ", house.name, " at ", house.startPoint.x, house.startPoint.z)
        print("House size: ", house.width, house.length, house.height)  
        print("isHouseBlock: ", house.isBlock)
        if house.isBlock == False:
            enviroment.renderHouse(house, box[0], world)

export = {  
    "name": "Generic Robinhood",
    "operation": operation,
}