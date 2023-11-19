import fire
import json
from icalendar import Calendar, Event
from datetime import datetime, time
from icalendar.prop import vRecur
from pathlib import Path
from dateutil.rrule import rrule, WEEKLY
from dateutil.relativedelta import relativedelta, MO, TU, WE, TH, FR, SA, SU

# Mapping weekdays to dateutil constants
WEEKDAYS = {
    "monday": MO,
    "tuesday": TU,
    "wednesday": WE,
    "thursday": TH,
    "friday": FR,
    "saturday": SA,
    "sunday": SU
}

# Function to parse time string and return time object
def parse_time(time_str):
    return time(int(time_str[:2]), int(time_str[2:4]), int(time_str[4:6]))

# Function to find the next occurrence of a given weekday and combine it with the provided time
def next_weekday_with_time(weekday, time_str):
    day = WEEKDAYS[weekday.lower()]
    now = datetime.now()
    next_day = rrule(WEEKLY, dtstart=now, byweekday=day)[0]
    event_time = parse_time(time_str)
    return datetime.combine(next_day, event_time)

# Function to create an ICS file from JSON data with weekly recurrence
def json_to_ics_with_recurrence(events, ics_filename):
    cal = Calendar()

    for event in events:
        cal_event = Event()
        cal_event.add('summary', event['name'].title())
        start_datetime = next_weekday_with_time(event['day'], event['start']) 
        end_datetime = next_weekday_with_time(event['day'], event['end'])  
        cal_event.add('dtstart', start_datetime)
        cal_event.add('dtend', end_datetime)
        cal_event.add('rrule', vRecur({'FREQ': 'WEEKLY'}))

        cal.add_component(cal_event)

    with open(ics_filename, 'wb') as ics_file:
        ics_file.write(cal.to_ical())

def main(filename: str):
    with open(filename, "r") as f:
        events = json.load(f)

    output_path = Path(filename).with_suffix(".ics")
    assert not output_path.exists()

    json_to_ics_with_recurrence(events, str(output_path))

if __name__ == "__main__":
    fire.Fire(main)

