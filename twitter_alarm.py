#!/usr/bin/env python3
#
# Twitter Alarm Clock
# twitterAlarm.py
# http://foundation.cs.colorado.edu/rpi/s13/prog1.html
#
# By Andy Sayler (www.andysayler.com)
# April 2013
#
# Updated by Ken Sheedlo (https://github.com/ksheedlo)
# April 2013

# Copyright (c) 2013 Andy Sayler
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
A basic program for counting tweets matching the provided search
query and triggering the playing of an alarm.wav file when the count
exceeds the provided threshold

Note: Has some limits (max count of 100, no auth, etc)
"""

from __future__ import print_function

import sys
import argparse
import time
import subprocess
import urllib.request as request
import urllib.parse as parse
import json

TIMEOUT = 10 # seconds
EXIT_FAILURE = -1
EXIT_SUCCESS = 0
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

def main(argv=None):
    """Module main function."""
    argv = argv or sys.argv[1:]

    # Setup Argument Parsing
    parser = argparse.ArgumentParser(
                            description='Sound alarm when N tweets are detected'
                            )
    parser.add_argument('query', type=str,
                       help='Twitter search query')
    parser.add_argument('count', type=int,
                       help='Tweet threshold to sound alarm (max 99)')

    # Parse Arguments
    args = parser.parse_args(argv)
    query = args.query
    threshold = args.count

    # Loop until threshold is reached
    cnt = count_tweets(query)
    while(cnt < threshold):
        time.sleep(TIMEOUT)
        cnt = count_tweets(query)
        if(cnt < 0):
            print("count_tweets returned error\n", file=sys.stderr)
            break
        print("There are {0} Tweets that match {1}\n".format(str(cnt), query))
        print("Alarm will {0}sound\n".format(
                                            "not " if (cnt < threshold) else ""
                                            ))

    # Sound alarm if threshold has been reached
    if(cnt >= threshold):
        child = subprocess.Popen(["aplay", "alarm.wav"])
        while(child.poll() == None):
            time.sleep(1)
        # Exit on a happy note
        return EXIT_SUCCESS
    else:
        # Or not...
        return EXIT_FAILURE

if __name__ == "__main__":
    sys.exit(main())
