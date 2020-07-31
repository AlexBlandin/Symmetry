from collections import Counter as multiset
from itertools import product, combinations
from tabulate import tabulate

def main():
  k, MAX_N = 2, 20
  table = [["N", "branches", "reduced", "quotient", "orbits", "fundamental", "err"]]
  for N in range(MAX_N+1):
    B, F, odd_N = multiset(), set(), N%2
    indices = tuple(range(1,N+1))
    midrc = (N//2,) if odd_N else (N//2, N//2+1) # middle rows/cols
    def board(squares): return "\n".join("".join("#" if (x,y) in squares else "-" for x in indices) for y in indices)
    def legal(branch):
      for xy, ab in combinations(branch,2):
        if xy != ab:
          x,y, a,b = *xy, *ab
          if x==a or y==b or x+y==a+b or x-y==a-b:
            return False
      return True
    def sym(squares): # from set of squares generate the symmetries as a set of frozen sets
      fs, flip = frozenset, lambda x: N-x-1 # flip from one side to other
      return { fs((flip(x),y) for x,y in squares), fs((x,flip(y)) for x,y in squares),
               fs((y,x) for x,y in squares),       fs((flip(x),flip(y)) for x,y in squares),
               fs((flip(y),x) for x,y in squares), fs((flip(y),flip(x)) for x,y in squares),
               fs((y,flip(x)) for x,y in squares), fs(squares) }

    for branch in map(frozenset, product(product(indices, midrc), product(midrc, indices)) if odd_N else combinations(set(product(indices, midrc)) | set(product(midrc, indices)), 4)):
      if branch not in B and legal(branch):
        s = sym(branch)
        c = len(s)
        B.update({b:c for b in s})
        F.add(branch)
        # if not odd_N and c==4:
        #   print(board(branch))
        #   print()
    ob, orbits = len(B), dict(sorted(multiset(B.values()).items(), key=lambda o:o[0], reverse=True))
    fundamental = {k: v//k for k,v in orbits.items()}
    sb = sum(fundamental.values())
    quotient = ob/sb if sb else 0
    
    err = []
    # expected = (N-1)*(N-3)+1 if odd_N else ob # 6*N*N - 30*N + 44 if N > 3 else 0
    # if ob != expected: err.append(f"expected {expected} ob")
    # expected = (N-1)*(N-3)//8+1 if odd_N else sb # N*(3*N-14)//4 + 5 if N > 3 else 0
    # if sb != expected: err.append(f"expected {expected} sb")
    # expected = (N-2)//2
    # if not odd_N and N >= 4 and fundamental[4] != expected: err.append(f"expected {expected} 4-fundamentals")
    if len(err): err = ", ".join(err)
    table.append([N, ob, sb, quotient, orbits, fundamental] + [err]*(len(err)>0))
  for row in table:
    if len(row)>6:
      break
  else:
    table[0] = ["N", "branches", "reduced", "quotient", "orbits", "fundamental"]
  open(f"./data/test.txt", mode="w").write(tabulate(table, headers="firstrow", floatfmt=["d","d","d",".3f"]))

if __name__ == "__main__": main()
