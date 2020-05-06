from estnltk import Text
from collections import defaultdict
from datetime import datetime, timedelta
from dateutil.parser import parse as dtparse
import re

from textblob import TextBlob

from swagger_server.models import EstNerResultDto

months = ["jaanuar", "veebruar", "märts", "aprill", "mai", "juuni", "juuli",
          "august", "september", "oktoober", "november", "detsember"]
month_regex = r"([0-9]?[0-9][.])((0?1)|(0?2)|(0?3)|(0?4)|(0?5)|(0?6)|(0?7)|(0?8)|(0?9)|(10)|(11)|(12))(?:[^0-9])"

def find_est_ner(text_fragments):
    found_named_entities = defaultdict(list)
    for text_fragment in text_fragments:
        text = Text(text_fragment)
        text = text.fix_spelling()

        blob = TextBlob(text_fragment)
        print("detected language:", blob.detect_language())

        for named_entity in list(zip(text.named_entities, text.named_entity_labels)):
            found_named_entities[named_entity[1].lower()].append(named_entity[0])

    joined_fragments = " ".join(text_fragments)
    start, end = get_normalized_start_end(joined_fragments)
    found_named_entities["start"] = start
    found_named_entities["end"] = end

    est_ner_result_dto = EstNerResultDto().from_dict(found_named_entities)
    print("returned est_ner_result_dto:\n", est_ner_result_dto)
    return est_ner_result_dto


def clean_temporal_expressions(text_fragment):
    pattern = re.compile(month_regex)
    # replace month numbers with month names
    text_fragment = pattern.sub(lambda m: m.group(1) + " " + months[int(m.group(2)) - 1] + " ", text_fragment)
    splitted = text_fragment.split()
    for i in range(len(splitted)):
        if ":" in splitted[i]:
            splitted[i] = "kell " + splitted[i]
        if "marts" in splitted[i]:
            splitted[i] = splitted[i].replace('a', 'ä')
    text_fragment = " ".join(splitted)
    print("text_fragment for analysis:", text_fragment)
    return text_fragment


