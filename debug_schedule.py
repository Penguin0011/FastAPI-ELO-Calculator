import fastf1
import logging

logging.basicConfig(level=logging.INFO)

def test_schedule():
    for year in range(2018, 2026):
        try:
            print(f"Testing year {year}...")
            schedule = fastf1.get_event_schedule(year)
            if schedule.empty:
                print(f"Year {year}: Schedule is empty.")
            else:
                print(f"Year {year}: Found {len(schedule)} events.")
        except Exception as e:
            print(f"Year {year}: FAILED - {e}")

if __name__ == "__main__":
    test_schedule()
