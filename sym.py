from itertools import product, combinations, starmap
from collections import Counter as multiset
from tabulate import tabulate

# Configure
MIN_N, MAX_N = 8, 20

table = [["N", "ob(N)", "sb(N)", "quotient", "branch lengths", "orbits", "fundamental", "err"]]
for N in range(MIN_N, MAX_N+1):
  branches, broken, lengths, odd_N = multiset(), set(), multiset(), N%2
  
  # Identify the middle rows and columns of the board, based on natural 1..N coordinate-indices
  indices = tuple(range(1,N+1))
  middle = tuple(indices[(N-1)//2 : N//2+1]) # middle/median indices (single if odd_n else pair)
  intersection = frozenset(product(middle, middle))
  rows = (product(indices, middle),) if odd_N else (product(indices, middle[:1]), product(indices, middle[1:]))
  cols = (product(middle, indices),) if odd_N else (product(middle[:1], indices), product(middle[1:], indices))
  numrc = len(rows) + len(cols)

  # Key Functions
  def legal(branch): return ((len(branch) == numrc or
                            (len(branch) == numrc-1 and len(branch & intersection))) and
                            all((x,y)==(a,b) or (x!=a and y!=b and x+y!=a+b and x-y!=a-b) for (x,y),(a,b) in combinations(branch, 2)))
  def symmetries(squares):
    mirror, rotate = lambda x,y: (N-x+1, y), lambda x,y: (N-y+1, x)
    mirrors, rotates = lambda squares: starmap(mirror, squares), lambda squares: starmap(rotate, squares)
    return { frozenset(mirrors(squares)), frozenset(mirrors(rotates(squares))), frozenset(mirrors(rotates(rotates(squares)))), frozenset(mirrors(rotates(rotates(rotates(squares))))),
             frozenset(rotates(squares)), frozenset(rotates(rotates(squares))), frozenset(rotates(rotates(rotates(squares)))), frozenset(squares) }
  
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
    print("\n".join(" ".join(line) for line in bd));print()
  
  # Split over branches
  for branch in map(frozenset, product(*rows, *cols)):
    if branch not in branches and legal(branch):
      s = symmetries(branch)
      c = len(s)
      branches.update({b:c for b in s})
      broken.add(branch)
      lengths.update([len(branch)])

  # Compute ob(N), sb(N), and assorted stats
  ob, orbits = len(branches), dict(sorted(multiset(branches.values()).items(), key=lambda o:o[0],reverse=True))
  fundamental = {k: v//k for k,v in orbits.items()}
  sb = sum(fundamental.values())
  quotient = ob/sb if sb else 0
  lengths = dict(lengths)

  # Error logging
  err = []
  expected = (N-1)*(N-3)+1 if odd_N else [0,0,0,0,0,0,0,0,206,0, 844,0, 2642,0, 6656,0, 14326,0, 27476,0, 48314][N] if 8 <= N <= 20 else ob # 6*N*N - 30*N + 44 if N > 3 else 0
  if ob != expected: err.append(f"expected {expected} ob")
  expected = (N-1)*(N-3)//8+1 if odd_N else [0,0,0,0,0,0,0,0,30,0, 113,0, 342][N] if 8 <= N <= 12 else sb # N*(3*N-14)//4 + 5 if N > 3 else 0
  if sb != expected: err.append(f"expected {expected} sb")
  if sb != len(broken): err.append(f"broken implies {len(broken)} sb")
  if len(err): err = ", ".join(err)
  table.append([N, ob, sb, quotient, lengths, orbits, fundamental] + [err]*bool(len(err)))
  
  # todo: turn into output for verify.py
  # from pprint import pp
  # pp(sorted(broken))

# Discard err column if there were no errors
if all(len(row)==len(table[0])-1 for row in table[1:]): table[0] = table[0][:-1]

# Write out results
open(f"./data/test.txt", mode="w").write(tabulate(table, headers="firstrow", floatfmt=["d","d","d",".3f"]))
