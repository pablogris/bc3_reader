# bc3_lib/domain/node.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Node:
    """Nodo genérico del árbol lógico (capítulo, partida, descompuesto…)."""

    code: str
    description: str
    long_desc: Optional[str] = None
    kind: str = ""             # capitulo, partida, des_mat, …
    unidad: Optional[str] = None
    precio: Optional[float] = None
    can_pres: Optional[float] = None   # cantidad presupuesto
    imp_pres: Optional[float] = None   # importe presupuesto
    measurements: List[str] = field(default_factory=list)
    children: List["Node"] = field(default_factory=list)

    # ───────── helpers ─────────
    def add_child(self, child: "Node") -> None:
        self.children.append(child)

    def compute_total(self) -> None:
        if (
            self.imp_pres is None
            and self.precio is not None
            and self.can_pres is not None
        ):
            self.imp_pres = self.precio * self.can_pres
        for ch in self.children:
            ch.compute_total()
