#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Sudhanshu Mishra'
SITENAME = u'Shortlog'
SITEURL = 'http://www.sudhanshumishra.in'
RELATIVE_URLS = False

TIMEZONE = 'Asia/Kolkata'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_DOMAIN = SITEURL
FEED_RSS = 'feeds/rss'
CATEGORY_FEED_RSS = 'feeds/category.%s.xml'
TAG_FEED_RSS = 'feeds/tag.%s.xml'

DISQUS_SITENAME = 'newgithubpagesblog'
GOOGLE_ANALYTICS = "UA-61714694-1"

POSTS_URL = 'posts/'
POSTS_INDEX_SAVE_AS = 'posts/index.html'

ARTICLE_URL = 'posts/{slug}/'
ARTICLE_SAVE_AS = 'posts/{slug}/index.html'

TAG_URL = 'posts/tags/{slug}/'
TAG_SAVE_AS = 'posts/tags/{slug}/index.html'
TAGS_SAVE_AS = 'posts/tags/index.html'

PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'

FEED_RSS = 'posts/feed/latest'
FEED_ATOM = 'posts/feed/latest.atom'



# Blogroll
LINKS =  (('Old Blog', 'http://blog.sudhanshumishra.in'),
          )

# Social widget
SOCIAL = (('GitHub', 'https://github.com/debugger22'),
          ('Twitter', 'https://twitter.com/debugger22'),
          ('Last.fm', 'http://www.last.fm/user/debugger22'),)

DEFAULT_PAGINATION = 10

PLUGIN_PATH = 'pelican-plugins'
PLUGINS = ['render_math', 'sitemap']
STATIC_PATHS = ['images']

# Plugin configurations

# render_math
MATH_JAX = {'color':'black','align':'center'}


# sitemap
SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 1.0,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'daily',
        'indexes': 'daily',
        'pages': 'daily'
    }
}
