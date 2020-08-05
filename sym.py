from collections import Counter as multiset
from itertools import product, combinations
from tabulate import tabulate

def main():
  # Configure
  MIN_N, MAX_N = 8, 20
  PLANAR = True

  table = [["N", "ob(N)", "sb(N)", "quotient", "orbits", "fundamental", "err"]]
  for N in range(MIN_N, MAX_N+1):
    B, F, odd_N = multiset(), set(), N%2
    indices = tuple(i for i in range(-(N//2), N//2+1) if i != 0 or odd_N) if PLANAR else tuple(range(1,N+1))
    midrc = tuple(indices[(N-1)//2 : N//2+1]) # middle rows/cols
    intersection = frozenset(product(midrc, midrc))
    def board(squares): return ["".join("#" if (x,y) in squares else "-" if (x,y) in product(indices,midrc) or (x,y) in product(midrc,indices) else " " for x in indices) for y in indices]
    def legal(branch): return (len(branch) == (2 if odd_N else 4) or (len(branch) == (1 if odd_N else 3) and any(square in intersection for square in branch))) \
                              and all((x,y)==(a,b) or (x!=a and y!=b and x+y!=a+b and x-y!=a-b) for (x,y),(a,b) in combinations(branch,2))
    def sym(squares): # from set of squares generate the symmetries as a set of frozen sets
      return \
      { frozenset((-x,y) for x,y in squares), frozenset((x,-y) for x,y in squares),  frozenset((y,x) for x,y in squares),  frozenset((-x,-y) for x,y in squares),
        frozenset((-y,x) for x,y in squares), frozenset((-y,-x) for x,y in squares), frozenset((y,-x) for x,y in squares), frozenset(squares), } \
      if PLANAR else \
      { frozenset(squares), frozenset((N-x+1,y) for x,y in squares), frozenset((x,N-y+1) for x,y in squares), frozenset((N-x+1,N-y+1) for x,y in squares),
        frozenset(), } # todo: since fs((y,x) for x,y in squares) is wrong I need to figure out the alternative
    
    # temp: 
    # branch = (frozenset(((0, -2), (-3, 0))) if odd_N else frozenset(((-4, -1), (1, -4), (-1, -3), (-3, 1)))) if PLANAR else (frozenset(((1, 4), (4, 2))) if odd_N else frozenset(((1, 4), (3, 5), (4, 2), (5, 6))))
    # s = sym(branch)
    # print(N, tuple(branch))
    # bd = [[] for _ in range(N)]
    # for b in s:
    #   for i,line in enumerate(board(b)):
    #     bd[i].append(line)
    # print("\n".join(" ".join(line) for line in bd))
    # print()
    # exit()

    rows = (product(indices,midrc),) if odd_N else (product(indices,midrc[:1]), product(indices,midrc[1:]))
    cols = (product(midrc,indices),) if odd_N else (product(midrc[:1],indices), product(midrc[1:],indices))
    for branch in map(frozenset, product(*rows, *cols)):
      if branch not in B and legal(branch):
        s = sym(branch)
        c = len(s)
        B.update({b:c for b in s})
        F.add(branch)
    
    ob, orbits = len(B), dict(sorted(multiset(B.values()).items(), key=lambda o:o[0], reverse=True))
    fundamental = {k: v//k for k,v in orbits.items()}
    sb = sum(fundamental.values())
    quotient = ob/sb if sb else 0
    
    err = []
    expected = (N-1)*(N-3)+1 if odd_N else [0,0,0,0,0,0,0,0,206,0, 844,0, 2642,0, 6656,0, 14326,0, 27476,0, 48314][N] if 8 <= N <= 20 else ob # 6*N*N - 30*N + 44 if N > 3 else 0
    if ob != expected: err.append(f"expected {expected} ob")
    expected = (N-1)*(N-3)//8+1 if odd_N else [0,0,0,0,0,0,0,0,30,0, 113,0, 342][N] if 8 <= N <= 12 else sb # N*(3*N-14)//4 + 5 if N > 3 else 0
    if sb != expected: err.append(f"expected {expected} sb")
    if sb != len(F): err.append(f"F implies {len(F)} sb")
    if len(err): err = ", ".join(err)
    table.append([N, ob, sb, quotient, orbits, fundamental] + [err]*(len(err)>0))
  for row in table:
    if len(row)>6: break
  else:
    table[0] = table[0][:-1]
  open(f"./data/test.txt", mode="w").write(tabulate(table, headers="firstrow", floatfmt=["d","d","d",".3f"]))

if __name__ == "__main__": main()
