#!/usr/bin/env python3
from pathlib import Path
from collections import Counter as multiset
from parse import *

TRUST_INPUT = False

for f in Path("./data/").glob("branches*.txt"):
  branches, m = set(), multiset()
  lines = open(f).readlines()
  sb, *d = parse("{:d} {{{:d}:{:d},{:d}:{:d}}}", lines[0]).fixed
  d = dict(zip(d[::2],d[1::2]))
  for s in lines[1:]:
    r = {}
    if TRUST_INPUT:
      r = eval(s)
    else:
      r = parse("{{({:d},{:d}), ({:d},{:d}), ({:d},{:d}), ({:d},{:d})}}", s)
      if r is None: r = parse("{{({:d},{:d}), ({:d},{:d}), ({:d},{:d})}}", s)
      if r is None: r = parse("{{({:d},{:d}), ({:d},{:d})}}", s)
      if r is None: r = parse("{{({:d},{:d})}}", s)
      if r:
        r = set(zip(r.fixed[::2], r.fixed[1::2]))
    branches.add(frozenset(r))
    m.update({len(r):1})
  print(f"{f}: sb = {sb}, lengths = {d}. {'sb seems correct' if len(branches)==sb else 'sb appears inconsistent'}. {'lengths seem correct' if dict(m)==d else 'lengths seem inconsistent'}.")
  