#!/usr/bin/env python
# encoding: utf-8
"""
review_cache_builder.py

flushes any existing critique brainz cache, and rebuild a fresh one.

Created by Benjamin Fields on 2014-06-12.
Copyright (c) 2014 . All rights reserved.
"""

import sys
import os
import sqlite3

import requests


def main():
    review_url = "http://critiquebrainz.org/ws/1/review/?sort=created&offset={offset}"
    with sqlite3.connect('data/pitchfork_review_data.sqlite') as conn:
        conn.row_factory = sqlite3.Row
        curs = conn.cursor()
        curs.execute('DROP TABLE IF EXISTS cbz_review_cache')
        curs.execute('CREATE TABLE cbz_review_cache (rating int,\
         last_updated timestamp,\
         language text,\
         license text,\
         created timestamp,\
         review text,\
         votes_negative int,\
         source_url text,\
         source text,\
         edits int,\
         votes_positive int,\
         user_id text,\
         id text,\
         release_group text,\
         review_class text)')
        offset = 0
        reviews=[1]
        while len(reviews)>0:
            print review_url.format(offset=offset)
            r = requests.get(review_url.format(offset=offset))
            reviews = r.json()['reviews']
            for review in reviews:
                curs.execute("INSERT INTO cbz_review_cache (rating, last_updated, language, license, created, review, votes_negative, source_url, source, edits, votes_positive, user_id, id, release_group, review_class) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (review['rating'],
                 review['last_updated'],#should be timestamp
                 review['language'],
                 review['license']['id'],
                 review['created'],
                 review['text'],
                 review['votes_negative'],
                 review['source_url'],
                 review['source'],
                 review['edits'],
                 review['votes_positive'],
                 review['user_id'],
                 review['id'],
                 review['release_group'],
                 review['review_class']))
            conn.commit()
            offset += 50
            


if __name__ == '__main__':
    main()

