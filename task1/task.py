from typing import List, Tuple
import re


def def_1(s: str):
    if not s or not s.strip():
        return []
    out = []
    for raw in s.splitlines():
        t = raw.strip()
        if not t:
            continue
        parts = [p for p in re.split(r"[,\s;]+", t) if p]
        if len(parts) < 2:
            continue
        out.append((int(parts[0]), int(parts[1])))
    return out


def def_2(edges, e: int):
    vs = set()
    for a, b in edges:
        vs.add(a)
        vs.add(b)
    vs.add(int(e))
    vs = sorted(vs)
    ix = {v: i for i, v in enumerate(vs)}
    return vs, ix


def def_3(n: int):
    return [[False for _ in range(n)] for _ in range(n)]


def def_4(vs, edges):
    ch = {v: [] for v in vs}
    pr = {v: [] for v in vs}
    for a, b in edges:
        ch[a].append(b)
        pr[b].append(a)
    return ch, pr


def def_5(start, ch):
    seen = set()
    stack = list(ch[start])
    while stack:
        x = stack.pop()
        if x in seen:
            continue
        seen.add(x)
        stack.extend(ch[x])
    return seen


def main(s: str, e: str) -> Tuple[
    List[List[bool]],
    List[List[bool]],
    List[List[bool]],
    List[List[bool]],
    List[List[bool]],
]:
    edges = def_1(s)
    vs, ix = def_2(edges, int(e))
    n = len(vs)
    r1 = def_3(n)
    r2 = def_3(n)
    r3 = def_3(n)
    r4 = def_3(n)
    r5 = def_3(n)
    ch, pr = def_4(vs, edges)
    for a, b in edges:
        r1[ix[a]][ix[b]] = True
        r2[ix[b]][ix[a]] = True
    for a in vs:
        d = def_5(a, ch)
        ia = ix[a]
        for b in d:
            ib = ix[b]
            if not r1[ia][ib]:
                r3[ia][ib] = True
                r4[ib][ia] = True
    for p in vs:
        kids = ch[p]
        k = len(kids)
        if k < 2:
            continue
        for i in range(k):
            for j in range(k):
                if i != j:
                    r5[ix[kids[i]]][ix[kids[j]]] = True
    return (r1, r2, r3, r4, r5)


if __name__ == "__main__":
    s = "1,2\n1,3\n3,4\n3,5"
    result = main(s, "1")
    names = ["r1", "r2", "r3", "r4", "r5"]
    for name, matrix in zip(names, result):
        print(f"\n{name}:")
        for row in matrix:
            print([int(x) for x in row])