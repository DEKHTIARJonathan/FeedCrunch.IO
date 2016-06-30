# -*- coding: utf-8 -*-
from feedcrunch.models import Post
from feedgen.feed import FeedGenerator

from datetime import datetime
from pytz import timezone

time_modifier = timezone('Europe/Paris')
now = datetime.now()
time_delta = time_modifier.utcoffset(now)

def generateRSS(type=""):
    if type not in ["rss", "atom"]:
        raise ValueError('Wrong Type of RSS Feed given to the generator, only "rss" and "atom" accepted.')
    fg = FeedGenerator()
    fg.id('https://www.feedcrunch.io/')
    fg.title('feedcrunch.IO - Do you have enough data about your #data?')
    fg.description('feedcrunch.IO - Do you have enough data about your #data?')
    fg.subtitle('Data Science, Machine Learning, Deep Learning, Big Data and Computer Vision RSS FEED!')

    fg.link(href="https://www.feedcrunch.io/", rel='alternate')

    if type=="rss":
        fg.link( href='https://www.feedcrunch.io/rss/', rel='self', type="application/rss+xml")
    else:
        fg.link( href='https://www.feedcrunch.io/atom/', rel='self', type="application/rss+xml")

    fg.logo('https://www.feedcrunch.io/static/images/favicon.png')
    fg.icon('https://www.feedcrunch.io/static/images/favicon.png')

    fg.category(term='Data Science')
    fg.language("en-us")
    fg.rights('cc-by')
    fg.author( {'name':'Jonathan DEKHTIAR','email':'contact@feedcrunch.io'})

    fg.lastBuildDate(time_modifier.localize(datetime.now()))

    listPosts = Post.objects.all().order_by('-id')
    for post in listPosts:
        fe = fg.add_entry()
        #fe.id(post.link)
        fe.id('https://www.feedcrunch.io/post/'+str(post.id))
        fe.title(post.title)
        """
        fe.content('''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Tamen
            aberramus a proposito, et, ne longius, prorsus, inquam, Piso, si ista
            mala sunt, placet. Aut etiam, ut vestitum, sic sententiam habeas aliam
            domesticam, aliam forensem, ut in fronte ostentatio sit, intus veritas
            occultetur? Cum id fugiunt, re eadem defendunt, quae Peripatetici,
            verba.''')
        """
        #fe.summary('Lorem ipsum dolor sit amet, consectetur adipiscing elit...')
        fe.link( href='https://www.feedcrunch.io/redirect/'+str(post.id), rel='alternate' )
        fe.author( name='Jonathan DEKHTIAR', email='contact@feedcrunch.io' )
        fe.updated(post.when + time_delta)

    return fg
