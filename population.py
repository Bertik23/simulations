import random
from math import inf
from matplotlib import pyplot as plt

REPRODUCTION_AGE = (15,60)
PARTNER_AGE_DEVIATION = 15
REPRODUCTION_BREAK = 10
MAX_BABIES = 10

death_rate = lambda age: 0#(age)/100

step = 0

id = 0

def mean(l):
    if len(l) == 0:
        return 0
    return sum(l)/len(l)

class Blob:
    def __init__(self, parents=None):
        global id
        self.parents = parents
        self.partner = None
        self.age = 0
        self.wantedBabies = -1
        self.childs = []
        self.childsNum = 0
        self.alive = True
        self.reproduced = -inf
        self.reproductions = []
        self.id = id
        id += 1
    def reproduce(self):
        if self.reproduced + REPRODUCTION_BREAK < step and self.alive:
            if self.age >= REPRODUCTION_AGE[0] and self.age <= REPRODUCTION_AGE[1]:
                if self.partner == None:
                    for blob in world:
                        if abs(blob.age - self.age) <= PARTNER_AGE_DEVIATION and blob.partner == None and blob.id != self.id and blob.alive:
                            self.partner = blob
                            blob.partner = self
                            print(self.age, self, blob)
                if self.partner != None:
                    if self.wantedBabies == -1:
                        if self.parents == None or self.partner.parents == None:
                            self.wantedBabies = -1
                        else:
                            try:
                                #print(self.parents[0].childsNum, self.partner.parents[1].childsNum)
                                self.wantedBabies = 2/(((len([ch for ch in self.parents[0].childs if ch.alive])/self.parents[0].childsNum)+(len([ch for ch in self.partner.parents[1].childs if ch.alive])/self.partner.parents[1].childsNum))/2)
                            except ZeroDivisionError as e:
                                print(type(e), e)
                                self.wantedBabies = -1
                    if (self.childsNum < self.wantedBabies or (self.wantedBabies == -1 and random.random() <= 0.5 and len([ch for ch in self.childs if ch.alive]) < 2)) and self.childsNum <= MAX_BABIES:
                        print(self, self.partner)
                        if self.childsNum >2:
                            print("MOOORE", self.childsNum)
                        self.reproduced = step
                        self.partner.reproduced = step
                        child = Blob((self,self.partner))
                        self.childs.append(child)
                        self.partner.childs.append(child)
                        self.childsNum += 1
                        self.partner.childsNum += 1
                        self.reproduced = step
                        self.partner.reproduced = step
                        self.reproductions.append(step)
                        self.partner.reproductions.append(step)
                        world.append(child)
                        if self.childsNum >2:
                            print("MOOORE", self.childsNum)
    def die(self):
        if random.random() < death_rate(self.age) or self.age >= 100:
            #print(death_rate(self.age), self.age)
            self.alive = False
            
    def __repr__(self):
        return f"Blob({id},{self.age})"
    
    def __str__(self):
        return f"Blob({id}, age={self.age},childs={self.childsNum}, reproduced={self.reproduced}, reproductions={self.reproductions})"
            
        
world = []
for i in range(10):
    world.append(Blob())
    world[-1].age = i+10
    print(world[-1])
    
population = []
avgDeathRate = []

while True:
    try:
        step += 1
        avgWantedBabiesList = []
        avgChildsList = []
        avgDeathRateList = []
        populationBefore = len(world)
        for blob in world:
            if not blob.alive:
                continue
            blob.die()
            blob.reproduce()
            blob.age += 1
            if blob.wantedBabies != -1:
                avgWantedBabiesList.append(blob.wantedBabies)
            if blob.childsNum != 0:
                avgChildsList.append(blob.childsNum)
                if blob.childsNum > 2: 
                    #print(blob, blob.childsNum)
                    pass
            avgDeathRateList.append(death_rate(blob.age))
        
        avgDeathRate.append(mean(avgDeathRateList))
        
        population.append(len([b for b in world if b.alive]))
        try:
            print(f"Step: {step}, avgWantedBabies: {mean(avgWantedBabiesList)}, avgChilds: {mean(avgChildsList)}, maxWanted: {max(avgWantedBabiesList)}, maxChilds: {max(avgChildsList)}, births: {len(world)-populationBefore}, population: {population[-1]}")
        except ValueError as e:
            if population[-1] == 0:
                break
            else:
                print(f"Step: {step}, avgWantedBabies: {mean(avgWantedBabiesList)}, {len(avgWantedBabiesList)}, {mean(avgChildsList)}, births: {len(world)-populationBefore}, population: {population[-1]}{e}")
        if step >= 10:
            break
    except KeyboardInterrupt:
        break

print(population,"\n\n\n", avgDeathRate)
plt.plot(range(len(population)), population, label="population")
maxPop = max(population)
plt.plot(range(len(avgDeathRate)), [i*maxPop for i in avgDeathRate], label="death_rate")
plt.show()
#print(world)
