# bc3_lib/infra/reader.py
"""
Lectura y construcción del árbol lógico a partir de un fichero BC3
(registros ~C|, ~T|, ~D|, ~M|, …).

API:
    • iter_registers(path) – yield BC3Register(tag, fields, raw)
    • build_tree(path)     – devuelve List[Node] (raíces)
"""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterator, List, NamedTuple

from bc3_lib.domain.node import Node
from bc3_lib.utils.text_sanitize import clean_text

ENCODING = "latin-1"
_NUM_RE = re.compile(r"^-?\d+(?:[.,]\d+)?$")


# ───────── registros ───────────────────────────────────────────────────────
class BC3Register(NamedTuple):
    tag: str
    fields: List[str]
    raw: str


def iter_registers(path: Path) -> Iterator[BC3Register]:
    with path.open(encoding=ENCODING, errors="ignore") as fh:
        for line in fh:
            if not line or line.startswith("/*") or not line.startswith("~") or "|" not in line:
                continue
            tag = line[:2]
            _, rest = line.split("|", 1)
            yield BC3Register(tag, rest.rstrip("\n").split("|"), line.rstrip("\n"))


# ───────── árbol lógico ────────────────────────────────────────────────────
def _kind(code: str, t_flag: str) -> str:
    if "##" in code:
        return "supercapitulo"
    if "#" in code:
        return "capitulo"
    return {"0": "partida", "1": "des_mo", "2": "des_maq", "3": "des_mat"}.get(t_flag, "otro")


def _to_float(txt: str) -> float | None:
    return float(txt.replace(",", ".")) if txt and _NUM_RE.match(txt) else None


def build_tree(bc3_path: Path) -> List[Node]:
    nodes: Dict[str, Node] = {}
    parents: Dict[str, str] = {}
    qty_map: Dict[str, float] = {}
    meas_map: Dict[str, List[str]] = defaultdict(list)

    for reg in iter_registers(bc3_path):
        if reg.tag == "~C":              # concepto
            code, unit, desc, price, *_rest = (reg.fields + [""] * 5)[:5]
            type_flag = (reg.fields + ["", "", "", "", "", ""])[5]
            nodes[code] = Node(
                code=code,
                description=clean_text(desc),
                kind=_kind(code, type_flag),
                unidad=unit or None,
                precio=_to_float(price),
            )

        elif reg.tag == "~T":            # texto largo
            code, txt = (reg.fields + [""])[:2]
            if code in nodes and nodes[code].long_desc is None:
                nodes[code].long_desc = clean_text(txt)

        elif reg.tag == "~D":            # descomposición
            parent, child_part = reg.fields[0], "|".join(reg.fields[1:])
            chunks = child_part.split("\\")
            for i in range(0, len(chunks), 3):
                child = chunks[i].strip()
                if not child:
                    continue
                parents[child] = parent
                qty_raw = chunks[i + 2] if i + 2 < len(chunks) else ""
                if _NUM_RE.match(qty_raw):
                    qty_map[child] = float(qty_raw.replace(",", "."))

        elif reg.tag == "~M":            # medición
            body = "|".join(reg.fields[1:])  # quitamos primer campo (~M|?|)
            if "\\" in body:
                code = body.split("\\", 1)[1].split("|", 1)[0]
                meas_map[code].append(reg.raw)

    # jerarquía padre-hijo
    for child, parent in parents.items():
        if child in nodes and parent in nodes:
            nodes[parent].add_child(nodes[child])

    # cantidades y mediciones
    for code, node in nodes.items():
        if code in qty_map:
            node.can_pres = qty_map[code]
        if code in meas_map:
            node.measurements = meas_map[code]
        node.compute_total()

    # raíces (nodos sin padre)
    child_codes = {c.code for n in nodes.values() for c in n.children}
    roots = [n for n in nodes.values() if n.code not in child_codes]
    return sorted(roots, key=lambda n: n.code)
