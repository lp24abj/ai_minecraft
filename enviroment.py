from unittest import case
import AmuletUtilities
import random
import numpy as np
from amulet.api.block import Block
import amulet
# from amulet.api.operations import paste
from amulet.api.selection import SelectionBox


from types import SimpleNamespace
#variables
NUMBER_GENE = 10
NUMBER_POPULATION = 200
LIST_HOUSE = [
    [13,14,7,"house_1.schem"],
    [9,10,6,"house_2.schem"],
    [10,10,8,"house_3.schem"],
    [8,6,6,"house_4.schem"],
    [8,6,6,"house_5.schem"],
    [9,7,4,"house_6.schem"],
    [11,17,7,"house_11.schem"],
    [8,6,5,"house_8.schem"], 
    [13,11,7,"house_9.schem"],
    [8,7,6,"house_10.schem"],
    #[12,7,12,"house_7.schem"], #church
    # [11,17,7,"house_11.schem"]
  ]

#create population
class House:
    #size of house calculate by block in minecraft
    # name=''
    # width = 0
    # length = 0
    # height = 0
    def __init__(self, pName, pSize):
        self.name = pName
        self.schem = pSize[3]
        self.width = pSize[0]
        self.length = pSize[1]
        self.height = pSize[2]
        self.startPoint = SimpleNamespace()
        self.startPoint.x = 0
        self.startPoint.z = 0
        self.startPoint.y = 0
        self.floor = []
        self.isBlock = False
class Chromosome:
    def __init__(self, genes, fitness):
        self.genes = genes
        self.fitness = fitness
#house 11 [18,11,7]
def GenerticAlgorithm(box,height_map,population):
    
    # print(len(population))
    #step 2: calculate fitness
    # print(selection[0])
    chromosome_with_fitness = []
    for chromosome in population:
      # print(chromosome.genes)
      # print("Evaluating chromosome with genes: ", [house.name for house in env.genes])
      genes, fitness = CalculateFitness(box[0], height_map, chromosome.genes)
      # print("Fitness: ", fitness)
      chromosome_with_fitness.append(Chromosome(genes, fitness))
    return chromosome_with_fitness
def InitialPopulation():
    population = []
    for _ in range(NUMBER_POPULATION):
        genes = [
            House(f"house_{i+1}", random.choice(LIST_HOUSE))
            for i in range(NUMBER_GENE)
        ]
        #0 if default fitness
        population.append(Chromosome(genes, -1))

    return population
def InitCentralChurch(box):
    # Precompute area once
    width = box.max_x - box.min_x
    depth = box.max_z - box.min_z
    out = []

    house = House("central", [1,1,9,"central.schem"])
    house.startPoint = SimpleNamespace()
    house.startPoint.x = random.randint(0, width - house.width)
    house.startPoint.z = random.randint(0, depth - house.length)

    return house
def CalculateFitness(box, height_map, genes):
    # Precompute area once
    width = box.max_x - box.min_x
    depth = box.max_z - box.min_z
    out = []

    total_block = 0
    n = len(genes)
    if n == 0:
        return [], 0.0

    for house in genes:
        sp = house.startPoint

        # Randomize start point if not set
        if sp.x == 0 and sp.z == 0:
            house.startPoint = SimpleNamespace()
            house.startPoint.x = random.randint(0, width - house.width)
            house.startPoint.z = random.randint(0, depth - house.length)

        # Compute blocking + update fields in one call
        house.isBlock, house.startPoint.y, house.floor = isHouseBlock(genes, house, height_map)
        if house.isBlock:
            total_block += 1

        out.append(house)

    return out, total_block / n

    

