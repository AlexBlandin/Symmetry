#!/usr/bin/env python3
from itertools import product
from pathlib import Path

report, green = [""], True
for f in Path("./data/verify/").glob("branches*.txt"):
  lines, branches, m, qcons = open(f).readlines(), set(), {}, True
  N, sb, d = map(eval, lines[0].split(maxsplit=2))
  for s in lines[1:]:
    branch = eval(s)
    branches.add(frozenset(branch))
    if len(branch) not in m: m[len(branch)] = 0
    m[len(branch)] += 1
    board = [[False]*N for _ in range(N)]
    for x,y in branch: board[y-1][x-1]=True
    *boardT, = map(list, zip(*board)) # transpose trick
    for i, row in enumerate(board, 1):
      if len([col for col in row if col]) > 1:
        print(f"{f}: AMO-inconsistent in row {1}, branch: {branch}"); qcons=False
    for i, col in enumerate(boardT, 1):
      if len([row for row in col if row]) > 1:
        print(f"{f}: AMO-inconsistent in col {1}, branch: {branch}"); qcons=False
    diag, adia = set(), set()
    for x,y in product(range(N),range(N)):
      if board[y][x]:
        if (x+y) in diag:
          print(f"{f}: AMO-inconsistent in diag {x+y}, branch: {branch}"); qcons=False
        if (x-y) in adia:
          print(f"{f}: AMO-inconsistent in diag {x-y}, branch: {branch}"); qcons=False
        diag.add(x+y); adia.add(x-y)
  green = green and qcons and len(branches)==sb and m==d
  report.append(f"{f}: N = {N}, sb = {sb}, lengths = {d}, Queens seem {'consistent' if qcons else 'inconsistent'}, sb seems {'consistent' if len(branches)==sb else 'inconsistent'}, lengths seem {'consistent' if m==d else 'inconsistent'}")
report[0] = "All green." if green else "Inconsistency detected."
open("./data/report.txt", mode="w").write("\n".join(report))
