import os
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
        a = int(parts[0])
        b = int(parts[1])
        if a <= 0 or b <= 0:
            raise ValueError("bad vertex id")
        out.append((a, b))
    return out


def def_2(edges):
    if not edges:
        return []
    m = 0
    for a, b in edges:
        if a > m:
            m = a
        if b > m:
            m = b
    g = [[0 for _ in range(m)] for _ in range(m)]
    for a, b in edges:
        i = a - 1
        j = b - 1
        g[i][j] = 1
        g[j][i] = 1
    return g


def def_3(p: str):
    with open(p, "r", newline="") as f:
        return f.read()


def main(s: str):
    return def_2(def_1(s))


def task(s: str):
    return main(s)


if __name__ == "__main__":
    p = os.path.join(os.path.dirname(__file__), "task2.csv")
    mat = main(def_3(p))
    for row in mat:
        print(row)