def selection(population_withFitness):
    #select the best gene
    sorted_population = sorted(population_withFitness, key=lambda x: x.fitness, reverse=False)
    # print("Sorted population: ", sorted_population)

    #select top 20%
    selected_population = sorted_population[:len(sorted_population)//2]
    # for individual in selected_population:
    #     print("Individual fitness: ", individual.fitness)
    return selected_population



def isHouseBlock(genes,house, box):
    x = house.startPoint.x
    z = house.startPoint.z
    # print("Start Point: ", x, z)
    #get height at start point from heightmap
    height = box[x,z]
    if height == -1:
        return True, 0, []
    
    # print(height)
    floor =[]
    for i in range(0, house.width):
        for j in range(0, house.length):
            # print("Checking at: ", x+i, z+j)
            current_height = box[x+i,z+j]
            floor.append([x+i,z+j])
            if current_height > height or current_height < height:
                return True, 0, []
    # print("Checked House with house")
    for other_house in genes:
        if other_house != house:
            common_elements = set(map(tuple, other_house.floor)) & set(map(tuple, house.floor))
            if common_elements:
                return True,0,[]
    return False,height,floor
#FINIAL LIS
def GetTheBestGenome(box, height_map, population_withFitness):
    #fiter only non-block house
    sorted_population = sorted(population_withFitness, key=lambda x: x.fitness, reverse=False)
    best_genome = sorted_population[0]
    return best_genome

#NEXT GENERATION FUNCTION UPDATED
def _gene_key(house):
    # same uniqueness rule you used
    return (house.name, house.startPoint.x, house.startPoint.z)

def _dedupe_genes(genes):
    # preserves first occurrence order (Python 3.7+ dict keeps insertion order)
    seen = {}
    for g in genes:
        k = _gene_key(g)
        if k not in seen:
            seen[k] = g
    return list(seen.values())

def _random_house(next_index):
    # next_index is 1-based "house_#"
    dims = random.choice(LIST_HOUSE)
    return House(f"house_{next_index}", dims)

def NextGeneration(population_withFitness):
    selected_population = selection(population_withFitness)
    next_generation = []

    # minor safety: if selection() can return empty
    if not selected_population:
        raise ValueError("selection() returned empty population")

    while len(next_generation) < NUMBER_POPULATION:
        parent1, parent2 = random.sample(selected_population, 2)

        # Filter non-block genes once
        p1 = [h for h in parent1.genes if not h.isBlock]
        p2 = [h for h in parent2.genes if not h.isBlock]

        # Merge + dedupe
        parent_genes = _dedupe_genes(p1 + p2)

        if len(parent_genes) >= NUMBER_GENE:
            # print("Crossover from parents")
            child_genes = random.sample(parent_genes, NUMBER_GENE)
        else:
            # print("Not enough genes, filling:", len(parent_genes))
            child_genes = list(parent_genes)

            # Fill remaining slots
            while len(child_genes) < NUMBER_GENE:
                child_genes.append(_random_house(len(child_genes) + 1))

        next_generation.append(Chromosome(child_genes, -1))
    return next_generation

#Generate House function
def renderHouseFloor(house, box, level):
    xmin = box.min_x
    zmin = box.min_z
    
    y = house.startPoint.y
    
    for coord in house.floor:
        cobbleBlock = Block("minecraft", "cobblestone")
        AmuletUtilities.setBlockAt(xmin+coord[0], y, zmin+coord[1], cobbleBlock, level)
    #for debug with 10 house types
    # if house.name =="house_1":
    #         block = Block("minecraft", "white_concrete")
    # elif house.name == "house_2":
    #         block = Block("minecraft", "black_concrete")
    # elif house.name == "house_3":
    #         block = Block("minecraft", "red_concrete")
    # elif house.name == "house_4":
    #         block = Block("minecraft", "blue_concrete")
    # elif house.name == "house_5":
    #         block = Block("minecraft", "lime_concrete")
    # elif house.name == "house_6":
    #         block = Block("minecraft", "yellow_concrete")
    # elif house.name == "house_7":
    #         block = Block("minecraft", "orange_concrete")
    # elif house.name == "house_8":
    #         block = Block("minecraft", "magenta_concrete")
    # elif house.name == "house_9":
    #         block = Block("minecraft", "cyan_concrete")
    # elif house.name == "house_10":
    #         block = Block("minecraft", "purple_concrete")
    # print("Rendering house: ", block)
    # AmuletUtilities.setBlockAt(xmin+house.startPoint.x, y, zmin+house.startPoint.z, block, level)


#Issue 1:
# House next to house
# House in the top of house
# House in water and lava




