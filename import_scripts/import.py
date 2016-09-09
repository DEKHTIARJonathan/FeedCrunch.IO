import json
from feedcrunch.models import *

data_file = open('articles.json').read()
data = json.loads(data_file)

tmp_user = FeedUser.objects.get(username="engineering")

for article in data:
  tmp_post = Post.objects.create(title=article['title'], link=article['link'], clicks=article['clicks'], user=tmp_user, activeLink=True, when=article['when'])
  tmp_post.save()