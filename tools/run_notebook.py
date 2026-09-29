"""Execute every code cell of a notebook in order (no Jupyter needed). Used by CI.

    python tools/run_notebook.py code/notebooks/ragkit_tour.ipynb
"""

import io
import json
import os
import sys
from contextlib import redirect_stdout


def main(path: str) -> int:
    nb = json.load(open(path, encoding="utf-8"))
    os.chdir(os.path.dirname(os.path.abspath(path)))
    env = {"__name__": "__main__"}
    n = 0
    for cell in nb["cells"]:
        if cell["cell_type"] != "code":
            continue
        n += 1
        with redirect_stdout(io.StringIO()):
            exec(compile("".join(cell["source"]), f"{path}[cell {n}]", "exec"), env)
    print(f"{path}: {n} code cells executed OK")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
