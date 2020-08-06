#!/usr/bin/env python3
from pathlib import Path
from parse import *

TRUST_INPUT = False

for f in Path("./data/").glob("branches*.txt"):
  branches, m = set(), {}
  lines = open(f).readlines()
  sb, *d = parse("{:d} {{{:d}:{:d},{:d}:{:d}}}", lines[0]).fixed
  d = dict(zip(d[::2],d[1::2]))
  for s in lines[1:]:
    branch = {}
    if TRUST_INPUT:
      branch = eval(s)
    else:
      branch = parse("{{({:d},{:d}), ({:d},{:d}), ({:d},{:d}), ({:d},{:d})}}", s)
      if branch is None: branch = parse("{{({:d},{:d}), ({:d},{:d}), ({:d},{:d})}}", s)
      if branch is None: branch = parse("{{({:d},{:d}), ({:d},{:d})}}", s)
      if branch is None: branch = parse("{{({:d},{:d})}}", s)
      if branch:
        branch = set(zip(branch.fixed[::2], branch.fixed[1::2]))
    branches.add(frozenset(branch))
    if len(branch) not in m: m[len(branch)] = 0
    m[len(branch)] += 1
  print(f"{f}: sb = {sb}, lengths = {d}. sb seems {'consistent' if len(branches)==sb else 'inconsistent'}. lengths seem {'consistent' if m==d else 'inconsistent'}.")

# # Because python can do this in 4 lines.
# from pathlib import Path
# for f, lines in map(lambda f: (f, open(f).readlines()), Path("./data/").glob("branches*.txt")):
#   branches, sb, d = {frozenset(eval(s)) for s in lines[1:]}, *list(map(eval, lines[0].split(maxsplit=1)))
#   print(f"{f}: sb = {sb}, lengths = {d}. sb seems {'consistent' if len(branches)==sb else 'inconsistent'}. lengths seem {'consistent' if {i:len(list(filter(lambda b:len(b)==i,branches))) for i in range(1,5) if len(list(filter(lambda b:len(b)==i,branches)))}==d else 'inconsistent'}.")