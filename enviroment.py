import random
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
#house 11 [18,11,7]
def initialPopulation():
    list_house = [[11,12,7],[10,7,6],[10,9,8],[6,6,6],[4,5,6],[7,9,4],[7,10,12],[4,5,5],[9,11,8],[7,6,7]]
    #one house is gene
    population = []
    #debug 

    #run
    #random list public house
    number_gene = 11
    number_population = 20
    for p in range(1,number_population):
        chromosome = []
        for i in range(1, number_gene):
            chromosome.append(House(f"house_{i}", list_house[random.randint(0, 9)]))
        population.append(chromosome)
    print(population[0][0].name)

def calculateFitness():
    #if house in flat area fitness =  1
    #if house is not enough area fitness = 0


    #first get square of house
    # square = width * length
    # move one by one to box to find

    #random the start possition of house.
    #use breath search to find area suitable to put the house. if suitable add possion to block list

    #update the list as good gene and update to next
    pass
def isHouseBlock(width,length,startPoint,box):
    x = startPoint.x
    y = startPoint.y
    height = box(x,y).height

    isBlock = False

    for i in width:
        for j in length:
            current_height = box(x+i,y+j).heigth
            if current_height > height +1 or current_height < height - 1:
                isBlock = True
                break;
    
    return isBlock