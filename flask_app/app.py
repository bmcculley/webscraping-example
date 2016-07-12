# -*- coding: utf-8 -*-
"""
    Webscraping Example
    ~~~~~~~~~~~~~~~~~~~
    An little example app that outputs either static html or json.
    :copyright: (c) 2016 by bmcculley.
    :license: MIT, see LICENSE for more details.

    select * from articles where id > 10 and id <= 20;
"""

from flask import Flask, Response, request, render_template
from flask import g
import json
import sqlite3

# settings
# how many posts per page
PER_PAGE = 10
# the sqlite database
DATABASE = '/media/blake/36e89c5e-0a94-43d9-bee5-895b7f75f253/web_scraping_tut/flask_app/app/database.db'

app = Flask(__name__, static_url_path='', static_folder='public')
app.add_url_rule('/', 'root', lambda: app.send_static_file('index.html'))


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/home")
def index():
    cur = get_db().cursor()
    next_page = 1
    page_num = int(request.args.get('page', 0))
    if page_num:
        start_row = page_num * PER_PAGE
        end_row = start_row + PER_PAGE
        cur.execute("select * from articles where id > %s and id <= %s"% (start_row, end_row))
        next_page = page_num + 1
    else:
        cur.execute("select * from articles where id <= %s"% PER_PAGE)
    rows = cur.fetchall()
    cur.close()
    prev_page = next_page - 2
    return render_template("home.html", rows=rows, next_page=next_page, prev_page=prev_page)


@app.route("/api", methods=["GET"])
def api_handler():
    cur = get_db().cursor()
    next_page = 1
    page_num = int(request.args.get('page', 0))
    if page_num:
        start_row = page_num * PER_PAGE
        end_row = start_row + PER_PAGE
        cur.execute("select * from articles where id > %s and id <= %s"% (start_row, end_row))
        next_page = page_num + 1
    else:
        cur.execute("select * from articles where id <= %s"% PER_PAGE)
    rows = cur.fetchall()
    cur.close()
    posts = []
    for row in rows:
        post = {}
        post['id'] = row[0]
        post['title'] = row[1]
        post['content'] = row[2]
        posts.append(post)
    return Response(
        json.dumps({'nextPage':next_page, 'posts':posts}),
        mimetype="application/json",
        headers={
            "Cache-Control": "no-cache",
            "Access-Control-Allow-Origin": "*"
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
