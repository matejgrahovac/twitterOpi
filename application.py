#!/usr/bin/env python3

from flask import Flask, redirect, render_template, request, url_for

import helpers
import os
import sys
from analyzer import Analyzer

app = Flask(__name__)


@app.template_filter()
def number(value):
    return "{:.4f}".format(value)

@app.template_filter()
def time(value):
    value = value[-4:] + ' ' + value[:19]
    return value


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():

    # validate screen_name
    screen_name = request.args.get("screen_name", "")
    if not screen_name:
        return redirect(url_for("index"))

    # get screen_name's tweets
    tweets = helpers.get_user_timeline(screen_name, 200)

    # absolute paths to lists
    positives = os.path.join(sys.path[0], "SentiWS_v1.8c_Positive.txt")
    negatives = os.path.join(sys.path[0], "SentiWS_v1.8c_Negative.txt")
    poENG = os.path.join(sys.path[0], "positive-words.txt")
    neENG = os.path.join(sys.path[0], "negative-words.txt")

    # instantiate analyzer
    analyzer = Analyzer(positives, negatives, poENG, neENG)

    # variables for counting
    positive = 0
    negative = 0

    # analyzing words and adding int to matching variable
    for tweet in tweets:

        tweet['score'] = analyzer.analyze(tweet['tweet'])

        if tweet['score'] > 0.0:
            positive += tweet['score']
        elif tweet['score'] < 0.0:
            negative -= tweet['score']

    # generate chart
    chart = helpers.chart(positive, negative)

    # render results
    return render_template("search.html", chart=chart, screen_name=screen_name, tweets=tweets)



# R. Remus, U. Quasthoff & G. Heyer: SentiWS - a Publicly Available German-language Resource for Sentiment Analysis.
# In: Proceedings of the 7th International Language Ressources and Evaluation (LREC'10), pp. 1168-1171, 2010
