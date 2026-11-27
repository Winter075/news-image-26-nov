"""Grader entrypoint: place the committed news poster at /output/entry.png."""

from os import environ
from pathlib import Path


def hand_in_poster():
    root = Path(__file__).parent.resolve()
    picture = root / "entry.png"
    if not picture.is_file():
        raise SystemExit("entry.png was not committed")
    destination = Path(environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    destination.mkdir(exist_ok=True, parents=True)
    (destination / "entry.png").write_bytes(picture.read_bytes())


hand_in_poster()
