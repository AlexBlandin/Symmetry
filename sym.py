from itertools import chain, product, combinations
from collections import Counter as multiset
from tabulate import tabulate
from tqdm import tqdm

def main():
  k = 2 # how many Queens to pre-place / branch on, we focus on k=2 (same as Q27)
  MAX_N = 50 # how big the board we should search up to
  table = [["N", "symmetries", "branches", "quotient"]]
  for _N in tqdm(range(1,MAX_N+1), ascii=True):
    N, odd_N = _N, _N%2 # for N*N Board
    S, sum_S = set(), 0 # use multiset() for dict-derived multiset
    
    indices = tuple(i for i in range(-(N//2), N//2+1) if i != 0 or odd_N)
    midrc = (0,) if odd_N else (1,-1) #  +  # midrc.branches(n) = {odd n: (n-1)(2n-1), even n: 2(n-1)(4n-5)
    edges = (indices[0], indices[-1]) # [ ] # edges of board, branches=https://oeis.org/A014635 +1 offset
    rings = lambda r: (*indices[:r],*indices[-r:]) # [O] # r outermost rings, rings(1)=edges, Q27 had r=2
    # edges ~ even N midrc: each point has 8-orbit except edges' 4*1 corners and midrc's 2x2 centroid
    
    region = rings(1) # midrc | edges | rings(2)
    for points in preplacement(region, indices, k):
      if len(points) == k:
        syms = sym(points)
        S += syms # use `S.update(syms)` if S=multiset()
        sum_S += len(syms)
    
    len_S = len(S)
    quotient = sum_S/len_S if len_S else 0
    table.append([N, sum_S, len_S, quotient])
  open("./data/test.txt", mode="w").write(tabulate(table, headers="firstrow", floatfmt=["d","d","d",".8f"]))

def preplacement(region, indices, k): # todo: preplacement/branching that is always Queens-legal
  s = set(chain(product(indices, region), product(region, indices)))
  return combinations(s, k)

def sym(points): # from one set generate the symmetries as a set of frozen sets
  rx = frozenset((-x,y) for x,y in points); ry = frozenset((x,-y) for x,y in points)
  rd = frozenset((y,x) for x,y in points); ra = frozenset((-x,-y) for x,y in points)
  r1 = frozenset((-y,x) for x,y in points); r2 = frozenset((-y,-x) for x,y in points)
  r3 = frozenset((y,-x) for x,y in points); r4 = frozenset(points)
  return {rx,ry,rd,ra,r1,r2,r3,r4}

def board(s, N):
  b, c2i = [[0]*N for _ in range(N)], lambda x: (x-1 if N%2==0 and x >= 1 else x) + N//2
  for x,y in s: b[c2i(x)][c2i(y)]=1
  return "\n".join("".join(map(str,b[i])) for i in range(N))

if __name__ == "__main__": main()
