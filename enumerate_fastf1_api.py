#!/usr/bin/env python3
"""Enumerate callables in fastf1.api and save to a DataFrame/CSV.

This script inspects the `fastf1.api` module to find available functions,
their signatures and a short docstring snippet. It writes the results to
`fastf1_api_endpoints.csv` which you can review before we pull data.

Run:
    python3 enumerate_fastf1_api.py --output fastf1_api_endpoints.csv

"""
from __future__ import annotations

import argparse
import inspect
import logging
from textwrap import shorten

import pandas as pd


def enumerate_api(module) -> pd.DataFrame:
    rows = []
    for name, obj in inspect.getmembers(module):
        if inspect.isfunction(obj) or inspect.ismethod(obj):
            try:
                sig = str(inspect.signature(obj))
            except (ValueError, TypeError):
                sig = "(unknown)"
            doc = inspect.getdoc(obj) or ""
            doc_short = shorten(doc.splitlines()[0] if doc else "", width=200, placeholder="...")
            rows.append({"name": name, "signature": sig, "doc": doc_short, "module": getattr(obj, "__module__", "")})
    df = pd.DataFrame(rows)
    # sort for readability
    df = df.sort_values("name").reset_index(drop=True)
    return df


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Enumerate fastf1.api functions")
    parser.add_argument("--output", default="fastf1_api_endpoints.csv", help="CSV file to write")
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    try:
        import fastf1.api as api
    except Exception as e:
        logging.error("Failed to import fastf1.api: %s", e)
        return 2

    df = enumerate_api(api)
    if df.empty:
        logging.info("No functions found in fastf1.api")
    else:
        df.to_csv(args.output, index=False)
        logging.info("Wrote %d endpoints to %s", len(df), args.output)
        print(df.head(50).to_string(index=False))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
