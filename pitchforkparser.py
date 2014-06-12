#!/usr/bin/env python
# encoding: utf-8
"""
pitchforkparser.py

Created by Benjamin Fields on 2014-06-12.
Copyright (c) 2014 . All rights reserved.
"""

import sys
import os
import requests

from bs4 import BeautifulSoup
from urllib2 import urlparse

def fetch_and_parse(url):
    """parses out the review and the spotify id, if present"""
    r = requests.get(url)
    soup = BeautifulSoup(r.content)
    review = soup.select('div.editorial')[0].text
    spotify_iframe = soup.select('div.spotify')[0].iframe
    spotify_embed_url = urlparse.urlparse(spotify_iframe['src'])
    spotify_item_uri = urlparse.parse_qs(spotify_embed_url.query)['uri'][0]
    return review, spotify_item_uri

def main():
    #really simple test of some spankrock and aphex twin
    for url in ("http://pitchfork.com/reviews/albums/15845-spank-rock-everything-is-boring-and-everyone-is-a-fucking-liar/", "http://pitchfork.com/reviews/albums/225-drukqs/"):
        print fetch_and_parse(url)


if __name__ == '__main__':
    main()

