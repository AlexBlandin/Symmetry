from collections import Counter as multiset
from itertools import product, combinations
from tabulate import tabulate

# Configure
MIN_N, MAX_N = 8, 20
PLANAR = True

table = [["N", "ob(N)", "sb(N)", "quotient", "orbits", "fundamental", "err"]]
for N in range(MIN_N, MAX_N+1):
  branches, reduced, odd_N = multiset(), set(), N%2
  
  # Identify the middle rows and columns of the board, based on either natural coordinate-indices or planar
  indices = tuple(i for i in range(-(N//2), N//2+1) if i != 0 or odd_N) if PLANAR else tuple(range(1,N+1))
  middle = tuple(indices[(N-1)//2 : N//2+1]) # middle/median indices (single if odd_n else pair)
  intersection = frozenset(product(middle, middle))
  rows = (product(indices, middle),) if odd_N else (product(indices, middle[:1]), product(indices, middle[1:]))
  cols = (product(middle, indices),) if odd_N else (product(middle[:1], indices), product(middle[1:], indices))
  numrc = len(rows) + len(cols)

  # Key Functions
  def legal(branch): return ((len(branch) == numrc or
                            (len(branch) == numrc-1 and len(branch & intersection))) and
                            all((x,y)==(a,b) or (x!=a and y!=b and x+y!=a+b and x-y!=a-b) for (x,y),(a,b) in combinations(branch,2)))
  def symmetries(squares):
    return {
      frozenset((-x,y) for x,y in squares), frozenset((x,-y) for x,y in squares), frozenset((y,x) for x,y in squares), frozenset((-x,-y) for x,y in squares),
      frozenset((-y,x) for x,y in squares), frozenset((-y,-x) for x,y in squares), frozenset((y,-x) for x,y in squares), frozenset(squares),
    } if PLANAR else {
      frozenset(squares), frozenset((N-x+1,y) for x,y in squares), frozenset((x,N-y+1) for x,y in squares), frozenset((N-x+1,N-y+1) for x,y in squares),
      frozenset(), # todo: since fs((y,x) for x,y in squares) is wrong I need to figure out the alternative
    }
  
  # Display & Debugging
  def board(squares): return ["".join("#" if (x,y) in squares else
                                      "-" if (x,y) in product(indices,middle) or (x,y) in product(middle,indices) else
                                      " "
                                      for x in indices) for y in indices]
  def printout(branch):
    print(N, tuple(branch))
    bd = [[] for _ in range(N)]
    for b in symmetries(branch):
      for i, line in enumerate(board(b)): bd[i].append(line)
    print("\n".join(" ".join(line) for line in bd))
    print()
  
  # temp: 
  # printout((((0, -2), (-3, 0)) if odd_N else ((-4, -1), (1, -4), (-1, -3), (-3, 1))) if PLANAR else (((1, 4), (4, 2)) if odd_N else ((1, 4), (3, 5), (4, 2), (5, 6))))
  # exit()
  
  # Split over branches
  for branch in map(frozenset, product(*rows, *cols)):
    if branch not in branches and legal(branch):
      s = symmetries(branch)
      c = len(s)
      branches.update({b:c for b in s})
      reduced.add(branch)
  
  # Compute ob(N), sb(N), and assorted stats
  ob, orbits = len(branches), dict(sorted(multiset(branches.values()).items(), key=lambda o:o[0],reverse=True))
  fundamental = {k: v//k for k,v in orbits.items()}
  sb = sum(fundamental.values())
  quotient = ob/sb if sb else 0
  
  # Error logging
  err = []
  expected = (N-1)*(N-3)+1 if odd_N else [0,0,0,0,0,0,0,0,206,0, 844,0, 2642,0, 6656,0, 14326,0, 27476,0, 48314][N] if 8 <= N <= 20 else ob # 6*N*N - 30*N + 44 if N > 3 else 0
  if ob != expected: err.append(f"expected {expected} ob")
  expected = (N-1)*(N-3)//8+1 if odd_N else [0,0,0,0,0,0,0,0,30,0, 113,0, 342][N] if 8 <= N <= 12 else sb # N*(3*N-14)//4 + 5 if N > 3 else 0
  if sb != expected: err.append(f"expected {expected} sb")
  if sb != len(reduced): err.append(f"reduced implies {len(reduced)} sb")
  if len(err): err = ", ".join(err)
  table.append([N, ob, sb, quotient, orbits, fundamental] + [err]*bool(len(err)))

# Discard err column if there were no errors
if all(len(row)==len(table[0])-1 for row in table[1:]): table[0] = table[0][:-1]

# Write out results
open(f"./data/test.txt", mode="w").write(tabulate(table, headers="firstrow", floatfmt=["d","d","d",".3f"]))
