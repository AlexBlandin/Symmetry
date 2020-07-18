from itertools import chain, product, combinations
from collections import Counter as multiset
from tabulate import tabulate
from tqdm import tqdm

def main():
  global k
  MAX_N = 50 # How big the board we should search up to
  k = 2 # how many Queens to place / branch on
  
  table = [["N", "orbits", "branches", "quotient"]]
  for _N in tqdm(range(1,MAX_N+1), ascii=True):
    global N
    N, odd_N = _N, _N%2 # for N*N Board
    Orb = set() # multiset() for dict-derived multiset
    sumorbit = 0
    
    indices = [i for i in range(-(N//2), N//2+1) if i != 0 or odd_N]
    midrc = [0] if odd_N else [1,-1] #  +  # cross/plus shaped "middle rows and columns"
    edges = [indices[0],indices[-1]] # [ ] # like +/evens in that 4 corners have 4-orbit like 2x2 centroid
    # in terms of symmetry, [] matches +/evens in terms of having two columns and two rows, in which each maps around in 8-orbits, and the corners 1+1+1+1 match the centroid 2x2 in their 4-orbits, so they're equivalent in terms of the quotient
    coron = lambda L: indices[:L] + indices[-L:] # coronal part of the board, where coron(1) == edges
    
    select = coron(3) # midrc | edges | coron(2)
    region = set(chain(product(indices, select), product(select, indices)))
    for points in preplacement(region):
      if len(points) == k:
        orbit = orbits(points)
        Orb.update(orbit) # Orb |= orbit # should be able to use in 3.9 for multiset
        sumorbit += len(orbit)
    branches = len(Orb)
    quotient = sumorbit/branches if branches else 0.0
    table.append([N, sumorbit, branches, quotient])
  
  with open("./data/data3.txt", mode="w") as o: o.write(tabulate(table, headers="firstrow", floatfmt=["d","d","d",".8f"]))

def preplacement(region): # todo: preplacement/branching that is always Queens-legal
  return set(map(frozenset, combinations(region, k)))

def orbits(points):
  # from one set generate the orbits as a set of frozen sets
  rx = frozenset((-x,y) for x,y in points)
  ry = frozenset((x,-y) for x,y in points)
  rd = frozenset((y,x) for x,y in points)
  ra = frozenset((-x,-y) for x,y in points)
  r1 = frozenset((-y,x) for x,y in points)
  r2 = frozenset((-y,-x) for x,y in points)
  r3 = frozenset((y,-x) for x,y in points)
  r4 = frozenset((x,y) for x,y in points) # r4 = identity
  return {rx,ry,rd,ra,r1,r2,r3,r4}

def board(p):
  "Places a set of (x,y) points `p` on an N*N ASCII board"
  b, c2i = [[0]*N for _ in range(N)], lambda x: (x-1 if N%2==0 and x >= 1 else x) + N//2
  for x,y in p: b[c2i(x)][c2i(y)]=1
  return "\n".join("".join(map(str,b[i])) for i in range(N))

if __name__ == "__main__": main()
