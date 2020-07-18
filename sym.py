from itertools import chain, product, combinations
from collections import Counter
from tabulate import tabulate
from tqdm import tqdm

def main():
  MAX_N = 100 # How big the board we should search up to
  k = 2 # how many Queens to place / branch on
  
  table = [["N", "orbits", "quotient"]]
  mem, rss = Process().memory_info, 0
  for _N in tqdm(range(1,MAX_N+1), ascii=True):
    global N
    N, odd_N = _N, _N%2 # for N*N Board
    T = set() # Counter() for dict-derived multiset
    sumorbit = 0
    
    # board centred on origin for trivial symmetry generation
    # N=6, indices = [-3,-2,-1,  1,2,3]
    # N=7, indices = [-3,-2,-1,0,1,2,3]
    indices = [i for i in range(-(N//2), N//2+1) if i != 0 or odd_N]
    midrc = [0] if odd_N else [1,-1] #  +  # cross/plus shaped "middle rows and columns"
    edges = [indices[0],indices[-1]] # [ ] # like +/evens in that 4 corners have 4-orbit like 2x2 centroid
    # in terms of symmetry, [] matches +/evens in terms of having two columns and two rows, in which each maps around in 8-orbits, and the corners 1+1+1+1 match the centroid 2x2 in their 4-orbits, so they're equivalent in terms of the quotient
    
    selection = set(chain(product(indices, edges), product(edges, indices)))
    # selection = set(chain(product(indices, midrc), product(midrc, indices)))
    for points in set(map(frozenset, combinations(selection, k))):
      if len(points) == k:
        # T.update(orbits(points)) # for `T = Counter()` if not in 3.9
        orbit = orbits(points)
        T |= orbit
        sumorbit += len(orbit)
    quotient = sumorbit/len(T) if len(T) else 0.0
    table.append([N, sumorbit, quotient])

  with open("./data.txt", mode="w") as o: o.write(tabulate(table, headers="firstrow", floatfmt=["d","d",".8f"]))

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

def plot(pl):
  "Place points on an ASCII board"
  b = [[0]*N for _ in range(N)]
  def c2i(x): return (x-1 if N%2==0 and x >= 1 else x) + N//2
  for x,y in pl:
    b[c2i(x)][c2i(y)]=1
  print("\n".join("".join(map(str,b[i])) for i in range(N)))

if __name__ == "__main__":
  main()
