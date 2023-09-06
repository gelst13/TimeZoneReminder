import json
import time
from datetime import datetime, timedelta, timezone
from blog.models import Post


with open('posts.json') as f:
    posts_json = json.load(f)

for post in posts_json:
    post = Post(title=post['title'], content=post['content'],
                date_posted=datetime.fromtimestamp(post['date_posted'],
                                                   tz=timezone(timedelta(seconds=abs(time.timezone)))))
    post.save()

