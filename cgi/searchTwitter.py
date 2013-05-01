#!/usr/bin/env python3
import sys
import time
import subprocess
import urllib.request as request
import urllib.parse as parse
import json
import cgi
import cgitb
import html

# Uses Version 1.0 of the Twitter Search API:
# https://dev.twitter.com/docs/api/1/get/search
APIURL     = "http://search.twitter.com/search.json"
MAXQLENGTH = 1000      # Max 1000 for Twitter Search API
RCOUNT     = 100       # Max 100 for Twitter Search API
ENCODING = 'utf-8'
RESULTSKEY = 'results'

def count_tweets(query):
    """Queries the search API and counts the results."""
    query_enc = parse.quote(query)
    if(len(query_enc) > MAXQLENGTH):
        print("Query Too Long", file=sys.stderr)
        return EXIT_FAILURE
    url = APIURL + "?q=" + query_enc + "&rpp=" + str(RCOUNT)
    with request.urlopen(url) as response:
        res_data = response.read()
        res_str = res_data.decode(ENCODING)
        res_obj = json.loads(res_str)
        return len(res_obj[RESULTSKEY])

# enable debugging
cgitb.enable()

pageStart = """
<!DOCTYPE html>

<html>
<body>
<h1>Search Results</h1>
"""

pageEnd = """
<p><a href="start.py">Perform Another Search</a></p>
</body>
</html>
"""
form = cgi.FieldStorage()

user_query = form.getfirst("query")

tweet_count = count_tweets(user_query)

html.escape(user_query)

print("Content-Type: text/html")
print()

print(pageStart)
print("<p>There are " + str(tweet_count) + " tweets related to " + str(user_query) + "</p>")
print(pageEnd)
