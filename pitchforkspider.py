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

from pitchforkparser import fetch_and_parse

def main():
    with sqlite3.connect('data/pitchfork_review_data.sqlite') as conn:
        conn.row_factory = sqlite3.Row
        curs = conn.cursor()
        curs.execute('select * from swdata where spotify_uri is NULL and review_text is NULL')
        pf_index = curs.fetchall()
        for pf_entry in pf_index:
            print pf_entry['url']
            try:
                review, spotify_item_uri = fetch_and_parse(pf_entry['url'])
            except Exception, err:
                print "::::unable to fetch from url due to", err
                continue
            curs.execute("UPDATE swdata SET spotify_uri = ?, review_text = ? WHERE url = ?", (spotify_item_uri, review, pf_entry['url']))
        conn.commit()
                
            


if __name__ == '__main__':
    main()

