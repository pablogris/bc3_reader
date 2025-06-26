# bc3_lib/app/flatten.py
"""Helpers para convertir una lista de Node en filas (dict)."""

from __future__ import annotations
from typing import Any, Dict, List

from bc3_lib.domain.node import Node


def _flatten(node: Node, acc: List[Dict[str, Any]]) -> None:
    acc.append(
        {
            "tipo": node.kind,
            "codigo": node.code,
            "descripcion_corta": node.description,
            "descripcion_larga": node.long_desc or "",
            "unidad": node.unidad or "",
            "precio": node.precio if node.precio is not None else "",
            "cantidad_pres": node.can_pres if node.can_pres is not None else "",
            "importe_pres": node.imp_pres if node.imp_pres is not None else "",
            "hijos": ",".join(ch.code for ch in node.children) if node.children else "",
            "mediciones": "⏎".join(node.measurements),
        }
    )
    for ch in node.children:
        _flatten(ch, acc)


def nodes_to_rows(roots: List[Node]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for r in roots:
        _flatten(r, rows)
    return rows
