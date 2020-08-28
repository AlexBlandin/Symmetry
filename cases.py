#!/usr/bin/env python3
from itertools import product, combinations, starmap
from math import log10, ceil

"""
Since the cases for the even N are rather hard to figure out, why not have this assist me?

probably need to do it somewhat differently and build up iteratively to keep it simple
and, if it could do the derivation and point out what came from where that'd be grand!

"""

"""
the diagonal scan gives sb(odd N) perfectly,
we can effectively simplify to first point (x,y) is all points on a row until you are adjacent to the middle (inclusive)
with then all points (i,j) on the column with a greater diagonal (i+k>x+y) until the middle (exclusive)
with then the middle point as the final piece
"""

MIN_N, MAX_N = 1, 20
for N, odd_N in [(N, N%2) for N in range(MIN_N, MAX_N+1)]:
  ob_branches, sb_branches = set(), set()
  
  indices = tuple(range(1,N+1))
  middle = tuple(indices[(N-1)//2 : N//2+1])
  intersection = frozenset(product(middle, middle))
  rows = (product(indices, middle),) if odd_N else (product(indices, middle[:1]), product(indices, middle[1:]))
  cols = (product(middle, indices),) if odd_N else (product(middle[:1], indices), product(middle[1:], indices))
  numrc = len(rows) + len(cols)

  def legal(branch): return ((len(branch) == numrc or
                            (len(branch) == numrc-1 and len(branch & intersection))) and
                            all((x,y)==(a,b) or (x!=a and y!=b and x+y!=a+b and x-y!=a-b) for (x,y),(a,b) in combinations(branch, 2)))
  def symmetries(squares):
    mirror, rotate = lambda x,y: (N-x+1, y), lambda x,y: (N-y+1, x)
    mirrors, rotates = lambda squares: starmap(mirror, squares), lambda squares: starmap(rotate, squares)
    return { frozenset(squares), frozenset(mirrors(squares)), frozenset(mirrors(rotates(squares))),
             frozenset(mirrors(rotates(rotates(squares)))), frozenset(mirrors(rotates(rotates(rotates(squares))))),
             frozenset(rotates(squares)), frozenset(rotates(rotates(squares))), frozenset(rotates(rotates(rotates(squares)))) }
  
  def board(squares): return ["".join("#" if (x,y) in squares else
                                      "-" if (x,y) in product(indices,middle) or (x,y) in product(middle,indices) else
                                      " " for x in indices) for y in indices]
  
  def include(branch):
    global ob_branches, sb_branches
    s = symmetries(branch)
    ob_branches |= s
    sb_branches.add(tuple(sorted(map(sorted,s))[0])) # always get lexographically first branch

  if odd_N:
    mid = middle[0] # the intersection of row and column
    for a in range(1, mid):
      for b in range(a+1, mid):
        branch = ((a,mid),(mid,b))
        include(branch)
    branch = ((mid,mid),)
    include(branch)
  else:
    for branch in map(frozenset, product(*rows, *cols)):
      if branch not in ob_branches and legal(branch):
        include(branch)
  
  root_branches = { branch for branch in sb_branches if (1,middle[0]) in branch }
  other_branches = sb_branches - root_branches
  sb = len(sb_branches)
  print(f"N: {N} sb: {sb}")
  zeroes = 1 if N < 3 else ceil(log10(sb))
  with open(f"data/cases{N:02}..txt",mode="w") as o:
    for i, (branch, s) in enumerate(map(lambda branch: (branch, symmetries(branch)), sorted(sb_branches)), 1):
      o.write(f"Branch {str(i).zfill(zeroes)}, {len(s)} orbits, i.e. ")
      o.write("{ ");o.write(", ".join(map(str,sorted(branch))));o.write(" }\n")
      bd = [[] for _ in range(N)]
      for b in sorted(map(sorted,s)):
        for i, line in enumerate(board(b)): bd[i].append(line)
      o.write("\n".join(" ".join(line) for line in bd));o.write("\n")
      o.write("\n")
  