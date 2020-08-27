#!/usr/bin/env python3
from itertools import product, combinations, starmap

# Configure
MIN_N, MAX_N = 1, 20
for N, odd_N in [(N, N%2) for N in range(MIN_N, MAX_N+1)]:
  ob_branches, sb_branches = set(), set()
  
  indices = tuple(range(1,N+1))
  middle = tuple(indices[(N-1)//2 : N//2+1])
  intersection = frozenset(product(middle, middle))
  rows = (product(indices, middle),) if odd_N else (product(indices, middle[:1]), product(indices, middle[1:]))
  cols = (product(middle, indices),) if odd_N else (product(middle[:1], indices), product(middle[1:], indices))
  numrc = len(rows) + len(cols)

  # can trivially half the first row we branch on if we want a speed-up
  # rows = (product(indices[:N//2+1], middle),) if odd_N else (product(indices[:N//2], middle[:1]), product(indices, middle[1:]))

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
  
  def include(branch):
    global ob_branches, sb_branches
    ob_branches |= symmetries(branch)
    sb_branches.add(branch)

  if odd_N: # Odd N is solved, so we don't check and have no reason to break
    mid = middle[0] # the intersection of row and column
    for a in range(1, mid): # can use mid-1 to avoid a gndn loop but it's clearer not to
      for b in range(a+1, mid):
        branch = ((a,mid),(mid,b))
        include(branch)
    branch = ((mid,mid),)
    include(branch)
  else:
    for branch in map(frozenset, product(*rows, *cols)):
      if branch not in ob_branches and legal(branch):
        include(branch)
  
    dob_branches, dsb_branches = set(), set()
    for adia in range(middle[0]+1, 2*middle[0]): # we're following diag (middle[0],1) and (1,middle[0]) to the intersection
      # (x,y) is a square with x,y in 1..N, diag in 2..2N, adia in 1-N..N-1
      # diag = x+y, fixed x (cols) -> y = diag-x, fixed y (rows) -> x = diag-y
      # adia = x-y, fixed x (cols) -> y = x-adia, fixed y (rows) -> x = adia+y
      
      # diag  adia
      # 2345  0123 (above 0 are +ve)
      # 3456  1012 (below 0 are -ve)
      # 4567  2101 (can use adia for outermost iter?)
      # 5678  3210 (with diag being quick for inner?)
      # diag in 2,3,4,5,6,7,8
      # adia in 3,2,1,0,1,2,3 (-ve left of 0)
      pass
  
    if (len(ob_branches), len(sb_branches)) != (len(dob_branches), len(dsb_branches)):
      print(f"{N} doesn't match, (ob, sb) are {(len(ob_branches), len(sb_branches))} != {(len(dob_branches), len(dsb_branches))}")
      break
else:
  print("All green.")