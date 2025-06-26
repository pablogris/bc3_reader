# bc3_lib/app/pandas.py
from pathlib import Path

import pandas as pd

from bc3_lib.infra.reader import build_tree
from bc3_lib.app.flatten import nodes_to_rows


def parse_bc3_to_df(path: Path) -> pd.DataFrame:
    """Parsea *path* y devuelve un DataFrame con toda la información."""
    roots = build_tree(path)
    rows = nodes_to_rows(roots)
    return pd.DataFrame.from_records(rows)
