b# bc3-lib

> Librería Python para leer ficheros **BC3 / FIEBDC-3**, transformarlos en `pandas.DataFrame` y reutilizarlos en cualquier aplicación (ETL, APIs, comparadores de presupuestos, análisis, etc.).

---

## ✨ Funciones clave

| Función                                           | Descripción                                                                                                                                                                                                       |
| ------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `parse_bc3_to_df(path: Path) -> pandas.DataFrame` | Lee un `.bc3`, construye el árbol de conceptos (capítulo → subcapítulo → partida → descompuesto) y lo convierte en un **DataFrame** con **todas** las columnas relevantes (`codigo`, `tipo`, descripciones, unidad, precio, cantidad, importe, hijos, mediciones…). |
| `build_tree(path: Path) -> list[Node]`            | Devuelve la jerarquía completa como una lista de objetos `Node` si necesitas trabajar a bajo nivel (no depende de *pandas*).                                                                                          |

---

## 📦 Instalación

### Desde GitHub (rama `main`)

```bash
pip install git+https://github.com/pablogris/bc3_reader.git@main
```

Nota: Si publicas tags (v0.1.0, v0.2.0…), puedes cambiar @main por el tag deseado en la URL.

Clonado local (para desarrollo)
Generated bash
git clone https://github.com/pablogris/bc3_reader.git
cd bc3_reader
python -m venv .venv
source .venv/bin/activate     # En Windows: .venv\Scripts\activate
pip install -e .              # Instala el paquete en modo editable
Use code with caution.
Bash
🚀 Uso rápido
Generated python
from pathlib import Path
from bc3_lib import parse_bc3_to_df

# Convierte el fichero BC3 a un DataFrame de pandas
df = parse_bc3_to_df(Path("input/presupuesto.bc3"))

# Inspecciona las primeras filas
print(df.head())

# Exporta el resultado a un CSV
df.to_csv("presupuesto.csv", sep=";", index=False)
Use code with caution.
Python
Columnas principales del DataFrame:
Columna	Significado
tipo	capitulo, partida, des_mat, …
codigo	Código único del concepto.
descripcion_corta, descripcion_larga	Textos descriptivos.
unidad, precio, cantidad_pres, importe_pres	Valores económicos y de medición del presupuesto.
hijos	Códigos de los conceptos hijos, separados por coma.
mediciones	Líneas de medición (~M...) concatenadas por \n.
🛠 Scripts de desarrollo
Dentro del directorio scripts/ encontrarás utilidades no incluidas en la distribución, pensadas para depuración.
scripts/main.py: Vuelca cualquier fichero BC3 a un archivo CSV.
Generated bash
python scripts/main.py input/presupuesto.bc3 output/presupuesto_df.csv
Use code with caution.
Bash
El directorio scripts/ está incluido en .gitignore y no forma parte del paquete distribuible.