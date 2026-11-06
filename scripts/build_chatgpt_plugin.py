#!/usr/bin/env python3
"""Build a portable skills-only ChatGPT plugin ZIP from this exact repository checkout.

Standard-library only; embeds the project's existing deterministic Python code.
No credentials, exchange data or network calls.
"""
from __future__ import annotations
import argparse
import json
import shutil
import struct
import subprocess
import sys
import tempfile
import zlib
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "plugin"
MANIFEST = json.loads((TEMPLATE / "plugin.json").read_text(encoding="utf-8"))
SKILLS = list((TEMPLATE / "skills").iterdir())
assert len(SKILLS) == 1 and (SKILLS[0] / "SKILL.md").is_file()
SKILL = SKILLS[0].name
PACKAGE = "candleaudit" if MANIFEST["name"] == "candleaudit" else "candlebacktest_ai"
assert PACKAGE == "candleaudit" or MANIFEST["name"] == "candlebacktest-ai"
OUTPUT = ROOT / "dist" / (MANIFEST["name"] + "-chatgpt-skill-v" + MANIFEST["version"] + ".zip")


def png_icon() -> bytes:
    """Small original RGBA candlestick icon, encoded without extra dependencies."""
    w = h = 128
    primary = (29, 96, 94, 255) if PACKAGE == "candleaudit" else (40, 67, 134, 255)
    pixels = bytearray()
    candles = [(29, 73, 91), (47, 52, 78), (65, 42, 69), (83, 25, 54), (101, 34, 59)]
    for y in range(h):
        pixels.extend(b"\x00")
        for x in range(w):
            c = primary
            for cx, top, low in candles:
                if (abs(x - cx) <= 2 and top - 8 <= y <= low + 6) or (abs(x - cx) <= 7 and top <= y <= low):
                    c = (160, 240, 213, 255)
            pixels.extend(bytes(c))
    def chunk(tag, payload):
        return struct.pack(">I", len(payload)) + tag + payload + struct.pack(">I", zlib.crc32(tag + payload) & 0xffffffff)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(bytes(pixels), 9)) + chunk(b"IEND", b"")


def build():
    OUTPUT.parent.mkdir(exist_ok=True)
    with ZipFile(OUTPUT, "w", compression=ZIP_DEFLATED, compresslevel=9) as out:
        for file in sorted(TEMPLATE.rglob("*")):
            if file.is_file() and "__pycache__" not in file.parts:
                out.write(file, file.relative_to(TEMPLATE).as_posix())
        out.writestr("assets/logo.png", png_icon())
        src = ROOT / "src" / PACKAGE
        for file in sorted(src.rglob("*")):
            if file.is_file() and "__pycache__" not in file.parts and file.suffix != ".pyc":
                out.write(file, f"skills/{SKILL}/runtime/src/{PACKAGE}/" + file.relative_to(src).as_posix())
        for file in sorted((ROOT / "examples").rglob("*")):
            if file.is_file():
                out.write(file, f"skills/{SKILL}/runtime/examples/" + file.relative_to(ROOT / "examples").as_posix())
        docs = (
            {"README.md": "README.md", "docs/design.md": "verification.md"}
            if PACKAGE == "candleaudit" else
            {"README.md": "README.md", "docs/EXECUTION_AND_SCHEMA.md": "SCHEMA.md", "docs/EXTERNAL_AI_PROMPT_FA.md": "STRATEGY_PROMPT_FA.md"}
        )
        for src_name, target in docs.items():
            out.write(ROOT / src_name, f"skills/{SKILL}/docs/{target}")
    print("CREATED", OUTPUT, OUTPUT.stat().st_size, "bytes")


def smoke():
    with tempfile.TemporaryDirectory(prefix="plugin_smoke_") as folder:
        folder = Path(folder)
        with ZipFile(OUTPUT) as z:
            bad = [x for x in z.namelist() if x.startswith("/") or ".." in Path(x).parts]
            assert not bad, bad
            z.extractall(folder)
        p = folder / "skills" / SKILL / "run.py"
        a = folder / "skills" / SKILL / "runtime" / "examples"
        if PACKAGE == "candleaudit":
            cmd = [sys.executable, str(p), "candles", str(a / "candles_clean.csv"), "--interval", "4h"]
        else:
            cmd = [sys.executable, str(p), "run", "--strategy", str(a / "ema_cross.json"),
                   "--candles", str(a / "candles_synthetic_4h.csv")]
        result = subprocess.run(cmd, cwd=folder, capture_output=True, text=True, timeout=30)
        if result.returncode:
            raise RuntimeError("Smoke FAIL: " + result.stderr + result.stdout[:1000])
        print("SMOKE PASS:", PACKAGE)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true", help="also execute bundled CLI with synthetic data")
    args = parser.parse_args()
    build()
    if args.smoke:
        smoke()
