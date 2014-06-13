#!/usr/bin/env python
# encoding: utf-8
"""
forkebrainz.py

Created by Benjamin Fields on 2014-06-12.
Copyright (c) 2014 . All rights reserved.
"""

# all the imports
import os
import sqlite3
import random
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

from IPython import embed

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path,'data/pitchfork_review_data.sqlite'),
    DEBUG=True,
    SECRET_KEY='development key',
                       ))
app.config.from_envvar('FORKED_SETTINGS', silent=True)

common_reviews = {}

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db
    
@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def get_intersection(mbz_id=None):
    """open and load the review intersection set, if it does not yet exist
    if a mbz id is given, return that element or raise if not an intersection
    if no id given, return whole dict"""
    db = get_db()
    if not hasattr(g, 'common_reviews'):
        g.common_reviews = {}
        curs = db.cursor()
        curs.execute("SELECT * FROM pf_cb_map")
        for row in curs.fetchall():
            existing = g.common_reviews.get(row['mbz_rg'], [])
            if existing == None:
                #wtf get wtf
                existing = []
            existing.append({'pf_url':row['pf_id'],
                             'spotify_uri':row['spotify_id'],
                             'cb_id':row['cb_id']})
            g.common_reviews[row['mbz_rg']] = existing
    if mbz_id == None:
        return g.common_reviews
    else:
        return g.common_reviews[mbz_id]
        
@app.route('/') 
def home():
    db = get_db()
    return render_template('index.html')

@app.route('/reviewsfor/<mbz_id>')
def reviews_for(mbz_id):
    print mbz_id
    db = get_db()
    # try:
    reviews = get_intersection(mbz_id)
    # except KeyError, err:
    #     print "could not find mbz_id", err, "when looking for", mbz_id
    #     abort(404)
    review = random.sample(reviews,1)[0]
    pf_url = review['pf_url']
    sp_uri = review['spotify_uri']
    cb_review = review['cb_id']
    print mbz_id, "gives", pf_url, sp_uri
    
    curs = db.cursor()
    curs.execute("SELECT * FROM swdata WHERE url = ?", (pf_url,))
    pf_review = dict(curs.fetchone())
    curs.execute("SELECT * FROM cbz_review_cache WHERE id = ?",
                 (cb_review,))
    cb_review =dict(curs.fetchone()) #need to strip formatting out of this one
    return render_template('two_reviews.html', cb_review=cb_review, pf_review=pf_review, sp_uri=sp_uri)
    
@app.route('/judgement')
def judgement():
    mbz_id = random.sample(get_intersection().keys(), 1)[0]
    print mbz_id
    db = get_db()
    # try:
    reviews = get_intersection(mbz_id)
    # except KeyError, err:
    #     print "could not find mbz_id", err, "when looking for", mbz_id
    #     abort(404)
    review = random.sample(reviews,1)[0]
    pf_url = review['pf_url']
    sp_uri = review['spotify_uri']
    cb_review = review['cb_id']
    print mbz_id, "gives", pf_url, sp_uri
    
    curs = db.cursor()
    curs.execute("SELECT * FROM swdata WHERE url = ?", (pf_url,))
    pf_review = dict(curs.fetchone())
    curs.execute("SELECT * FROM cbz_review_cache WHERE id = ?",
                 (cb_review,))
    cb_review =dict(curs.fetchone()) #need to strip formatting out of this one
    
    which_pf = random.sample(('a', 'b'), 1)[0]
    if which_pf == 'a':
        review_text_a = pf_review['review_text']
        review_text_b = cb_review['review']
    else:
        review_text_a = cb_review['review']
        review_text_b = pf_review['review_text']
    max_len = min(len(review_text_a), len(review_text_b))
    if len(review_text_a) > max_len:
        review_text_a = review_text_a[:max_len] + "..."
    if len(review_text_b) > max_len:
        review_text_b = review_text_b[:max_len] + "..."
    session['which_pf'] = which_pf
    session['pitchfork'] = dict(pf_review)
    session['cb'] = dict(cb_review)
    return render_template('judgement.html', cb_review=cb_review, pf_review=pf_review, sp_uri=sp_uri, review_text_a=review_text_a, review_text_b=review_text_b)
    
@app.route('/eval', methods=["POST"])
def evaluate():
    submitted_answer = request.form['picked_review']
    correct_answer = session['which_pf']
    if submitted_answer == correct_answer:
        result = "CORRECT!"
    else:
        result = "WRONG!"
    # pf_review = session['pitchfork']
    # cb_review = session['cb']
    return render_template('eval.html', result=result)
    
if __name__ == '__main__':
  app.run(debug=True)

