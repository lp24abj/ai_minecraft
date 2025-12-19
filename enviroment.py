import AmuletUtilities
from numpy import empty
import random
from amulet.api.block import Block

from types import SimpleNamespace
#variables
NUMBER_GENE = 10
NUMBER_POPULATION = 200
LIST_HOUSE = [[11,12,7],[10,7,6],[10,9,8],[6,6,6],[4,5,6],[7,9,4],[7,10,12],[4,5,5],[9,11,8],[7,6,7]]

#create population
class House:
    #size of house calculate by block in minecraft
    # name=''
    # width = 0
    # length = 0
    # height = 0
    def __init__(self, pName, pSize):
        self.name = pName
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
    house_withFitness = []
    for chromosome in population:
      # print(chromosome.genes)
      # print("Evaluating chromosome with genes: ", [house.name for house in env.genes])
      generation, fitness = CalculateFitness(box[0], height_map, chromosome.genes)
      # print("Fitness: ", fitness)
      house_withFitness.append(Chromosome(generation, fitness))
    return house_withFitness
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
def CalculateFitness(box,height_map, genes):
    xmin = box.min_x
    xmax = box.max_x

    zmin = box.min_z
    zmax = box.max_z

    width = xmax - xmin
    depth = zmax - zmin



    #if house in flat area fitness =  1
    #if house is not enough area fitness = 0
    house_withFitness = []
    totalBlock=0
    #update the list as good gene and update to next
    for house in genes:
      # print(house)
      if house.startPoint.x == 0 and house.startPoint.z == 0:
        start_point = SimpleNamespace()
        start_point.x = random.randint(0, width- house.width)
        start_point.z = random.randint(0, depth- house.length)  
        house.startPoint = start_point
      # print("House: ", house.name, " at ", start_point.x, start_point.z)
      # print("House size: ", house.width, house.length, house.height)  
      # print("isHouseBlock: ", house.isBlock)
      house.isBlock,house.startPoint.x,house.startPoint.z,house.startPoint.y,house.floor = isHouseBlock(genes,house, height_map)
      # blockByOther = isHouseBlockByOtherHouse(genes, house, height_map)
      # if blockByOther == True:
      #     house.isBlock = True
      if house.isBlock == True:
          totalBlock +=1
      house_withFitness.append(house)
    return house_withFitness,totalBlock/len(genes) 


# def NextGeneration(population_withFitness):
#     #create next generation
#     selected_population = selection(population_withFitness)
#     next_generation = []
#     while len(next_generation) < NUMBER_POPULATION:
#         # random.seed()
#         parent1 = random.choice(selected_population)
#         parent2 = random.choice(selected_population)
#         #crossover
#         #get all house from parent1 and parent2 whern isblock is false
#         parent1_genes = [house for house in parent1.genes if not house.isBlock]
#         # for house in parent1_genes:
#         #     print("Parent1 house: ", house.name, " isBlock: ", house.isBlock)
#         parent2_genes = [house for house in parent2.genes if not house.isBlock]
#         # for house in parent2_genes:
#         #     print("Parent2 house: ", house.name, " isBlock: ", house.isBlock)
#         #merge genes
#         merge_genes = parent1_genes + parent2_genes
#         #remove duplicate genes by name and start point
#         unique_genes = {}
#         for house in merge_genes:
#             key = (house.name, house.startPoint.x, house.startPoint.z)
#             if key not in unique_genes:
#                 unique_genes[key] = house
#         parent_genes = list(unique_genes.values())

#         #check length of parent genes
#         if len(parent_genes) >= NUMBER_GENE:
#             #random select genes from parent1 and parent2
#             print("Crossover from parents")
#             child_genes = random.sample(parent_genes, NUMBER_GENE)
#         else:
#             print("Not enough genes from parents, filling with random genes",len(parent_genes))
#             #if not enough genes, fill with random genes
#             child_genes = parent_genes
#             list_house = [[11,12,7],[10,7,6],[10,9,8],[6,6,6],[4,5,6],[7,9,4],[7,10,12],[4,5,5],[9,11,8],[7,6,7]]
#             while len(child_genes) < NUMBER_GENE:
#                 random.seed()
#                 child_genes.append(House(f"house_{len(child_genes)+1}", list_house[random.randint(0, 9)]))

