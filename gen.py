#!/usr/bin/env python3
from itertools import product, combinations, starmap

# Configure
MIN_N, MAX_N = 1, 20
for N, odd_N in [(N, N%2) for N in range(MIN_N, MAX_N+1)]:
  ob_branches, sb_branches = set(), set()
  
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
    return { frozenset(squares), frozenset(mirrors(squares)), frozenset(mirrors(rotates(squares))),
             frozenset(mirrors(rotates(rotates(squares)))), frozenset(mirrors(rotates(rotates(rotates(squares))))),
             frozenset(rotates(squares)), frozenset(rotates(rotates(squares))), frozenset(rotates(rotates(rotates(squares)))) }
  
  # Base
  for branch in map(frozenset, product(*rows, *cols)):
    if branch not in ob_branches and legal(branch):
      ob_branches |= symmetries(branch)
      sb_branches.add(branch)
  
  # Halved first row we select, so half search space
  dob_branches, dsb_branches = set(), set()
  rows = (product(indices[:N//2+1], middle),) if odd_N else (product(indices[:N//2], middle[:1]), product(indices, middle[1:]))
  cols = (product(middle, indices),) if odd_N else (product(middle[:1], indices), product(middle[1:], indices))
  for branch in map(frozenset, product(*rows, *cols)):
    if branch not in dob_branches and legal(branch):
      dob_branches |= symmetries(branch)
      dsb_branches.add(branch)
  
  if (len(ob_branches), len(sb_branches)) != (len(dob_branches), len(dsb_branches)):
    print(f"{N} doesn't match, (ob, sb) are {(len(ob_branches), len(sb_branches))} != {(len(dob_branches), len(dsb_branches))}")
    break
else:
  print("All green.")