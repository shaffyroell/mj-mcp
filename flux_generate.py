#!/usr/bin/env python3
"""Generate images with FLUX via the Black Forest Labs API.

Usage:
    export BFL_API_KEY=...            # get one at https://api.bfl.ai
    python flux_generate.py "a prompt" --n 4 --ar 16:9 --out images/

Environment:
    BFL_API_KEY   Black Forest Labs API key (required)

Notes:
    - Default model is flux-pro-1.1-ultra (best "look"). Override with --model.
    - Each variation is a separate request with a different seed, so you get
      distinct options to choose from.
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

import httpx

API_ROOT = "https://api.bfl.ai/v1"

# aspect ratios BFL ultra accepts as a string; pro-1.1 wants width/height instead
_WH = {
    "1:1": (1024, 1024),
    "16:9": (1344, 768),
    "9:16": (768, 1344),
    "4:3": (1152, 896),
    "3:4": (896, 1152),
    "3:2": (1216, 832),
    "2:3": (832, 1216),
}


def _headers(key: str) -> dict:
    return {"x-key": key, "accept": "application/json", "content-type": "application/json"}


def submit(client: httpx.Client, key: str, model: str, prompt: str, ar: str, seed: int) -> str:
    body: dict = {"prompt": prompt, "seed": seed, "output_format": "png"}
    if "ultra" in model:
        body["aspect_ratio"] = ar
    else:
        w, h = _WH.get(ar, (1024, 1024))
        body["width"], body["height"] = w, h
    r = client.post(f"{API_ROOT}/{model}", headers=_headers(key), json=body, timeout=60)
    r.raise_for_status()
    data = r.json()
    return data["id"], data.get("polling_url")


def poll(client: httpx.Client, key: str, task_id: str, polling_url: str | None) -> str:
    url = polling_url or f"{API_ROOT}/get_result"
    for _ in range(120):  # ~2 min max
        r = client.get(url, headers=_headers(key), params={"id": task_id}, timeout=30)
        r.raise_for_status()
        data = r.json()
        status = data.get("status")
        if status == "Ready":
            return data["result"]["sample"]
        if status in ("Error", "Failed", "Content Moderated", "Request Moderated"):
            raise RuntimeError(f"FLUX job {task_id} ended with status: {status} ({data})")
        time.sleep(1)
    raise TimeoutError(f"FLUX job {task_id} did not complete in time")


def download(client: httpx.Client, img_url: str, dest: Path) -> None:
    r = client.get(img_url, timeout=120)
    r.raise_for_status()
    dest.write_bytes(r.content)


def main() -> int:
    p = argparse.ArgumentParser(description="Generate images with FLUX (Black Forest Labs).")
    p.add_argument("prompt", help="Image prompt (English).")
    p.add_argument("--n", type=int, default=4, help="Number of variations to generate.")
    p.add_argument("--ar", default="16:9", help="Aspect ratio, e.g. 16:9, 1:1, 4:3.")
    p.add_argument("--model", default="flux-pro-1.1-ultra",
                   help="BFL model, e.g. flux-pro-1.1-ultra, flux-pro-1.1.")
    p.add_argument("--out", default="images", help="Output directory.")
    p.add_argument("--seed", type=int, default=1, help="Base seed; variation i uses seed+i.")
    args = p.parse_args()

    key = os.getenv("BFL_API_KEY")
    if not key:
        print("ERROR: BFL_API_KEY is not set. Get a key at https://api.bfl.ai", file=sys.stderr)
        return 2

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    saved = []
    with httpx.Client() as client:
        for i in range(args.n):
            seed = args.seed + i
            print(f"[{i+1}/{args.n}] submitting (seed={seed})...")
            task_id, polling_url = submit(client, key, args.model, args.prompt, args.ar, seed)
            img_url = poll(client, key, task_id, polling_url)
            dest = out / f"variation_{i+1}_seed{seed}.png"
            download(client, img_url, dest)
            saved.append(dest)
            print(f"    saved {dest}")

    print("\nDone. Generated:")
    for s in saved:
        print(f"  {s}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
