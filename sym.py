from itertools import chain, product, combinations
from time import time
from tabulate import tabulate
from tqdm import tqdm
from psutil import Process
from humanize import naturalsize
from collections import Counter
"""
construct (from a set of points on an N*N chessboard) all other sets of points of that set under symmetry

for any one given, pre-allocate and say "hey I expect these to be filled", once they're filled they can say in return "I expect this to be here and it was!"

for any given scheme (of how we select the points for splitting, either our + approach or the coronal approach etc) what's the average orbit?


currently implemented is the "+" selection, the orbits we're seeing for odd N k=1 is exactly https://oeis.org/A158057
TODO: implement coronal
TODO: figure out the evens orbits since it's approaching 6
TODO: figure out formula
"""

# 0,0 is the centre of the board, only appears on odd grids
# centre cluster for even boards are the (+-1,+-1) coords (no 0 on even boards)
# 8//2 == 4, so even then we shift >=0 by +1, so 0..7 -> -4,-3,-2,-1,1,2,3,4
# 7//2 == 3, so odd then we don't do anything, so 0..6 -> -3,-2,-1,0,1,2,3

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

def main():
  table = [["N", "orbits", "quotient"]]
  MAX_N, MAX_K = 200, 2
  mem, rss = Process().memory_info, 0
  with tqdm(range(1,MAX_N+1), ascii=True) as tq:
    for _N in tq:
      global N
      N = _N # N*N Board
      even = N%2==0
      
      rss = max(rss, mem().rss)
      tq.set_description(f"Processing N = {N} {naturalsize(rss)} used")
      # for _k in range(1, min(_N, MAX_K)+1):
      k = 2 # k = _k # how many Queens to place / branch on
      # T = Counter() # use to track occurences
      T, sumorbit = set(), 0
      
      indices = [i-N//2 for i in range(N)]
      if even:
        indices = [i+1 if i >= 0 else i for i in indices]
      middle = [1,-1] if even else [0]
      edge = [indices[0],indices[-1]]
      
      # selection = set(chain(product(indices, edge), product(edge, indices)))
      selection = set(chain(product(indices, middle), product(middle, indices)))
      for points in set(map(frozenset, combinations(selection, k))):
        if len(points) == k:
          # T.update(orbits(points)) # for `T = Counter()`
          orbit = orbits(points)
          T |= orbit
          sumorbit += len(orbit)
      rss = max(rss, mem().rss)
      
      # sumorbit = sum(T.values()) # for `T = Counter()`
      quotient = sumorbit/len(T) if len(T) else 0.0
      table.append([N, sumorbit, quotient])
      # end for
  table = tabulate(table, headers="firstrow", floatfmt=["d","d",".8f"])
  with open("./symdata2.txt", mode="w") as o:
    o.write(table)
    o.write("\n")

def plot(pl):
  "Place points on an ASCII board"
  b = [[0]*N for _ in range(N)]
  def c2i(x):
    "Convert to indices"
    if N%2==0 and x >= 1: x -= 1
    return x + N//2
  for x,y in pl:
    b[c2i(x)][c2i(y)]=1
  print("\n".join("".join(map(str,b[i])) for i in range(N)))


def human_time(t: float, seconds = True):
  return f"{int(t//60)}m {human_time((int(t)%60)+(t-int(t)), True)}" if t > 60 else f"{t:.3f}s" if t > 0.1 and seconds else f"{t*1000:.3f}ms" if t > 0.0001 else f"{t*1000000:.3f}us"

if __name__ == "__main__":
  main()
