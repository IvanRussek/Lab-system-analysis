from typing import Tuple, Dict, Set
import math, re
from collections import defaultdict, deque

def _parse_edges(csv_text: str):
    edges = []
    for raw in csv_text.strip().splitlines():
        if not raw.strip():
            continue
        parts = [p for p in re.split(r"[;,\s]+", raw.strip()) if p]
        if len(parts) >= 2:
            edges.append((parts[0], parts[1]))
    return edges

def _orient_as_tree(edges, root: str):
    undirected: Dict[str, Set[str]] = defaultdict(set)
    nodes: Set[str] = set()
    for u, v in edges:
        nodes.update([u, v])
        undirected[u].add(v)
        undirected[v].add(u)
    if root not in nodes:
        nodes.add(root)
    parents: Dict[str, Set[str]] = defaultdict(set)
    children: Dict[str, Set[str]] = defaultdict(set)
    seen = {root}
    q = deque([root])
    while q:
        cur = q.popleft()
        for nb in undirected[cur]:
            if nb not in seen:
                parents[nb].add(cur)
                children[cur].add(nb)
                seen.add(nb)
                q.append(nb)
    for n in nodes:
        parents.setdefault(n, set())
        children.setdefault(n, set())
    return children, parents

def _descendants(node: str, children: Dict[str, Set[str]]):
    res = set()
    stack = list(children[node])
    while stack:
        w = stack.pop()
        if w not in res:
            res.add(w)
            stack.extend(children[w])
    return res

def _ancestors(node: str, parents: Dict[str, Set[str]]):
    res = set()
    stack = list(parents[node])
    while stack:
        w = stack.pop()
        if w not in res:
            res.add(w)
            stack.extend(parents[w])
    return res

def _entropy(l_counts: Dict[str, Dict[str, int]]):
    n = len(l_counts)
    denom = max(1, n - 1)
    H = 0.0
    for m in l_counts.values():
        for r in ("r1", "r2", "r3", "r4", "r5"):
            lij = m.get(r, 0)
            if lij > 0:
                p = lij / denom
                H += -p * math.log(p, 2)
    return H

def main(s: str, e: str) -> Tuple[float, float]:
    edges = list(_parse_edges(s))
    children, parents = _orient_as_tree(edges, e)
    nodes = set(children.keys()) | set(parents.keys())
    n = len(nodes)
    l_counts = {m: {"r1": 0, "r2": 0, "r3": 0, "r4": 0, "r5": 0} for m in nodes}
    
    for m in nodes:
        l_counts[m]["r1"] = len(children[m])
        l_counts[m]["r2"] = len(parents[m])
    
    for m in nodes:
        desc = _descendants(m, children)
        l_counts[m]["r3"] = len(desc) - len(children[m])  
        anc = _ancestors(m, parents)
        l_counts[m]["r4"] = len(anc) - len(parents[m])    

    for p, ch in children.items():
        c = len(ch)
        if c > 1:
            for u in ch:
                l_counts[u]["r5"] += c - 1

    H = _entropy(l_counts)
    c = 1.0 / (math.e * math.log(2.0))
    Href = c * n * 5 if n > 0 else 1.0
    h = H / Href if Href > 0 else 0.0
    return round(H, 1), round(h, 1)

# Алиас для совместимости
def task(s: str, e: str) -> Tuple[float, float]:
    return main(s, e)

if __name__ == '__main__':
    csv_text = "1,2\n1,3\n2,4\n2,5"
    print(main(csv_text, "1"))