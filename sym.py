from collections import Counter as multiset
from itertools import product
from tabulate import tabulate

def main():
  k, MAX_N = 2, 50
  table = [["N", "branches", "reduced", "quotient", "orbits", "fundamental"]]
  for N in range(MAX_N+1):
    S, odd_N = multiset(), N%2
    midrc = (0,) if odd_N else (1,-1) # middle rows/cols
    indices = tuple(i for i in range(-(N//2), N//2+1) if i != 0 or odd_N)
    
    for branch in product(product(indices, midrc), product(midrc, indices)):
      if legal(branch):
        S.update(sym(branch))
    
    branches = len(S)
    orbits = multiset(S.values())
    fundamental = {k: v//k for k,v in orbits.items()}
    reduced = sum(fundamental.values())
    quotient = branches/reduced if reduced else 0
    orbits = dict(sorted(orbits.items(), key=lambda o:o[0], reverse=True))
    table.append([N, branches, reduced, quotient, orbits, fundamental])
  open(f"./data/test.txt", mode="w").write(tabulate(table, headers="firstrow", floatfmt=["d","d","d",".3f"]))

def legal(branch):
  (x,y), (a,b) = branch
  return not (x != a or a != b) and (x==a or y==b or x+y==a+b or x-y==a-b))

def sym(squares): # from set of squares generate the symmetries as a set of frozen sets
  rx = frozenset((-x,y) for x,y in squares); ry = frozenset((x,-y) for x,y in squares)
  rd = frozenset((y,x) for x,y in squares);  ra = frozenset((-x,-y) for x,y in squares)
  r1 = frozenset((-y,x) for x,y in squares); r2 = frozenset((-y,-x) for x,y in squares)
  r3 = frozenset((y,-x) for x,y in squares); r4 = frozenset(squares)
  return {rx,ry,rd,ra,r1,r2,r3,r4}

def index_to_range(x,N): return (x-1 if N%2==0 and x >= 1 else x) + N//2
def board(squares, indices): return [[(x,y) in squares for x in indices] for y in indices]

if __name__ == "__main__": main()
