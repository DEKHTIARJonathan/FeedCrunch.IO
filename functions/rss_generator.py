#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.exceptions import ObjectDoesNotExist

from feedcrunch.models import Post, FeedUser, Option
from feedgen.feed import FeedGenerator

def generateRSS(type="", username=""):
    if type not in ["rss", "atom"]:
        raise ValueError('Wrong Type of RSS Feed given to the generator, only "rss" and "atom" accepted.')

    try:
        user = FeedUser.objects.get(username=username)
    except ObjectDoesNotExist:
        raise ValueError("The requested user ['"+username+"'] doesn't exist.")

    try:
        max_rss_posts = int(Option.objects.get(parameter="max_rss_posts").value)
    except ObjectDoesNotExist:
        raise ValueError("The Option 'max_rss_posts' doesn't exist.")

    ########## ======================================== FEED GENERATION =========================================== ##########

    fg = FeedGenerator()
    fg.id('https://www.feedcrunch.io/@'+username+'/')
    fg.title('Feedcrunch.IO - @' + user.username+ " - " + user.rss_feed_title)
    fg.subtitle(user.description)

    fg.link(href="https://www.feedcrunch.io/", rel='alternate')
    if type=="rss":
        fg.link( href='https://www.feedcrunch.io/@'+username+'/rss/', rel='self', type="application/rss+xml")
    else:
        fg.link( href='https://www.feedcrunch.io/@'+username+'/atom/', rel='self', type="application/atom+xml")

    fg.logo('https://www.feedcrunch.io/static/images/favicon.png')
    fg.icon('https://www.feedcrunch.io/static/images/favicon.png')

    for interest in user.interests.all():
        fg.category(term=interest.name)

    fg.language("en-us")
    fg.rights('cc-by')
    fg.author( {'name':user.get_full_name(),'email':user.email})

    last_post_date = Post.objects.filter(user=user.username).order_by("-when")[:1][0].when
    fg.lastBuildDate(last_post_date)

    # ======== Adding Posts to the Feed ======== #

    listPosts = Post.objects.filter(user=username, activeLink=True).order_by('-id')[:max_rss_posts]

    for post in listPosts:
        fe = fg.add_entry()
        #fe.id(post.link)
        fe.id('https://www.feedcrunch.io/@'+username+'/redirect/'+str(post.id))
        fe.title(post.title)
        fe.summary(post.title)

        """
        fe.content('''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Tamen
            aberramus a proposito, et, ne longius, prorsus, inquam, Piso, si ista
            mala sunt, placet. Aut etiam, ut vestitum, sic sententiam habeas aliam
            domesticam, aliam forensem, ut in fronte ostentatio sit, intus veritas
            occultetur? Cum id fugiunt, re eadem defendunt, quae Peripatetici,
            verba.''', type="CDATA")
        """

        fe.link( href='https://www.feedcrunch.io/@'+username+'/redirect/'+str(post.id), rel='alternate' )
        fe.author({'name':user.get_full_name(),'email':user.email})
        fe.updated(post.when)

        #fe.category([{'term' : 'category', 'scheme': 'http://www.somedomain.com/category', 'label' : 'Category'}])
        for tag in post.tags.all():
            fe.category([{'term' : tag.name}])

    return fg
