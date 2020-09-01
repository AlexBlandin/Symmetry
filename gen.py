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
  
  # Display & Debugging
  def board(squares): return ["".join("#" if (x,y) in squares else
                                      "-" if (x,y) in product(indices,middle) or (x,y) in product(middle,indices) else
                                      " " for x in indices) for y in indices]
  def printout(branch, single=False, multiple=False):
    print(N, tuple(branch)); bd = [[] for _ in range(N)]
    for b in (symmetries(branch) if not single else [branch] if not multiple else branch):
      for i, line in enumerate(board(b)): bd[i].append(line)
    print("\n".join(" ".join(line) for line in bd));print()

  def lexo(branch):
    return tuple(sorted(map(sorted,symmetries(branch)))[0])
  def include(branch):
    global ob_branches, sb_branches
    s = symmetries(branch)
    ob_branches |= s
    sb_branches.add(lexo(branch)) # always get lexographically first branch

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

    # 23456789 01234567 (mod 10 for compactness)
    # 34567890 10123456 (+/- over/under 0 for R)
    # 45678901 21012345 
    # 56789012 32101234 
    # 67890123 43210123 
    # 78901234 54321012 
    # 89012345 65432101 
    # 90123456 76543210 

    #    56       34    (mod 10, just midrc)
    #    67       23    (+-over/under0 on R)
    #    78       12    
    # 56789012 32101234 
    # 67890123 43210123 
    #    01       21    
    #    12       32    
    #    23       43    

    # TODO: Reduce to just generating fundamental
    # TODO: Simplify.

    dob_branches, dsb_branches = set(), set()
    def include(branch):
      global dob_branches, dsb_branches
      s = symmetries(branch)
      dob_branches |= s
      dsb_branches.add(lexo(branch))
    left, right = lambda t: t[0], lambda t: t[1]
    def scanline(diag, coord=[], adia=[]):
      return {Q for Q in ((middle[0], diag-middle[0]), (middle[1], diag-middle[1]), (diag-middle[1],middle[1])) if sum(Q)==diag and 1<=Q[0]<=N and 1<=Q[1]<=N and Q[0] not in map(left, coord) and Q[1] not in map(right, coord) and Q[0]-Q[1] not in adia}
    for a in range(1+middle[0], 2*middle[0]): # This is correct and matches (also only generates the fundamentals as expected which is great) but since I'm simplifying I'll keep the checks to avoid breaking
      limit = 2*N-a+2 # stack of opposing limits
      rc1 = (a-middle[0], middle[0]) # stack of coords representing Queens (get diag as sum of tuple)
      adg = rc1[0]-rc1[1] # antidiagonal
      for b in range(a+1, limit+1):
        for rc2 in scanline(b, [rc1], [adg]):
          for c in range(b+1, limit+1):
            for rc3 in scanline(c, [rc1, rc2], [adg, rc2[0]-rc2[1]]):
              if rc2 in intersection or rc3 in intersection:
                branch = (rc1, rc2, rc3)
                if legal(frozenset(branch)):
                  if frozenset(branch) in dob_branches: ...#printout([branch, lexo(branch)],True,True)
                  else: include(branch)
              else:
                for d in range(c+1, limit+1):
                  for rc4 in scanline(d, [rc1, rc2, rc3], [adg, rc2[0]-rc2[1], rc3[0]-rc3[1]]):
                    branch = (rc1, rc2, rc3, rc4)
                    if legal(frozenset(branch)):
                      if frozenset(branch) in dob_branches: ...#printout([branch, lexo(branch)],True,True)
                      else: include(branch)

    if ob_branches != dob_branches or sb_branches != dsb_branches:
      print(f"{N} doesn't match, (ob, sb) are {(len(ob_branches), len(sb_branches))} != {(len(dob_branches), len(dsb_branches))}")
      break
else:
  print("All green.")