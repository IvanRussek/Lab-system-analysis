import json
import re
from functools import cmp_to_key


def def_1(s: str):
    t = re.sub(r",\s*]", "]", s)
    try:
        a = json.loads(t)
    except json.JSONDecodeError:
        a = json.loads(s)
    out = []
    for x in a:
        if isinstance(x, list):
            out.append(x)
        else:
            out.append([x])
    return out


def def_2(r):
    s = set()
    for cl in r:
        for x in cl:
            s.add(x)
    return s


def def_3(r, all_items):
    pos = {}
    for i, cl in enumerate(r):
        for x in cl:
            pos[x] = i
    n = len(all_items)
    y = [[0] * n for _ in range(n)]
    for i in range(n):
        a = all_items[i]
        ra = pos.get(a, None)
        if ra is None:
            continue
        for j in range(n):
            b = all_items[j]
            rb = pos.get(b, None)
            if rb is None:
                continue
            y[i][j] = 1 if rb >= ra else 0
    return y


def def_4(m):
    n = len(m)
    return [[m[j][i] for j in range(n)] for i in range(n)]


def def_5(a, b):
    n = len(a)
    return [[1 if (a[i][j] and b[i][j]) else 0 for j in range(n)] for i in range(n)]


def def_6(a, b):
    n = len(a)
    return [[1 if (a[i][j] or b[i][j]) else 0 for j in range(n)] for i in range(n)]


def def_7(m):
    n = len(m)
    r = [row[:] for row in m]
    for k in range(n):
        rk = r[k]
        for i in range(n):
            if not r[i][k]:
                continue
            ri = r[i]
            for j in range(n):
                if rk[j]:
                    ri[j] = 1
    return r


def def_8(x):
    return (isinstance(x, str), str(x))


def main(json_a: str, json_b: str) -> str:
    ra = def_1(json_a)
    rb = def_1(json_b)
    all_items = sorted(list(def_2(ra) | def_2(rb)))
    n = len(all_items)
    idx = {x: i for i, x in enumerate(all_items)}
    ya = def_3(ra, all_items)
    yb = def_3(rb, all_items)
    yat = def_4(ya)
    ybt = def_4(yb)
    yab = def_5(ya, yb)
    yabt = def_5(yat, ybt)
    p = def_6(yab, yabt)

    c = [[yab[i][j] for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            if p[i][j] == 0:
                c[i][j] = 1
                c[j][i] = 1

    e = def_5(c, def_4(c))
    es = def_7(e)

    clusters = []
    used = [False] * n
    for i in range(n):
        if used[i]:
            continue
        group = [k for k in range(n) if es[i][k] == 1]
        for k in group:
            used[k] = True
        items = [all_items[k] for k in group]
        items.sort(key=def_8)
        clusters.append(items)

    def def_9(a, b):
        ia = idx[a[0]]
        ib = idx[b[0]]
        ab = c[ia][ib]
        ba = c[ib][ia]
        if ab == 1 and ba == 0:
            return -1
        if ab == 0 and ba == 1:
            return 1
        return 0

    clusters.sort(key=cmp_to_key(def_9))

    out = []
    for cl in clusters:
        if len(cl) == 1:
            out.append(cl[0])
        else:
            out.append(cl)
    return json.dumps(out, ensure_ascii=False)


if __name__ == "__main__":
    json_a = "[1,[2,3],4,[5,6,7],8,9,10]"
    json_b = "[[1,2],[3,4,5],6,7,9,[8,10]]"
    result = main(json_a, json_b)
    print(result)


