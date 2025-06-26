# bc3_lib/__init__.py
"""
Librería BC3 de alto nivel.

API pública:
    • build_tree(Path)       → List[Node]
    • parse_bc3_to_df(Path)  → pandas.DataFrame
"""
from pathlib import Path

from bc3_lib.infra.reader import build_tree
from bc3_lib.app.pandas import parse_bc3_to_df

__all__ = ["build_tree", "parse_bc3_to_df", "Path"]
