import json
import datetime
import pytz
import time
# from datetime import datetime, timedelta, timezone
from blog.models import Post


def date_from_str(date_posted: str):
    year = int(date_posted[6:10])
    month = int(date_posted[3:5])
    day = int(date_posted[:2])
    hour = int(date_posted[11:13])
    minute = int(date_posted[14:16])
    return datetime.datetime(year, month, day, hour, minute, tzinfo=pytz.utc)


with open('posts.json') as f:
    posts_json = json.load(f)

for post in posts_json:
    # post = Post(title=post['title'], content=post['content'],
    #             date_posted=datetime.fromtimestamp(post['date_posted'],
    #                                                tz=timezone(timedelta(seconds=abs(time.timezone)))))
    #
    post = Post(title=post['title'], content=post['content'],
                date_posted=date_from_str(post['date_posted']))

    post.save()




