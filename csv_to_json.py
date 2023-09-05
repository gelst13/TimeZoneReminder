import csv
import json


def csv_to_json(csv_file, json_file):
    json_array = []
    with open(csv_file, newline="", encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter=",", quotechar='|')
        for row in reader:
            json_array.append(row)

    with open(json_file, 'w', encoding='utf-8') as jsonf:
        json.dump(json_array, jsonf, indent=4)


def print_json(json_file):
    with open(json_file, 'r', encoding='utf-8') as jsonf:
        posts = json.load(jsonf)
    for post in posts:
        for key in post:
            print(post[key])
        print('-----------')


f_in, f_out = 'posts.csv', 'posts.json'
csv_to_json(f_in, f_out)
print_json(f_out)
