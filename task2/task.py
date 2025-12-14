from typing import Tuple, Dict, Set
import math
import re
from collections import deque, defaultdict


def def_1(s: str):
    out = []
    if not s or not s.strip():
        return out
    for raw in s.splitlines():
        t = raw.strip()
        if not t:
            continue
        parts = [p for p in re.split(r"[;,\s]+", t) if p]
        if len(parts) < 2:
            continue
        out.append((parts[0], parts[1]))
    return out


def def_2(edges, root: str):
    g: Dict[str, Set[str]] = defaultdict(set)
    nodes: Set[str] = set([root])
    for a, b in edges:
        nodes.add(a)
        nodes.add(b)
        g[a].add(b)
        g[b].add(a)
    ch: Dict[str, Set[str]] = {k: set() for k in nodes}
    pr: Dict[str, Set[str]] = {k: set() for k in nodes}
    q = deque([root])
    seen = set([root])
    while q:
        x = q.popleft()
        for y in g.get(x, set()):
            if y in seen:
                continue
            seen.add(y)
            pr[y].add(x)
            ch[x].add(y)
            q.append(y)
    for k in nodes:
        ch.setdefault(k, set())
        pr.setdefault(k, set())
    return nodes, ch, pr


def def_3(start: str, nxt: Dict[str, Set[str]]):
    out = set()
    stack = list(nxt.get(start, set()))
    while stack:
        x = stack.pop()
        if x in out:
            continue
        out.add(x)
        stack.extend(nxt.get(x, set()))
    return out


def def_4(cnts: Dict[str, Dict[str, int]]):
    n = len(cnts)
    d = n - 1
    if d <= 0:
        d = 1
    h = 0.0
    for m in cnts.values():
        for k in ("r1", "r2", "r3", "r4", "r5"):
            v = m.get(k, 0)
            if v <= 0:
                continue
            p = v / d
            h += -p * (math.log(p) / math.log(2.0))
    return h

def main(s: str, e: str) -> Tuple[float, float]:
    edges = def_1(s)
    nodes, ch, pr = def_2(edges, e)
    cnts = {m: {"r1": 0, "r2": 0, "r3": 0, "r4": 0, "r5": 0} for m in nodes}
    for m in nodes:
        cnts[m]["r1"] = len(ch[m])
        cnts[m]["r2"] = len(pr[m])
    for m in nodes:
        d = def_3(m, ch)
        a = def_3(m, pr)
        cnts[m]["r3"] = len(d) - len(ch[m])
        cnts[m]["r4"] = len(a) - len(pr[m])
    for p in nodes:
        k = len(ch[p])
        if k > 1:
            for u in ch[p]:
                cnts[u]["r5"] += k - 1
    H = def_4(cnts)
    n = len(nodes)
    c = 1.0 / (math.e * math.log(2.0))
    href = c * n * 5 if n > 0 else 1.0
    hn = (H / href) if href > 0 else 0.0
    return round(H, 1), round(hn, 1)

def task(s: str, e: str) -> Tuple[float, float]:
    return main(s, e)

if __name__ == '__main__':
    csv_text = "1,2\n1,3\n2,4\n2,5"
    print(main(csv_text, "1"))