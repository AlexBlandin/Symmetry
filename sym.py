from collections import Counter as multiset
from itertools import product
from tabulate import tabulate

def main():
  k, MAX_N = 2, 50
  table = [["N", "branches", "orbits"]]
  table = [["N", "branches", "fundamental", "quotient", "orbits", "broken"]]
  for N in range(MAX_N+1):
    S, odd_N = multiset(), N%2
    indices = tuple(i for i in range(-(N//2), N//2+1) if i != 0 or odd_N)
    midrc = (0,) if odd_N else (1,-1) #  +  # middle row/col
    
    for branch in product(product(indices, midrc), product(midrc, indices)):
      if legal(branch):
        S.update(sym(branch))
    
    # branches = len(S)
    # orbits = multiset(S.values())
    # table.append([N, branches, dict(sorted(orbits.items(), key=lambda o:o[0], reverse=True))])
    
    branches = len(S)
    orbits = multiset(S.values())
    broken = {k: v//k for k,v in orbits.items()}
    fundamental = sum(broken.values())
    quotient = branches/fundamental if fundamental else 0
    table.append([N, branches, fundamental, quotient, dict(sorted(orbits.items(), key=lambda o:o[0], reverse=True)), broken])
  open(f"./data/test.txt", mode="w").write(tabulate(table, headers="firstrow", floatfmt=["d","d","d",".3f"]))

def legal(branch):
  (x,y), (a,b) = branch
  return not ((x != a or a != b) and (x==a or y==b or x+y==a+b or x-y==a-b))

def sym(points): # from set of points generate the symmetries as a set of frozen sets
  rx = frozenset((-x,y) for x,y in points); ry = frozenset((x,-y) for x,y in points)
  rd = frozenset((y,x) for x,y in points);  ra = frozenset((-x,-y) for x,y in points)
  r1 = frozenset((-y,x) for x,y in points); r2 = frozenset((-y,-x) for x,y in points)
  r3 = frozenset((y,-x) for x,y in points); r4 = frozenset(points)
  return {rx,ry,rd,ra,r1,r2,r3,r4}

def index_to_range(x,N): return (x-1 if N%2==0 and x >= 1 else x) + N//2
def board(points, indices): return [[(x,y) in points for x in indices] for y in indices]

if __name__ == "__main__": main()
