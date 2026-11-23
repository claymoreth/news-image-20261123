import os
import shutil
from pathlib import Path


def _base_dir():
    bot_dir = os.environ.get("MAKEFUN_BOT_DIR")
    if bot_dir:
        return Path(bot_dir)
    return Path(__file__).resolve().parent


def main():
    base = _base_dir()
    src = base / "entry.jpg"
    if not src.is_file():
        raise FileNotFoundError(f"entry image not found: {src}")
    out_dir = Path("/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, out_dir / "entry.png")


if __name__ == "__main__":
    main()
