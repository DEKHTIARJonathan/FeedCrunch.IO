from dataradar.models import Article
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
    fg.id('https://www.dataradar.io/')
    fg.title('DataRadar.IO - Do you have enough data about your #data?')
    fg.description('DataRadar.IO - Do you have enough data about your #data?')
    fg.subtitle('Data Science, Machine Learning, Deep Learning, Big Data and Computer Vision RSS FEED!')

    fg.link(href="https://www.dataradar.io/", rel='alternate')

    if type=="rss":
        fg.link( href='https://www.dataradar.io/rss/', rel='self', type="application/rss+xml")
    else:
        fg.link( href='https://www.dataradar.io/atom/', rel='self', type="application/rss+xml")

    fg.logo('https://www.dataradar.io/favicon.png')
    fg.icon('https://www.dataradar.io/favicon.png')

    fg.category(term='Data Science')
    fg.language("en-us")
    fg.rights('cc-by')
    fg.author( {'name':'Jonathan DEKHTIAR','email':'contact@dataradar.io'})

    fg.lastBuildDate(time_modifier.localize(datetime.now()))

    listArticles = Article.objects.all().order_by('-id')
    for article in listArticles:
        fe = fg.add_entry()
        #fe.id(article.link)
        fe.id('https://www.dataradar.io/article/'+str(article.id))
        fe.title(article.title)
        """
        fe.content('''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Tamen
            aberramus a proposito, et, ne longius, prorsus, inquam, Piso, si ista
            mala sunt, placet. Aut etiam, ut vestitum, sic sententiam habeas aliam
            domesticam, aliam forensem, ut in fronte ostentatio sit, intus veritas
            occultetur? Cum id fugiunt, re eadem defendunt, quae Peripatetici,
            verba.''')
        """
        #fe.summary('Lorem ipsum dolor sit amet, consectetur adipiscing elit...')
        fe.link( href='https://www.dataradar.io/redirect/'+str(article.id), rel='alternate' )
        fe.author( name='Jonathan DEKHTIAR', email='contact@dataradar.io' )
        fe.updated(article.when + time_delta)

    return fg
