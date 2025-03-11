from vineyard.cli import cli
from pathlib import Path

Path("./outputs").mkdir(parents=True, exist_ok=True)
Path("/tmp/vineyard").mkdir(parents=True, exist_ok=True)

if __name__ == '__main__':
    cli()
