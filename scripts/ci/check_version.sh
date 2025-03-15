#!/bin/bash
VERSION_FROM_PYPROJECT=$(grep -oP '(?<=version = ")[^"]+' pyproject.toml)
VERSION_FROM_INIT=$(grep -oP '(?<=__version__ = ")[^"]+' src/vinery/__init__.py)

if [ "$VERSION_FROM_PYPROJECT" != "$VERSION_FROM_INIT" ]; then
  echo "Version mismatch: __version__ in __init__.py ($VERSION_FROM_INIT) does not match pyproject.toml version ($VERSION_FROM_PYPROJECT)."
  exit 1
else
  echo "Version match: $VERSION_FROM_PYPROJECT"
fi
