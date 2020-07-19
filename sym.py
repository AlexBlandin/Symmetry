from itertools import chain, product, combinations
from collections import Counter as multiset
from tabulate import tabulate
from tqdm import tqdm

def main():
  k = 2 # how many Queens to pre-place / branch on, we focus on k=2 (same as Q27)
  MAX_N = 50 # how big an N*N board we should cheack
  table = [["N", "symmetries", "branches", "quotient", "orbits"]]
  for _N in tqdm(range(1,MAX_N+1), ascii=True): # we could start at 3
    N, odd_N = _N, _N%2 # for N*N Board
    S, sum_S = multiset(), 0
    orbits = multiset()
    
    indices = tuple(i for i in range(-(N//2), N//2+1) if i != 0 or odd_N)
    midrc = (0,) if odd_N else (1,-1) #  +  
    edges = (indices[0], indices[-1]) # [ ] # edges of board
    rings = lambda r: (*indices[:r],*indices[-r:]) # [O] # r outermost rings, rings(1)=edges, Q27 had r=2, max k = 2*r (that gives legal points)
    
    region = rings(1) # midrc | edges | rings(2)
    for points in preplacement(region, indices, k):
      if len(points) == k and legal(points, True):
        syms = sym(points)
        S.update(syms)
        sum_S += len(syms)
    
    len_S = len(S)
    quotient = sum_S/len_S if len_S else 0
    orbits.update(S.values())
    table.append([N, sum_S, len_S, quotient, dict(orbits)])
  open(f"./data/test.txt", mode="w").write(tabulate(table, headers="firstrow", floatfmt=["d","d","d",".8f"]))

def legal(points, LEGAL=True):
  "Whether a set of points are Queens-legal (disable with LEGAL=False)"
  if not LEGAL: return True
  for xy in points:
    for ab in points:
      if xy!=ab:
        x,y, a,b = *xy, *ab
        if x==a or y==b or x+y==a+b or x-y==a-b:
          return False
  return True

def preplacement(region, indices, k):
  points = set(chain(product(indices, region), product(region, indices)))
  return combinations(points, k)

def sym(points): # from one set generate the symmetries as a set of frozen sets
  rx = frozenset((-x,y) for x,y in points); ry = frozenset((x,-y) for x,y in points)
  rd = frozenset((y,x) for x,y in points); ra = frozenset((-x,-y) for x,y in points)
  r1 = frozenset((-y,x) for x,y in points); r2 = frozenset((-y,-x) for x,y in points)
  r3 = frozenset((y,-x) for x,y in points); r4 = frozenset(points)
  return {rx,ry,rd,ra,r1,r2,r3,r4}

def index2coord(x): return (x-1 if N%2==0 and x >= 1 else x) + N//2

def board(s, N):
  b = [[0]*N for _ in range(N)]
  for x,y in s: b[index2coord(x)][index2coord(y)]=1
  return "\n".join("".join(map(str,b[i])) for i in range(N))

if __name__ == "__main__": main()
