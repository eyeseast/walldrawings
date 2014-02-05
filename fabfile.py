import datetime
import os

from fabric.api import *
from slugify import slugify as _slugify

POST_TEMPLATE = """\
---
title: "{title}"
layout: post
published: true
comments: false
tags: []
scripts: []
styles: []
excerpt: "tl;dr"
---
"""

ROOT = os.path.realpath(os.path.dirname(__file__))
_f = lambda fn: os.path.join(ROOT, fn)

class _DoingItWrong(Exception):
    """
    Catch-all for breaking things
    """
    pass


def post(title='', format='markdown'):
    """
    Create a new stub post
    """
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    slug = _slugify(title)
    filename = _f("_posts/{0}-{1}.{2}".format(date, slug, format))
    if not os.path.exists(filename):
        with open(filename, 'wb') as f:
            content = POST_TEMPLATE.format(title=title)
            f.write(content.encode('utf-8'))
    else:
        raise _DoingItWrong('That post already exists!')


def publish():
    """
    Push to Github Pages
    """
    local('git push origin master')
    local('git push origin master:gh-pages')

