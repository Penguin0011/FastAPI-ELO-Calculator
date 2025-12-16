# FastAPI-ELO-Calculator
Pulls data from fastf1.dev and calculates an ELO for drivers based on various factors

# Data is auto cached

# Replay
Replay system works once you install all requirement api's in requirements.txt

# Usage of the replay system.
Run the main script and specify the year and round:

python main.py --year 2025 --round 12
To run a Sprint session (if the event has one), add --sprint:

python main.py --year 2025 --round 12 --sprint
The application will load a pre-computed telemetry dataset if you have run it before for the same event. To force re-computation of telemetry data, use the --refresh-data flag:

python main.py --year 2025 --round 12 --refresh-data
Search Round Numbers (including Sprints)
To find the round number for a specific Grand Prix event, you can use the --list-rounds flag along with the year to return a list of events and their corresponding round numbers:

python main.py --year 2025 --list-rounds
To return a list of events that include Sprint sessions, use the --list-sprints flag:

python main.py --year 2025 --list-sprints
Qualifying Session Replay
To run a Qualifying session replay, use the --qualifying flag:

python main.py --year 2025 --round 12 --qualifying
To run a Sprint Qualifying session (if the event has one), add --sprint:

python main.py --year 2025 --round 12 --qualifying --sprint