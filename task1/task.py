from typing import List, Tuple
import csv
import io

def main(s: str, e: str) -> Tuple[
    List[List[bool]],
    List[List[bool]],
    List[List[bool]],
    List[List[bool]],
    List[List[bool]]
]:
    edges = []
    if s.strip():
        reader = csv.reader(io.StringIO(s))
        for row in reader:
            if len(row) == 2:
                u_str, v_str = row[0].strip(), row[1].strip()
                if u_str and v_str:
                    edges.append((int(u_str), int(v_str)))

    vertices = set(v for edge in edges for v in edge)
    vertices.add(int(e))  
    vertices = sorted(vertices)
    n = len(vertices)
    index = {v: i for i, v in enumerate(vertices)}

    children = {v: [] for v in vertices}
    parent = {v: None for v in vertices}
    for u, v in edges:
        children[u].append(v)
        parent[v] = u

    def get_descendants(v):
        desc = set()
        stack = [v]
        while stack:
            node = stack.pop()
            for c in children[node]:
                if c not in desc:
                    desc.add(c)
                    stack.append(c)
        return desc

    def zero_matrix():
        return [[False] * n for _ in range(n)]

    r1 = zero_matrix()  
    r2 = zero_matrix()  
    r3 = zero_matrix()  
    r4 = zero_matrix()  
    r5 = zero_matrix()  

    for u, v in edges:
        r1[index[u]][index[v]] = True
        r2[index[v]][index[u]] = True  

    for u in vertices:
        desc = get_descendants(u)
        for v in desc:
            if not r1[index[u]][index[v]]:  
                r3[index[u]][index[v]] = True
                r4[index[v]][index[u]] = True

    for p in vertices:
        kids = children[p]
        for i in range(len(kids)):
            for j in range(len(kids)):
                if i != j:
                    c1, c2 = kids[i], kids[j]
                    r5[index[c1]][index[c2]] = True

    return (r1, r2, r3, r4, r5)


if __name__ == "__main__":
    s = "1,2\n1,3\n3,4\n3,5"
    result = main(s, "1")

    names = ["r1", "r2", "r3", "r4", "r5"]
    for name, matrix in zip(names, result):
        print(f"\n{name}:")
        for row in matrix:
            print([int(x) for x in row])