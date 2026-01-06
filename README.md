# FastAPI-ELO-Calculator

Pulls data from fastf1.dev and calculates an ELO for drivers based on various factors.

## Repository Info
- Repo: theaakashb/FastAPI-ELO-Calculator
- Language composition: Python (100%)

## Overview
This project uses the FastF1 library to retrieve Formula 1 timing and telemetry data, then computes ELO ratings for drivers based on configurable factors. A FastAPI service can expose endpoints to query ratings, update inputs, and run recalculations.

## Data Sources and Networking
To allow FastF1 to retrieve data, ensure your firewall permits outbound HTTPS access to:
- https://livetiming.formula1.com (primary for live timing/telemetry)

Depending on your usage for schedules/results, you may also need:
- https://ergast.com
- https://api.jolpica-f1.com

## Getting Started
1. Create and activate a virtual environment
   - macOS/Linux:
     ```
     python -m venv .venv
     source .venv/bin/activate
     ```
   - Windows (PowerShell):
     ```
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the FastAPI app (example):
   ```
   uvicorn app.main:app --reload
   ```
   Adjust the module path to match your project layout.

## Configuration
- Set any environment variables required for FastF1 caching or API behavior.
- Configure ELO calculation parameters (e.g., K-factor, weighting for quali vs race, DNFs, penalties) in your application settings.

## Endpoints (examples)
- `GET /elo/{driver}`: Retrieve the current ELO for a driver
- `POST /elo/recalculate`: Trigger recalculation for a session or season
- `GET /sessions/{year}`: List sessions available for a given year

Note: Actual endpoints depend on how your FastAPI app is structured.

## Development Notes
- FastF1 benefits from a local cache to avoid repeated downloads; ensure the cache directory is writable.
- When running behind a firewall, verify the allowed domains above are reachable.

## License
Add your chosen license here.