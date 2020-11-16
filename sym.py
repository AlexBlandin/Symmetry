#!/usr/bin/env python3
from itertools import product, combinations, starmap
from collections import Counter as multiset
from tabulate import tabulate

# Configure
MIN_N, MAX_N = 1, 50
table = [["N", "ob(N)", "sb(N)", "quotient", "branch lengths", "orbits", "fundamental", "err"]]
for N, odd_N in [(N, N%2) for N in range(MIN_N, MAX_N+1)]:
  ob_branches, sb_branches, lengths = multiset(), set(), multiset()
  
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
  def lexo(branch):
    return tuple(sorted(map(sorted,symmetries(branch)))[0])
  
  # Display & Debugging
  def board(squares): return ["".join("#" if (x,y) in squares else
                                      "-" if (x,y) in product(indices,middle) or (x,y) in product(middle,indices) else
                                      " " for x in indices) for y in indices]
  def printout(branch, single=False, multiple=False):
    print(N, tuple(branch)); bd = [[] for _ in range(N)]
    for b in (symmetries(branch) if not single else [branch] if not multiple else branch):
      for i, line in enumerate(board(b)): bd[i].append(line)
    print("\n".join(" ".join(line) for line in bd));print()
  
  def include(branch):
    global ob_branches, sb_branches
    s = symmetries(branch)
    c = len(s)
    ob_branches.update({b:c for b in s})
    sb_branches.add(lexo(branch))
    lengths.update([len(branch)])

  # Split over branches
  if odd_N: # Odd N is solved, so we don't check and have no reason to break
    mid = middle[0] # the intersection of row and column
    for a in range(1, mid-1): # First Queen
      for b in range(a+1, mid): # Second Queen
        branch = ((a,mid),(mid,b))
        include(branch)
    branch = ((mid,mid),) # Intersection (1-orbit case)
    include(branch)
  else:
    def include(branch):
      global ob_branches, sb_branches
      s = symmetries(branch)
      c = len(s)
      ob_branches.update({b:c for b in s})
      sb_branches.add(lexo(branch))
      lengths.update([len(branch)])
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
                  if frozenset(branch) in ob_branches: ...#printout([branch, lexo(branch)],True,True)
                  else: include(branch)
              else:
                for d in range(c+1, limit+1):
                  for rc4 in scanline(d, [rc1, rc2, rc3], [adg, rc2[0]-rc2[1], rc3[0]-rc3[1]]):
                    branch = (rc1, rc2, rc3, rc4)
                    if legal(frozenset(branch)):
                      if frozenset(branch) in ob_branches: ...#printout([branch, lexo(branch)],True,True)
                      else: include(branch)
    # for branch in map(frozenset, product(*rows, *cols)):
    #   if branch not in ob_branches and legal(branch):
    #     s = symmetries(branch)
    #     c = len(s)
    #     ob_branches.update({b:c for b in s})
    #     sb_branches.add(branch)
    #     lengths.update([len(branch)])

  # Compute ob(N), sb(N), and assorted stats
  ob, orbits = len(ob_branches), dict(sorted(multiset(ob_branches.values()).items(), key=lambda o:o[0],reverse=True))
  fundamental = {k: v//k for k,v in orbits.items()}
  sb = sum(fundamental.values())
  quotient = ob/sb if sb else 0
  lengths = dict(lengths)

  # Error logging
  err = []
  expected = (N-1)*(N-3)+1 if odd_N else N**4-22*N**3+201*N**2-883*N+1574 if N >= 8 else ob
  if ob != expected: err.append(f"expected {expected} ob")
  expected = (N-1)*(N-3)//8+1 if odd_N else (N**4-22*N**3+202*N**2-888*N+1584)//8 if N >= 8 else sb
  if sb != expected: err.append(f"expected {expected} sb")
  if sb != len(sb_branches): err.append(f"sb_branches implies {len(sb_branches)} sb")
  if sb != sum(lengths.values()): err.append(f"lengths implies {sum(lengths.values())} sb")
  if len(err): err = ", ".join(err)
  table.append([N, ob, sb, quotient, lengths, orbits, fundamental] + [err]*bool(len(err)))
  sorted_sb_branches = sorted(sorted(str(branch) for branch in map(set, sb_branches)), key=lambda branch: len(branch))
  open(f"./data/verify/branches{N:02d}.txt", mode="w").write("\n".join([f"{N} {sb} {lengths}"]+sorted_sb_branches))

# Discard err column if there were no errors
if all(len(row)==len(table[0])-1 for row in table[1:]):
  table[0] = table[0][:-1]
  print("All green.")
else:
  print("Errors detected.")

# Write out results
open(f"./data/results.txt", mode="w").write(tabulate(table, headers="firstrow", floatfmt=["d","d","d",".3f"]))
