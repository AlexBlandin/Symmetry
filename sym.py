from itertools import chain, product, combinations
from collections import Counter as multiset
from sys import argv, getsizeof
from tabulate import tabulate
from tqdm import tqdm
from humanize import naturalsize

def main():
  STRATEGY = argv[1] if len(argv)>1 else "midrc" # midrc | rings(1) | rings(2) | rings(3)
  for k in range(1,{"midrc":4,"rings1":4,"rings2":8,"rings3":12}[STRATEGY]+1): # how many Queens to pre-place / branch on
    MAX_N = 50 if k==2 or STRATEGY in ["midrc","rings(1)"] else 20 # how big an N*N board we should check
    table = [["N", "symmetries", "branches", "quotient", "orbits"],[0,0,0,0.0,{}]]
    for N in tqdm(range(1,MAX_N+1), ascii=True): # we could start at 3
      orbits, odd_N = multiset(), N%2
      S, sum_S = multiset(), 0
      
      indices = tuple(i for i in range(-(N//2), N//2+1) if i != 0 or odd_N)
      midrc = (0,) if odd_N else (1,-1) #  +  # middle row/col
      edges = (indices[0], indices[-1]) # [ ] # edges of board = rings(1)
      rings = lambda r: (*indices[:r],*indices[-r:]) # [O] # Q27 did r=2, max k = 2*r (that gives legal points)
      
      region = {"midrc":midrc,"rings1":edges,"rings2":rings(2),"rings3":rings(3)}[STRATEGY]
      for points in preplacement(region, indices, k):
        if len(points) == k and legal(points, True):
          syms = sym(points) # todo: may need to consider 'internal' orbits from derived/continued board-states/placements for completion (separate multiset and stats)
          S.update(syms)
          sum_S += len(syms)
      
      len_S = len(S)
      quotient = sum_S/len_S if len_S else 0
      orbits.update(S.values())
      table.append([N, sum_S, len_S, quotient, dict(orbits)])
      size_S = getsizeof(S)
      if size_S >= 10_000_000_000: # exit out if we're using too much memory (currently 10GB)
        print(f"SYMERR: Exitting to avoid OOM {naturalsize(getsizeof(S))}")
        break
    open(f"./data/{STRATEGY}.k{k}.txt", mode="w").write(tabulate(table, headers="firstrow", floatfmt=["d","d","d",".8f"]))

def legal(points, LEGAL=True):
  "Whether a set of points are Queens-legal (disable with LEGAL=False)"
  if not LEGAL: return True
  for xy, ab in combinations(points, 2): # poly check instead of linear because simplicity and because k=2
    if xy!=ab: # faster to check and then destructure
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

def index_to_range(x): return (x-1 if N%2==0 and x >= 1 else x) + N//2
def board(points, indices): return [[(x,y) in points for x in indices] for y in indices]

if __name__ == "__main__": main()
