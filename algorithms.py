import math
from unittest import case
import AmuletUtilities
import random
import numpy as np
from amulet.api.block import Block
import amulet
# from amulet.api.operations import paste
from amulet.api.selection import SelectionBox
from collections import Counter


from types import SimpleNamespace
#variables
NUMBER_GENE = 10
NUMBER_POPULATION = 200
LIST_HOUSE = [
    [13,14,7,"house_1.schem","House"],
    [9,10,6,"house_2.schem","Jail"],
    [10,10,8,"house_3.schem","House"],
    [8,6,6,"house_4.schem","Storage"],
    [8,6,6,"house_5.schem","Storage"],
    [9,7,4,"house_6.schem","Farm"],
    [11,17,7,"house_11.schem","Watchtower"],
    [8,6,5,"house_8.schem","Storage"], 
    [13,11,7,"house_9.schem","House"],
    [8,7,6,"house_10.schem","Storage"],
    #[12,7,12,"house_7.schem"], #church
    # [11,17,7,"house_11.schem"]
  ]
HOUSE_TYPES = {
    "House":2,
    "Farm":1,
    "Storage":4,
    "Jail":1,
    "Watchtower":2,
}

#create population
class House:
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
        self.type = pSize[4]
class Chromosome:
    def __init__(self, genes, fitness):
        self.genes = genes
        self.fitness = fitness
#house 11 [18,11,7]
def GenerticAlgorithm(box,height_map,population):
    chromosome_with_fitness = []
    for chromosome in population:
      # print(chromosome.genes)
      # print("Evaluating chromosome with genes: ", [house.name for house in env.genes])
      genes, fitness = CalculateFitness(box[0], height_map, chromosome.genes)
      # print("Fitness: ", fitness)
      chromosome_with_fitness.append(Chromosome(genes, fitness))
      # print(fitness)
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

def CalculateFitness(box, height_map, genes):
    width = box.max_x - box.min_x
    depth = box.max_z - box.min_z
    out = []

    for house in genes:
        sp = house.startPoint
        # Randomize start point if not set
        if sp.x == 0 and sp.z == 0:
            house.startPoint = SimpleNamespace()
            house.startPoint.x = random.randint(0, width - house.width)
            house.startPoint.z = random.randint(0, depth - house.length)

        # Compute blocking + update fields in one call
        house.isBlock, house.startPoint.y, house.floor = isHouseBlock(genes, house, height_map)
        out.append(house)
    fitness_score  = fitness(out)
    return out, fitness_score 

def fitness(chromosome):
    total = len(chromosome)
    valid = [h for h in chromosome if h.isBlock == False]
    
    # 1. Buildability
    buildability = len(valid) / total if total > 0 else 0
    
    # 2. Entropy on valid houses only
    if len(valid) > 0:
        types  = [h.type for h in valid]
        entropy_score = normalized_entropy(types, len(HOUSE_TYPES))
    else:
        entropy_score = 0.0
    # print("Buildability: %.4f, Entropy: %.4f" % (buildability, entropy_score))
    return (
        0.6 * buildability +
        0.4 * entropy_score
    )
def normalized_entropy(items, num_types):
    H = entropy(items)
    # print("Entropy H: ", H)
    H_max = math.log2(num_types)
    return H / H_max

def entropy(items):
    counts = Counter(items)
    total = sum(counts.values())
    
    H = 0.0
    for count in counts.values():
        p = count / total
        H -= p * math.log2(p)
    return H

def selection(population_withFitness):
    selected = random.sample(population_withFitness, 3)
    return max(selected, key=lambda x: x.fitness)



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
def mutate(genes, mutation_rate):
    for g in genes:
        if random.random() < mutation_rate:

            # 1. Mutate TYPE (quan trọng cho entropy)
            # if random.random() < 0.5:
                g = House("house_x", random.choice(LIST_HOUSE))

            # # 2. Mutate POSITION (an toàn)
            # else:
            #     g.startPoint.x += random.randint(-2, 2)
            #     g.startPoint.z += random.randint(-2, 2)
    return genes
def crossover(p1_genes, p2_genes):
    child = []
    for g1, g2 in zip(p1_genes, p2_genes):
        child.append(g1 if random.random() < 0.5 else g2)
    return child
def adaptive_mutation_rate(pop_entropy,
                           min_rate=0.03,
                           max_rate=0.25):
    return min_rate + (1 - pop_entropy) * (max_rate - min_rate)
def NextGeneration(population_withFitness, pop_entropy):
    next_generation = []
    mutation_rate = adaptive_mutation_rate(pop_entropy)

    while len(next_generation) < NUMBER_POPULATION:
        parent1 = selection(population_withFitness)
        parent2 = selection(population_withFitness)
        # print("Selected parents with fitness: ", parent1.fitness, parent2.fitness)
        # Filter non-block genes once
        p1_genes = parent1.genes
        p2_genes = parent2.genes

        # 1. Crossover
        child_genes = crossover(p1_genes, p2_genes)
        # print("Child genes before dedupe: ", [house.name for house in child_genes])
        # 2. Mutation
        child_genes = mutate(child_genes, mutation_rate)
        # print("Child genes after mutation: ", [house.name for house in child_genes])

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


#Issue 1:
# House next to house
# House in the top of house
# House in water and lava




