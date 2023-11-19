import fire
import json
from icalendar import Calendar, Event
from datetime import datetime
from icalendar.prop import vRecur
from pathlib import Path

# Function to convert time string to datetime object
def convert_time(time_str, day_str):
    return datetime.strptime(day_str + time_str, '%Y%m%d%H%M%S')

# Function to create an ICS file from JSON data with weekly recurrence
def json_to_ics_with_recurrence(events, ics_filename):
    # Create a calendar
    cal = Calendar()

    # Add events to the calendar
    for event in events:
        cal_event = Event()
        cal_event.add('summary', event['name'])
        start_datetime = convert_time(event['start'], '20231122')  # Example date for Wednesday
        end_datetime = convert_time(event['end'], '20231122')      # Example date for Wednesday
        cal_event.add('dtstart', start_datetime)
        cal_event.add('dtend', end_datetime)

        # Set the recurrence rule for weekly repetition
        cal_event.add('rrule', vRecur({'FREQ': 'WEEKLY'}))

        cal.add_component(cal_event)

    # Write the calendar to an ICS file
    with open(ics_filename, 'wb') as ics_file:
        ics_file.write(cal.to_ical())


def main(filename: str):
    with open(filename, "r") as f:
        events = json.load(f)
    
    output_path = Path(filename).with_suffix(".ics")
    assert not output_path.exists()

    # Convert JSON to ICS with weekly recurrence
    json_to_ics_with_recurrence(events, str(output_path))

if __name__ == "__main__":
    fire.Fire(main)
