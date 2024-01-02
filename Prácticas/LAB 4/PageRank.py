#!/usr/bin/python

from collections import namedtuple
import argparse
import time
import sys
import numpy as np

class Edge:
    def __init__ (self, origin=None):
        self.origin = origin    #IATA
        self.weight = 1.0       #weight

    def __repr__(self):
        return "edge: {0} {1}".format(self.origin, self.weight)
        
    ## write rest of code that you need for this class

class Airport:
    def __init__ (self, iden=None, name=None, id = None):
        self.code = iden
        self.name = name
        self.routes = []
        self.routeHash = dict()
        self.outweight = 0.0
        self.id = id

    def __repr__(self):
        return f"{self.code}\t{self.pageIndex}\t{self.name}"
            

edgeList = [] # list of Edge
edgeHash = dict() # hash of edge to ease the match
airportList = [] # list of Airport
airportHash = dict() # hash key IATA code -> Airport

def readAirports(fd):
    print("Reading Airport file from {0}".format(fd))
    airportsTxt = open(fd, "r", encoding="utf8")
    cont = 0
    for line in airportsTxt.readlines():
        a = Airport()
        try:
            temp = line.split(',')
            if len(temp[4]) != 5 :
                raise Exception('not an IATA code')
            a.name=temp[1][1:-1] + ", " + temp[3][1:-1]
            a.code=temp[4][1:-1]
        except Exception as inst:
            pass
        else:
            a.id=cont
            cont += 1
            airportList.append(a)
            airportHash[a.code] = a
    airportsTxt.close()
    print(f"There were {cont} Airports with IATA code")


def readRoutes(fd):
    print("Reading Routes file from {0}".format(fd))
    routesTxt = open(fd, "r", encoding="utf8")
    cont = 0
    for line in routesTxt.readlines():
        edg = Edge()
        try:
            temp = line.split(',')
            
            if len(temp[2]) != 3 or len(temp[4]) != 3:
                raise Exception('not an IATA code')
            
            orig = temp[2]
            dest = temp[4]

            if orig not in airportHash:
                raise Exception('Origin airport has no IATA code')
            if dest not in airportHash:
                raise Exception('Destination airport has no IATA code')



        except Exception as inst:
            pass
        else:
            airportO = airportHash[orig]
            airportO.outweight += 1.0
            airportD = airportHash[dest]
            if orig in airportD.routeHash:
                airportD.routeHash[orig].weight +=1.0
            else:
                edg.origin = orig
                edg.weight = 1.0
                airportD.routeHash[orig] = edg
                airportD.routes.append(edg)
                cont += 1

    routesTxt.close()
    print(f"There were {cont} Routes with IATA code")


def computePageRanks(maxIters, epsilon, l, debug):
    n = len(airportList)
    p = np.full(n,1/n)

    iterations = 0
    stop = False
    
    pesNoOutWeight = 1/n
    numOut = l*noOutWeight/n
    
    while not stop and iterations < maxIters:
        q = np.full(n,0.0)
        for i in range(0,n):
            sum = 0
            r = airportList[i].routes
            
            for e in r: 
                index = airportHash[e.origin].id
                sum += (p[index] * e.weight)/airportList[index].outweight
            q[i] = l * sum + (1.0-l)/n + pesNoOutWeight * numOut

        if debug:
            print(q.sum()) # check if the sum is 1
        pesNoOutWeight = (1-l)/n + pesNoOutWeight*numOut
        iterations +=1
        
        diff = list(map(lambda x,y: abs(x-y) ,p,q))
        stop = all(map(lambda valor: valor < epsilon, diff))

        p = q
        
    
    return p, iterations
    
    
def outputPageRanks(p,head):
    print("    <<<<<<<<<<<<<<<<<<<<<<<< PageRanks >>>>>>>>>>>>>>>>>>>>>>>> \n")
    list = []
    if head > len(p):
        head = len(p)
    for a in airportList:
        list.append((a.name,p[a.id]))
    list = sorted(list, key=lambda x: x[1], reverse=True)
    for x in list[:head]:
        print(f"    {x[0]} ==> {x[1]}")
    return

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--l', required=False, default=0.8, help='Lambda')
    parser.add_argument('--maxIters', required=False, default=500, help='Number of iterations to converge')
    parser.add_argument('--e', required=False, default=-10, help='Epsilon exponent value to converge')
    parser.add_argument('--head', required=False, default=10000000, help='Number of pageranks to see')
    parser.add_argument('--debug', required=False, default=False, help='Number of pageranks to see')


    
    args = parser.parse_args()
    l = float(args.l)
    maxIters = int(args.maxIters)
    epsilon = 10**(float(args.e))
    head = int(args.head)
    debug = args.debug == "True"

    readAirports("airports.txt")
    readRoutes("routes.txt")

    global noOutWeight
    noOutWeight = len(list(filter(lambda n: n.outweight == 0, airportList)))

    time1 = time.time()
    p, iterations = computePageRanks(maxIters, epsilon, l, debug)
    time2 = time.time()
    outputPageRanks(p,head)
    print("#Iterations:", iterations)
    print("Time of computePageRanks():", time2-time1)

if __name__ == "__main__":
    sys.exit(main())