import random
from math import inf
from matplotlib import pyplot as plt
from statistics import median

REPRODUCTION_AGE = (15,60)
PARTNER_AGE_DEVIATION = 15
REPRODUCTION_BREAK = 10
MAX_BABIES = inf

SIM_STEPS = 10000
SIM_BLOBS = 1000

death_rate = lambda age: 10/1000

step = 0

id = 0

def roundTo(n, num):
 
    # Smaller multiple
    a = (num // n) * n
     
    # Larger multiple
    b = a + n
     
    # Return of closest of two
    return (b if n - a > b - n else a)


def toNearestPowerOf(n, num):
    print(roundTo(n, num))
    return n**(len(str(roundTo(n, num)))-1)

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
        self.id = 0+id
        self.birthstep = step
        id += 1
    def reproduce(self):
        #print(self.id)
        if self.reproduced + REPRODUCTION_BREAK < step and self.alive:
            if self.age >= REPRODUCTION_AGE[0] and self.age <= REPRODUCTION_AGE[1]:
                if self.partner == None or not self.partner.alive:
                    for blob in world:
                        if abs(blob.age - self.age) <= PARTNER_AGE_DEVIATION and (blob.age >= REPRODUCTION_AGE[0] and blob.age <= REPRODUCTION_AGE[1]) and blob.partner == None and blob.id != self.id and blob.alive:
                            self.partner = blob
                            blob.partner = self
                            #print(self.age, self.id, self, blob)
                            break
                if self.partner != None:
                    if self.wantedBabies == -1:
                        if self.parents == None or self.partner.parents == None:
                            self.wantedBabies = -1
                        else:
                            try:
                                #print(self.parents[0].childsNum, self.partner.parents[1].childsNum)
                                self.wantedBabies = 2/(((len([ch for ch in self.parents[0].childs if ch.alive])/self.parents[0].childsNum)+(len([ch for ch in self.partner.parents[1].childs if ch.alive])/self.partner.parents[1].childsNum))/2)
                                if random.random() < 0.5:
                                    self.wantedBabies = round(self.wantedBabies)
                            except ZeroDivisionError as e:
                                print(type(e), e)
                                self.wantedBabies = -1
                    if (self.childsNum < self.wantedBabies or (self.wantedBabies == -1 and len([ch for ch in self.childs if ch.alive]) < 2)) and self.childsNum <= MAX_BABIES:
                        if self.reproduced + REPRODUCTION_BREAK < step and self.partner.reproduced + REPRODUCTION_BREAK < step and random.random() < 0.5:
                            #print(self.reproduced + REPRODUCTION_BREAK, step)
                            self.reproduced = 0+step
                            self.partner.reproduced = 0+step
                            child = Blob((self,self.partner))
                            self.childs.append(child)
                            self.partner.childs.append(child)
                            self.childsNum += 1
                            self.partner.childsNum += 1
                            self.reproduced = 0+step
                            self.partner.reproduced = 0+step
                            self.reproductions.append(step)
                            self.partner.reproductions.append(step)
                            world.append(child)
                            return True
                        else:# self.reproduced + REPRODUCTION_BREAK >= step:# or self.partner.reproduced + REPRODUCTION_BREAK >= step:
                            #print(self.id, self.partner.id, self.reproduced + REPRODUCTION_BREAK, self.partner.reproduced + REPRODUCTION_BREAK, step)
                            return False

    def die(self):
        rn = random.random()
        if rn < death_rate(self.age) or self.age >= 100:
            #print(rn, death_rate(self.age))
            #print(death_rate(self.age), self.age)
            self.alive = False
            
    def __repr__(self):
        return f"Blob({self.id}, {self.age})"
    
    def __str__(self):
        if self.partner == None:
            partnerId = -1
        else:
            partnerId = self.partner.id
        return f"Blob({self.id}, age={self.age},childs={self.childsNum}, reproduced={self.reproduced}, reproductions={self.reproductions}, partner_id={partnerId})"
            
        
world = []
for i in range(SIM_BLOBS):
    world.append(Blob())
    world[-1].age = random.randint(0,100)
print(world)
    
population = []
avgDeathRate = []
deathRate = []
medianAge = []
meanAge = []
reproductionTries = []
avgWantedBabies = []
avgChilds = []

while True:
    try:
        step += 1
        avgWantedBabiesList = []
        avgChildsList = []
        avgDeathRateList = []
        reproductionTrie = 0
        ages = []
        populationBefore = len(world)
        removed = 0
        for blob in world:
            if not blob.alive and blob.birthstep+(2*REPRODUCTION_AGE[1]) < step:
                world.remove(blob)
                removed += 1
                continue
            if not blob.alive:
                continue
            #print(blob.id)
            blob.die()
            if not blob.alive: continue
            if blob.reproduce() == False: reproductionTrie += 1
            blob.age += 1
            if blob.wantedBabies != -1:
                avgWantedBabiesList.append(blob.wantedBabies)
            if blob.childsNum != 0:
                avgChildsList.append(blob.childsNum)
                # if blob.childsNum > blob.wantedBabies: 
                #     print(blob)
                #     pass
            avgDeathRateList.append(death_rate(blob.age))
            ages.append(blob.age)
        
        if len(ages) != 0:
            medianAge.append(median(ages))
        else:
            medianAge.append(0)
        meanAge.append(mean(ages))
        populationBefore -= removed
        
        reproductionTries.append(reproductionTrie)
        
        avgDeathRate.append(mean(avgDeathRateList))
        
        avgWantedBabies.append(mean(avgWantedBabiesList))
        avgChilds.append(mean(avgChildsList))
        
        population.append(len([b for b in world if b.alive]))
        try:
            deaths = population[-2]-population[-1]+(len(world)-populationBefore)
            deathRate.append((deaths/population[-2]))
        except IndexError:
            deaths = 0
            deathRate.append(0)

        

        try:
            print(f"Step: {step}, avgWantedBabies: {mean(avgWantedBabiesList)}, avgChilds: {mean(avgChildsList)}, maxWanted: {max(avgWantedBabiesList)}, maxChilds: {max(avgChildsList)}, births: {len(world)-populationBefore}, deaths: {deaths}, population: {population[-1]}")
        except ValueError as e:
            if population[-1] == 0:
                break
            else:
                print(f"Step: {step}, avgWantedBabies: {mean(avgWantedBabiesList)}, {len(avgWantedBabiesList)}, {mean(avgChildsList)}, births: {len(world)-populationBefore}, deaths: {deaths}, population: {population[-1]} {e}")
        if step >= SIM_STEPS:
            break
    except KeyboardInterrupt:
        break

# print(population,"\n\n\n", avgDeathRate)
poplulationPlot, = plt.plot(range(len(population)), population, label="population")
maxPop = toNearestPowerOf(10, max(population))
avgDeathRatePlot, = plt.plot(range(len(avgDeathRate)), [i*maxPop for i in avgDeathRate], label="avg_death_rate")
deathRatePlot, = plt.plot(range(len(deathRate)), [i*maxPop*10 for i in deathRate], label="death_rate", linestyle=":", zorder=10)
meanAgePlot, = plt.plot(range(len(meanAge)), [i*maxPop/100 for i in meanAge], label="mean_age")
medianAgePlot, = plt.plot(range(len(medianAge)), [i*maxPop/100 for i in medianAge], label="median_age")
reproductionTriesPlot, = plt.plot(range(len(reproductionTries)), [i*maxPop/100 for i in reproductionTries], label="reproduction_tries", zorder=-inf)
avgWantedBabiesPlot, = plt.plot(range(len(avgWantedBabies)), [i*maxPop/10 for i in avgWantedBabies], label="avg_wanted_babies")
avgChildsPlot, = plt.plot(range(len(avgChilds)), [i*maxPop/10 for i in avgChilds], label="avg_childs")
plt.legend([poplulationPlot, avgDeathRatePlot, deathRatePlot, meanAgePlot, medianAgePlot, reproductionTriesPlot, avgWantedBabiesPlot, avgChildsPlot],["Population","Avg Death Rate", f"Death Rate (1/{maxPop*10})", f"Mean Age (x{maxPop/100})", f"Median Age (x{maxPop/100})", f"Reproduction Tries (x{maxPop/100})", f"Avg Wanted Babies (x{maxPop/10})", f"Avg Childs (x{maxPop/10})"])

plt.show()
#print(world)