#         # crossover_point = random.randint(1, NUMBER_GENE - 1)
#         # child_genes = parent1.genes[:crossover_point] + parent2.genes[crossover_point:]
#         #mutation
#         # if random.random() < 0.1:  #10% chance of mutation
#         #     mutation_point = random.randint(0, NUMBER_GENE - 1)
#         #     list_house = [[11,12,7],[10,7,6],[10,9,8],[6,6,6],[4,5,6],[7,9,4],[7,10,12],[4,5,5],[9,11,8],[7,6,7]]
#         #     child_genes[mutation_point] = House(f"house_{mutation_point+1}", list_house[random.randint(0, 9)])
#         next_generation.append(Chromosome(child_genes, -1))
#     return next_generation   
def selection(population_withFitness):
    #select the best gene
    sorted_population = sorted(population_withFitness, key=lambda x: x.fitness, reverse=False)
    # print("Sorted population: ", sorted_population)

    #select top 20%
    selected_population = sorted_population[:len(sorted_population)//20]
    for individual in selected_population:
        print("Individual fitness: ", individual.fitness)
    return selected_population

def renderHouse(house, box, level):
    xmin = box.min_x
    zmin = box.min_z

    xmax = box.max_x
    zmax = box.max_z
    
    x = house.startPoint.x
    z = house.startPoint.z
    y = house.startPoint.y
    # for i in range(0, house.width):
    #     for j in range(0, house.length):
    #         goldBlock = Block("minecraft", "gold_block")
    #         AmuletUtilities.setBlockAt(xmin+x+i, y, zmin+z+j, goldBlock, level)
    for coord in house.floor:
        goldBlock = Block("minecraft", "gold_block")
        AmuletUtilities.setBlockAt(xmin+coord[0], y, zmin+coord[1], goldBlock, level)
def isHouseBlock(genes,house, box):
    x = house.startPoint.x
    z = house.startPoint.z
    # print("Start Point: ", x, z)
    #get height at start point from heightmap
    height = box[x,z]
    # print(height)
    isBlock = False
    floor =[]
    for i in range(0, house.width):
        for j in range(0, house.length):
            # print("Checking at: ", x+i, z+j)
            current_height = box[x+i,z+j]
            floor.append([x+i,z+j])
            if current_height > height or current_height < height:
                return True, x, z, height, floor
    # print("Checked House with house")
    for other_house in genes:
        if other_house != house:
            common_elements = set(map(tuple, other_house.floor)) & set(map(tuple, house.floor))
            if common_elements:
                return True,x,z,height,floor
    return False,x,z,height,floor

def GetHeightMap(level, selection):
    xmin = selection.min_x
    xmax = selection.max_x

    zmin = selection.min_z
    zmax = selection.max_z

    width = xmax - xmin
    depth = zmax - zmin

    #We are storing our Heightmap in a 2D array.
    heightMap = empty((width, depth), dtype=int)

    for x in range(xmin, xmax):
        for z in range(zmin, zmax):
            for y in range(255, - 1, -1):  #Y goes from 255 to 0        
                #For each location, we retrieve the block existing at these coordinates.
                block = AmuletUtilities.getBlockAt(x, y, z, level)
                if AmuletUtilities.isBlockAir(block) == False:
                    heightMap[x - xmin, z - zmin] = y
                    break

    return heightMap


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
            # if debug:
            print("Crossover from parents")
            child_genes = random.sample(parent_genes, NUMBER_GENE)
        else:
            # if debug:
            print("Not enough genes, filling:", len(parent_genes))
            child_genes = list(parent_genes)

            # Fill remaining slots
            while len(child_genes) < NUMBER_GENE:
                child_genes.append(_random_house(len(child_genes) + 1))

        next_generation.append(Chromosome(child_genes, -1))
    return next_generation