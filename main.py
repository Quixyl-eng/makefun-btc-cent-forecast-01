# Fifteen percent of the way back to the last four hours.
import json
import math
import os
import statistics
from pathlib import Path

WINDOW = 240
PULL = 0.15

def guess(prices):
    last = prices[-1]
    sample = prices[-WINDOW:] if len(prices) >= WINDOW else prices
    mid = statistics.median(sample)
    price = last - PULL * (last - mid)
    if not math.isfinite(price) or not 0 < price < 10000000:
        return last
    return price

src = Path(os.environ.get("MAKEFUN_INPUT_DIR", "/input"))
dst = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
dst.mkdir(parents=True, exist_ok=True)
for path in sorted(src.glob("*.in")):
    case = json.loads(path.read_text())
    prices = case["markets"][0]["prices"]
    out = {"forecasts": [{"case": case["case"], "price": guess(prices)}]}
    (dst / f"{path.stem}.out").write_text(json.dumps(out, separators=(",", ":")))
