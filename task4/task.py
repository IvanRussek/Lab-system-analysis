from __future__ import annotations
import json
from typing import Any, Dict, List, Tuple, Union

Point = Tuple[float, float]
JsonData = Union[Dict, List, str]

def _load_json_maybe(s: JsonData) -> Any:
    if isinstance(s, str):
        return json.loads(s)
    return s

def _as_terms_map(var_obj: Any, expected_key: str | None = None) -> Dict[str, List[Point]]:
    if isinstance(var_obj, list):
        terms = var_obj
    elif isinstance(var_obj, dict):
        if expected_key is not None and expected_key in var_obj:
            terms = var_obj[expected_key]
        elif len(var_obj) == 1:
            first_value = next(iter(var_obj.values()))
            if isinstance(first_value, list):
                terms = first_value
            else:
                raise ValueError("Single dictionary value must be a list")
        else:
            raise ValueError("Invalid dictionary structure for terms")
    else:
        raise TypeError(f"Unsupported type: {type(var_obj)}")

    out: Dict[str, List[Point]] = {}
    for term in terms:
        if "id" not in term or "points" not in term:
            raise ValueError("Term must contain 'id' and 'points'")
        
        term_id = term["id"]
        pts = [(float(p[0]), float(p[1])) for p in term["points"]]
        pts.sort(key=lambda x: x[0])  
        out[term_id] = pts
    return out

def _mu_piecewise_linear(x: float, points: List[Point]) -> float:
    if x <= points[0][0]:
        return points[0][1]
    if x >= points[-1][0]:
        return points[-1][1]
    
    for i in range(len(points) - 1):
        x0, y0 = points[i]
        x1, y1 = points[i + 1]
        if x0 <= x <= x1:
            if x0 == x1:  
                return min(y0, y1)
            ratio = (x - x0) / (x1 - x0)
            return y0 + ratio * (y1 - y0)
    return 0.0

def _build_universe(terms_map: Dict[str, List[Point]], step: float = 0.01) -> List[float]:
    """Build discrete universe of discourse from term ranges."""
    all_x = [p[0] for pts in terms_map.values() for p in pts]
    lo, hi = min(all_x), max(all_x)
    
    n_steps = int(round((hi - lo) / step))
    universe = [lo + i * step for i in range(n_steps + 1)]
    universe[-1] = hi  
    return universe

def main(
    temperature_json: JsonData,
    heating_json: JsonData,
    rules_json: JsonData,
    current_temperature: float,
) -> float:
    temp_terms = _as_terms_map(_load_json_maybe(temperature_json), "температура")
    heat_terms = _as_terms_map(_load_json_maybe(heating_json), "уровень нагрева")
    rules = [(r[0], r[1]) for r in _load_json_maybe(rules_json)]

    S = _build_universe(heat_terms)

    mu_temp = {
        term: _mu_piecewise_linear(current_temperature, pts)
        for term, pts in temp_terms.items()
    }

    mu_agg = [0.0] * len(S)

    for t_term, h_term in rules:
        activation = mu_temp.get(t_term, 0.0)
        if activation <= 0:
            continue
            
        heat_pts = heat_terms[h_term]
        for i, s_val in enumerate(S):
            heat_mu = _mu_piecewise_linear(s_val, heat_pts)
            combined = min(activation, heat_mu)
            if combined > mu_agg[i]:
                mu_agg[i] = combined

    max_mu = max(mu_agg) if mu_agg else 0.0
    if max_mu <= 0:
        return float(S[0]) if S else 0.0

    for s_val, mu_val in zip(S, mu_agg):
        if abs(mu_val - max_mu) < 1e-9:  
            return float(s_val)

    return float(S[0])