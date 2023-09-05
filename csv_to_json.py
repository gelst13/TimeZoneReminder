import csv
import json
from datetime import datetime
from dateutil.tz import tzoffset


def transform_date_string(date: dict):
    # datetime.datetime(2023, 8, 23, 11, 48, 27, 151924, tzinfo=datetime.timezone.utc)
    zone_info = float(datetime.now().astimezone().strftime('%z')) / 100  # get local offset
    return datetime(year=date['year'], month=date['month'], day=date['day'],
                    hour=12, minute=0, second=0,
                    tzinfo=tzoffset(None, int(zone_info * 3600)))


def csv_to_json(csv_file, json_file):
    json_array = []
    with open(csv_file, newline="", encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=",", quotechar='|')
        for i, row in enumerate(reader):
            # row.loads()['date_posted'] = transform_date_string(row[0].split('/'))
            json_array.append(row)
            date_ = list(map(int, json_array[i]['date_posted'].split('/')))
            print(date_)
            date_dict = {'year': date_[2],
                         'month': date_[1],
                         'day': date_[0]}
            date_datetime_format = transform_date_string(date_dict)
            print(date_datetime_format)
            date_timestamp = datetime.timestamp(date_datetime_format)
            json_array[i]['date_posted'] = date_timestamp

    with open(json_file, 'w', encoding='utf-8') as jsonf:
        json.dump(json_array, jsonf, indent=4)


def print_json(json_file):
    with open(json_file, 'r', encoding='utf-8') as jsonf:
        posts = json.load(jsonf)
    for post in posts:
        print(datetime.fromtimestamp(post['date_posted']))
        print(post['title'])
        print(post['content'])
        print('-----------')


f_in, f_out = 'posts.csv', 'posts.json'
csv_to_json(f_in, f_out)
print_json(f_out)
