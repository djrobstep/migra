from pathlib import Path
from time import time

from toml import dumps, loads

PYPROJECT = "pyproject.toml"

p = Path(PYPROJECT)
pyproject = loads(p.read_text())

v = pyproject["tool"]["poetry"]["version"]

parts = v.split(".")[:2]
unix = str(int(time()))

parts.append(unix)

v_with_timestamp = ".".join(parts)
pyproject["tool"]["poetry"]["version"] = v_with_timestamp

p.write_text(dumps(pyproject))
