import csv
import json
import time
from datetime import datetime, timedelta, timezone


def transform_date_string(date: dict):
    # datetime.datetime(2023, 8, 23, 11, 48, 27, 151924, tzinfo=datetime.timezone.utc)
    zone = timezone(timedelta(seconds=abs(time.timezone)))  # get local offset
    d = datetime(year=date['year'], month=date['month'], day=date['day'],
                 hour=12, minute=0, second=0,
                 tzinfo=zone)
    print(f'constructed aware {d}')
    return d.astimezone(timezone.utc)


def csv_to_json(csv_file, json_file):
    json_array = []
    with open(csv_file, newline="", encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=",", quotechar='|')
        for i, row in enumerate(reader):
            json_array.append(row)
            date_ = list(map(int, json_array[i]['date_posted'].split('/')))
            print(date_)
            date_dict = {'year': date_[2],
                         'month': date_[1],
                         'day': date_[0]}
            date_utc = transform_date_string(date_dict)
            print(f'UTC {date_utc}')
            date_timestamp = date_utc.replace(tzinfo=timezone.utc).timestamp()
            print(date_timestamp)
            print(datetime.fromtimestamp(date_timestamp, timezone.utc))
            print(datetime.fromtimestamp(date_timestamp, tz=timezone(timedelta(seconds=abs(time.timezone)))))
            json_array[i]['date_posted'] = date_timestamp
            print(json_array[i]['date_posted'])
            date_posted_local = datetime.fromtimestamp(json_array[i]['date_posted'],
                                                       tz=timezone(timedelta(seconds=abs(time.timezone))))
            print(date_posted_local)

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


f_in, f_out = 'post.csv', 'posts.json'
csv_to_json(f_in, f_out)
# print_json(f_out)
