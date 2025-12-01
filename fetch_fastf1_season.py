#!/usr/bin/env python3
"""Fetch season and latest livetiming endpoints via fastf1._api and save results.

This script will:
- Use fastf1.get_event_schedule(year) to enumerate events/sessions
- For each session, call a set of fastf1._api endpoint functions using session.api_path
- Save each endpoint's returned DataFrame or JSON to a CSV/JSON file in an output dir
- Produce an index CSV (`season_index.csv`) with one row per endpoint call pointing to the saved file

Notes:
- This can be network-heavy. By default it fetches only sessions where F1 API support
  is available and will skip empty sessions. You can limit the number of events with --max-events.
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import pathlib
import re
import sys
from typing import Any, Dict, List

import pandas as pd

from fastf1 import get_event_schedule, get_session
import fastf1._api as api


def safe_name(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]", "_", s)


def save_dataframe(df: pd.DataFrame, path: pathlib.Path) -> int:
    df.to_csv(path, index=False)
    return len(df)


def save_json(obj: Any, path: pathlib.Path) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, default=str, ensure_ascii=False, indent=2)


ENDPOINTS = [
    'timing_data',
    'timing_app_data',
    'car_data',
    'position_data',
    'track_status_data',
    'session_status',
    'session_status_data',
    'race_control_messages',
    'lap_count',
    'driver_info',
    'weather_data',
]


def fetch_for_session(year: int, round_no: int, event_name: str, session_name: str, out_dir: pathlib.Path) -> List[Dict[str, Any]]:
    recs: List[Dict[str, Any]] = []
    try:
        sess = get_session(year, round_no, session_name)
    except Exception as e:
        logging.exception("Failed to get session %s %s", round_no, session_name)
        return recs

    path = sess.api_path
    logging.info("Session %s - api_path=%s", session_name, path)

    for ep in ENDPOINTS:
        out_name = f"{year}_R{round_no}_{safe_name(event_name)}_{safe_name(session_name)}_{ep}"
        out_file = out_dir / f"{out_name}.csv"
        out_json = out_dir / f"{out_name}.json"
        info = dict(year=year, round=round_no, event=event_name, session=session_name, endpoint=ep, file=None, rows=None, error=None)
        try:
            func = getattr(api, ep, None)
            if func is None:
                info['error'] = 'missing_endpoint'
                recs.append(info)
                continue

            result = func(path)

            # handle known return types
            if isinstance(result, tuple):
                # save each element to a json or csv; combine into json wrapper
                wrapper = {}
                for i, part in enumerate(result):
                    if isinstance(part, pd.DataFrame):
                        p = out_dir / f"{out_name}_part{i}.csv"
                        save_dataframe(part, p)
                        wrapper[f'part{i}'] = str(p)
                    else:
                        wrapper[f'part{i}'] = part
                save_json(wrapper, out_json)
                info['file'] = str(out_json)
                info['rows'] = None
            elif isinstance(result, pd.DataFrame):
                save_dataframe(result, out_file)
                info['file'] = str(out_file)
                info['rows'] = len(result)
            else:
                # fallback: store as json
                save_json(result, out_json)
                info['file'] = str(out_json)

        except Exception as e:
            logging.exception("Error fetching %s for %s", ep, session_name)
            info['error'] = str(e)

        recs.append(info)

    return recs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Fetch fastf1 season and latest data via fastf1._api endpoints")
    parser.add_argument("--year", type=int, default=None, help="Season year (default: current year)")
    parser.add_argument("--out", default="fastf1_season_data", help="Output directory")
    parser.add_argument("--max-events", type=int, default=0, help="Max events to fetch (0=all)")
    parser.add_argument("--only-latest", action='store_true', help="Also produce a 'latest' index for the most recent event")
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    year = args.year if args.year is not None else pd.Timestamp.now().year
    out_dir = pathlib.Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    sched = get_event_schedule(year)
    # filter to events with F1ApiSupport True
    if 'F1ApiSupport' in sched.columns:
        sched = sched[sched['F1ApiSupport'] == True]

    events = sched.itertuples()
    recs_all: List[Dict[str, Any]] = []
    count = 0
    for i, row in enumerate(events):
        if args.max_events and (i >= args.max_events):
            break
        round_no = int(getattr(row, 'RoundNumber'))
        event_name = getattr(row, 'EventName')
        logging.info("Processing event round %s: %s", round_no, event_name)
        # iterate session columns Session1..Session5
        for sidx in range(1, 6):
            sname_col = f'Session{sidx}'
            if sname_col not in sched.columns:
                continue
            sname = getattr(row, sname_col)
            if not sname or str(sname).strip() == 'nan':
                continue
            recs = fetch_for_session(year, round_no, event_name, sname, out_dir)
            recs_all.extend(recs)
        count += 1

    index_df = pd.DataFrame(recs_all)
    index_path = out_dir / 'season_index.csv'
    index_df.to_csv(index_path, index=False)
    logging.info('Wrote index with %d rows to %s', len(index_df), index_path)

    if args.only_latest:
        # find latest event (max RoundNumber) and write a small index
        if not index_df.empty:
            latest_round = index_df['round'].max()
            latest_df = index_df[index_df['round'] == latest_round]
            latest_path = out_dir / 'latest_event_index.csv'
            latest_df.to_csv(latest_path, index=False)
            logging.info('Wrote latest event index to %s', latest_path)

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
