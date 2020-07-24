from itertools import chain, product, combinations
from collections import Counter as multiset
from tabulate import tabulate
from psutil import Process
from tqdm import tqdm
from sys import argv

def main():
  STRATEGY = argv[1] if len(argv)>1 else "midrc" # midrc | rings1 | rings2 | rings3
  r = 1 if STRATEGY not in ["rings2","rings3"] else {"rings2":2,"rings3":3}[STRATEGY]
  for k in range(2,4*r+1): # how many Queens to pre-place / branch on
    MAX_N = 50 if k==2 or STRATEGY in ["midrc","rings1"] else 30
    table = [["N", "symmetries", "branches", "quotient", "orbits"],[0,0,0,0.0,{}]]
    for N in tqdm(range(1,MAX_N+1), ascii=True): # we could start at 3
      S, sum_S, odd_N = multiset(), 0, N%2
      indices = tuple(i for i in range(-(N//2), N//2+1) if i != 0 or odd_N)
      midrc = (0,) if odd_N else (1,-1)    #  +  # middle row/col
      rings = (*indices[:r],*indices[-r:]) # [ ] # r outermost rings ("coronal")
      region = midrc if STRATEGY=="midrc" else rings
      for points in preplacement(region, indices, k):
        if legal(points): # bypass for lawless
          syms = sym(points) # todo: may need to consider 'internal' orbits from derived/continued board-states/placements for completion (separate multiset and stats)
          S.update(syms); sum_S += len(syms)
      rss = Process().memory_info().rss # rings2 k=6 N=14 uses 15.0 GB
      branches = len(S)
      quotient = sum_S/branches if branches else 0
      orbits = multiset(S.values())
      table.append([N, sum_S, branches, quotient, dict(sorted(orbits.items(), key=lambda o:o[0], reverse=True))])
      if rss >= 10_000_000_000: # exit out if we're using too much memory (currently 10GB)
        print(f"Exitting to avoid OOM, used {rss/1_000_000_000:.2f}GB")
        break
    open(f"./data/{STRATEGY}.k{k}.txt", mode="w").write(tabulate(table, headers="firstrow", floatfmt=["d","d","d",".8f"]))

def legal(points):
  "Whether a set of points are Queens-legal"
  for (x,y), (a,b) in combinations(points, 2):
    if x==a or y==b or x+y==a+b or x-y==a-b:
      return False
  return True

def preplacement(region, indices, k):
  points = set(chain(product(indices, region), product(region, indices)))
  return combinations(points, k)

def sym(points): # from set of points generate the symmetries as a set of frozen sets
  rx = frozenset((-x,y) for x,y in points); ry = frozenset((x,-y) for x,y in points)
  rd = frozenset((y,x) for x,y in points); ra = frozenset((-x,-y) for x,y in points)
  r1 = frozenset((-y,x) for x,y in points); r2 = frozenset((-y,-x) for x,y in points)
  r3 = frozenset((y,-x) for x,y in points); r4 = frozenset(points)
  return {rx,ry,rd,ra,r1,r2,r3,r4}

def index_to_range(x,N): return (x-1 if N%2==0 and x >= 1 else x) + N//2
def board(points, indices): return [[(x,y) in points for x in indices] for y in indices]

if __name__ == "__main__": main()
