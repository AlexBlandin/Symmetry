from itertools import chain, product, combinations
from collections import Counter as multiset
from tabulate import tabulate
from tqdm import tqdm

def main():
  global k
  MAX_N = 50 # How big the board we should search up to
  k = 2 # how many Queens to pre-place / branch on, Q27 used 2 max and we only need 2 max, higher gets improved quotients but the combinatoric increase in combinations of points is far too much
  
  table = [["N", "symmetries", "branches", "quotient"]]
  for _N in tqdm(range(1,MAX_N+1), ascii=True):
    global N
    N, odd_N = _N, _N%2 # for N*N Board
    S, sum_S = set(), 0 # use a `multiset()` for dict-derived multiset
    
    indices = [i for i in range(-(N//2), N//2+1) if i != 0 or odd_N]
    midrc = [0] if odd_N else [1,-1] #  +  # cross/plus shaped "middle rows and columns"
    edges = [indices[0],indices[-1]] # [ ] # like +/evens in that 4 corners have 4-orbit like 2x2 centroid
    coron = lambda L: indices[:L] + indices[-L:] # coronal part of the board, edges == coron(1), Q27 used L=2
    # in terms of symmetry, [] matches +/evens in terms of having two columns and two rows, in which each maps around in 8-orbits, and the 4*1 corners match the 2x2 centroid in their symmetries, so ends up equivalent
    
    region = coron(1) # midrc | edges | coron(2)
    for points in preplacement(region, indices):
      if len(points) == k:
        syms = sym(points)
        S.update(syms) # S |= syms # should be able to use in 3.9 for multiset
        sum_S += len(syms)
    len_S = len(S)
    quotient = sum_S/len_S if len_S else 0
    table.append([N, sum_S, len_S, quotient])
  open("./data/test.txt", mode="w").write(tabulate(table, headers="firstrow", floatfmt=["d","d","d",".8f"]))

def preplacement(region, indices): # todo: preplacement/branching that is always Queens-legal
  s = set(chain(product(indices, region), product(region, indices)))
  return combinations(s, k)

def sym(points): # from one set generate the symmetries as a set of frozen sets
  rx = frozenset((-x,y) for x,y in points)
  ry = frozenset((x,-y) for x,y in points)
  rd = frozenset((y,x) for x,y in points)
  ra = frozenset((-x,-y) for x,y in points)
  r1 = frozenset((-y,x) for x,y in points)
  r2 = frozenset((-y,-x) for x,y in points)
  r3 = frozenset((y,-x) for x,y in points)
  r4 = frozenset((x,y) for x,y in points) # r4 = identity
  return {rx,ry,rd,ra,r1,r2,r3,r4}

def board(s):
  b, c2i = [[0]*N for _ in range(N)], lambda x: (x-1 if N%2==0 and x >= 1 else x) + N//2
  for x,y in s: b[c2i(x)][c2i(y)]=1
  return "\n".join("".join(map(str,b[i])) for i in range(N))

if __name__ == "__main__": main()
