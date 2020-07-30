from collections import Counter as multiset
from itertools import product, combinations
from tabulate import tabulate

def main():
  k, MAX_N = 2, 200
  table = [["N", "branches", "reduced", "quotient", "orbits", "fundamental", "err"]]
  for N in range(MAX_N+1):
    B, F, odd_N = multiset(), set(), N%2
    midrc = (0,) if odd_N else (1,-1) # middle rows/cols
    indices = tuple(i for i in range(-(N//2), N//2+1) if i != 0 or odd_N)
    def index(x): return (x-1 if N%2==0 and x >= 1 else x) + N//2 # reverse the conversion from 0..N-1 to -N//2..N//2
    def board(squares): return "\n".join("".join("#" if (x,y) in squares else "-" for x in indices) for y in indices)
    def legal(branch):
      (x,y), (a,b) = branch
      ox, oy, oa, ob = index(x), index(y), index(a), index(b) # return to 0..N-1 range
      return (branch == ((0,0),(0,0))) or (x!=a and y!=b and ox+oy!=oa+ob and ox-oy!=oa-ob)

    for branch in product(product(indices, midrc), product(midrc, indices)) if odd_N else combinations(set(product(indices, midrc)) | set(product(midrc, indices)), 2):
      if frozenset(branch) not in B and legal(branch):
        s = sym(branch)
        c = len(s)
        B.update({b:c for b in s})
        F.add(branch)
        # if not odd_N and c==4:
        #   print(board(branch))
        #   print()
    branches, orbits = len(B), dict(sorted(multiset(B.values()).items(), key=lambda o:o[0], reverse=True))
    fundamental = {k: v//k for k,v in orbits.items()}
    reduced = sum(fundamental.values())
    quotient = branches/reduced if reduced else 0
    
    err = []
    expected = (N-1)*(N-3)+1 if odd_N else 6*N*N - 30*N + 44 if N > 3 else 0
    if branches != expected: err.append(f"expected {expected} branches")
    expected = (N-1)*(N-3)//8+1 if odd_N else N*(3*N-14)//4 + 5 if N > 3 else 0
    if reduced != expected: err.append(f"expected {expected} reduced")
    expected = (N-2)//2
    if not odd_N and N >= 4 and fundamental[4] != expected: err.append(f"expected {expected} 4-fundamentals")
    if len(err): err = ", ".join(err)
    table.append([N, branches, reduced, quotient, orbits, fundamental] + [err]*(len(err)>0))
  for row in table:
    if len(row)>6:
      break
  else:
    table[0] = ["N", "branches", "reduced", "quotient", "orbits", "fundamental"]
  open(f"./data/test.txt", mode="w").write(tabulate(table, headers="firstrow", floatfmt=["d","d","d",".3f"]))

def sym(squares): # from set of squares generate the symmetries as a set of frozen sets
  rx = frozenset((-x,y) for x,y in squares); ry = frozenset((x,-y) for x,y in squares)
  rd = frozenset((y,x) for x,y in squares);  ra = frozenset((-x,-y) for x,y in squares)
  r1 = frozenset((-y,x) for x,y in squares); r2 = frozenset((-y,-x) for x,y in squares)
  r3 = frozenset((y,-x) for x,y in squares); r4 = frozenset(squares)
  return {rx,ry,rd,ra,r1,r2,r3,r4}

if __name__ == "__main__": main()