def get_normalized_start_end(text):
    text = clean_temporal_expressions(text)
    text = Text(text)
    text = text.fix_spelling()
    timexes = text.timexes

    try:
        # filter out durations
        timexes = [timex for timex in timexes if timex["type"] != "DURATION"]
        # filter out year only date
        timexes = [timex for timex in timexes if not (timex["type"] == "DATE" and "-" not in timex["value"])]

        start = ""
        end = ""
        if len(timexes) > 1:  # event with a clear duration
            dates = []
            times = []
            for timex in timexes:
                if timex["type"] == "DATE":
                    dates.append(timex["value"])
                elif timex["type"] == "TIME":
                    time = timex["value"]
                    if time.startswith("T"):
                        # no date given, assume today's date
                        todays_date = datetime.today().strftime('%Y-%m-%d')
                        time = todays_date + time
                    times.append(time)

            print("detected dates:", dates)
            print("detected times:", times)

            # convert to datetime objects
            dates = sorted([dtparse(date, dayfirst=False) for date in dates])
            times = sorted([dtparse(time, dayfirst=False) for time in times])

            if len(dates) >= 2 and len(times) >= 2:
                # even if there are more than 2 detected, only use first 2
                # make sure the event is definitely in the future
                todays_date = datetime.today()
                if dates[0].year < todays_date.year:
                    dates[0] = dates[0].replace(year=todays_date.year)
                if dates[1].year < todays_date.year:
                    dates[1] = dates[1].replace(year=todays_date.year)
                # match together dates and times in case times picked up a wrong date
                start = dates[0].replace(hour=times[0].hour).replace(minute=times[0].minute).isoformat()
                end = dates[1].replace(hour=times[1].hour).replace(minute=times[1].minute).isoformat()
            elif len(dates) >= 2 and len(times) == 1:
                # even if there are more than 2 dates detected, only use first 2
                # make sure the event is definitely in the future
                todays_date = datetime.today()
                if dates[0].year < todays_date.year:
                    dates[0] = dates[0].replace(year=todays_date.year)
                if dates[1].year < todays_date.year:
                    dates[1] = dates[1].replace(year=todays_date.year)
                # match together dates and times in case times picked up a wrong date
                start = dates[0].replace(hour=times[0].hour).replace(minute=times[0].minute).isoformat()
                # only one time given, so use it for end time as well
                end = dates[1].replace(hour=times[0].hour).replace(minute=times[0].minute).isoformat()
            elif len(dates) == 1 and len(times) >= 2:
                # even if there are more than 2 times detected, only use first 2
                # make sure the event is definitely in the future
                todays_date = datetime.today()
                if dates[0].year < todays_date.year:
                    dates[0] = dates[0].replace(year=todays_date.year)
                # match together the date with given times in case times picked up a wrong date
                start = dates[0].replace(hour=times[0].hour).replace(minute=times[0].minute).isoformat()
                end = dates[0].replace(hour=times[1].hour).replace(minute=times[1].minute).isoformat()
            elif len(dates) == 1 and len(times) == 1:
                # start date and start time given
                # make sure the event is definitely in the future
                todays_date = datetime.today()
                if dates[0].year < todays_date.year:
                    dates[0] = dates[0].replace(year=todays_date.year)
                # match together date and time in case time picked up a wrong date
                start = dates[0].replace(hour=times[0].hour).replace(minute=times[0].minute)
                # no duration info given, set it to 1 h
                end = start + timedelta(hours=1)
                start = start.isoformat()
                end = end.isoformat()
            elif len(dates) == 0:
                # only times given, make sure the event is definitely in the future
                todays_date = datetime.today()
                if times[0].year < todays_date.year:
                    times[0] = times[0].replace(year=todays_date.year)
                if times[1].year < todays_date.year:
                    times[1] = times[1].replace(year=todays_date.year)
                start = times[0].isoformat()
                end = times[1].isoformat()
            elif len(times) == 0:
                # only dates given, make sure the event is definitely in the future
                todays_date = datetime.today()
                if dates[0].year < todays_date.year:
                    dates[0] = dates[0].replace(year=todays_date.year)
                if dates[1].year < todays_date.year:
                    dates[1] = dates[1].replace(year=todays_date.year)
                start = dates[0].isoformat()
                end = dates[1].isoformat()
                # this is an all-day event, remove time part
                start = start[:start.index("T")]
                end = end[:end.index("T")]
        elif len(timexes) == 1:  # only starting time is given
            timex = timexes[0]
            if timex["type"] == "DATE":
                start = dtparse(timex["value"], dayfirst=False)
                end = dtparse(timex["value"], dayfirst=False)
                # make sure the event is definitely in the future
                todays_date = datetime.today()
                if start.year < todays_date.year:
                    start = start.replace(year=todays_date.year)
                if end.year < todays_date.year:
                    end = end.replace(year=todays_date.year)
                # this is an all-day event, remove time part
                start = start.isoformat()
                start = start[:start.index("T")]
                end = end.isoformat()
                end = end[:end.index("T")]
            elif timex["type"] == "TIME":
                time = timex["value"]
                if time.startswith("T"):
                    # no date given, assume today's date
                    todays_date = datetime.today().strftime('%Y-%m-%d')
                    time = todays_date + time
                start = dtparse(timex["value"], dayfirst=False)
                # no duration info given, set it to 1 h
                end = (dtparse(timex["value"], dayfirst=False) + timedelta(hours=1))
                # make sure the event is definitely in the future
                todays_date = datetime.today()
                if start.year < todays_date.year:
                    start = start.replace(year=todays_date.year)
                if end.year < todays_date.year:
                    end = end.replace(year=todays_date.year)
                start = start.isoformat()
                end = end.isoformat()

        return (start, end)

    except:
        return ("", "")

