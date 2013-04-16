#!/usr/bin/python3
#
# twitterAlarm.py
#
# By Andy Sayler (www.andysayler.com)
# April 2013
#
# A basic program for counting tweets matching the provided search
# query and triggering the playing of an alarm.wav file when the count
# exceeds the provided threshold
#
# Note: Has some limits (max count of 100, no auth, etc)

# Std Library Imports
import sys
import argparse
import time
import subprocess
import urllib.request as request
import urllib.parse as parse
import json

import pifacedigitalio as pface

# Constants
TIMEOUT = 10 # in seconds
EXIT_FAILURE = -1
EXIT_SUCCESS = 0
# Uses Version 1.0 of the Twitter Search API:
# https://dev.twitter.com/docs/api/1/get/search
APIURL     = "http://search.twitter.com/search.json"
MAXQLENGTH = 1000      # Max 1000 for Twitter Search API
RCOUNT     = 100       # Max 100 for Twitter Search API
ENCODING = 'utf-8'
RESULTSKEY = 'results'

# Globals
p = None
pfd = None

# A function to query the search API and count the results
def countTweets(query):
    queryEnc = parse.quote(query)
    if(len(queryEnc) > MAXQLENGTH):
        sys.stderr.write("Query Too Long")
        return EXIT_FAILURE
    url = APIURL + "?q=" + queryEnc + "&rpp=" + str(RCOUNT)
    res = request.urlopen(url)
    resData = res.read()
    resStr = resData.decode(ENCODING)
    resDec = json.loads(resStr)
    return len(resDec[RESULTSKEY])

# A callback function to snooze the alarm
def snooze(interupt_bit, input_byte):
    sys.stdout.write("Snooooozing...\n")
    p.kill()
    pfd.leds[0].turn_off()
    pfd.leds[1].turn_off()
    pfd.leds[2].turn_off()
    pfd.leds[3].turn_off()
    pfd.leds[4].turn_off()
    pfd.leds[5].turn_off()
    pfd.leds[6].turn_off()
    pfd.leds[7].turn_off()

# Setup Argument Parsing
parser = argparse.ArgumentParser(description='Sound alarm when N tweets are detected')
parser.add_argument('query', type=str,
                   help='Twitter search query')
parser.add_argument('count', type=int,
                   help='Tweet threshold to sound alarm (max 99)')

# Parse Arguments
args = parser.parse_args()
query = args.query
threshold = args.count

# Setup Piface
pface.init()
pfd = pface.PiFaceDigital(0)
ifm = pface.InputFunctionMap()
ifm.register(0, 0, snooze)
ifm.register(1, 0, snooze)
ifm.register(2, 0, snooze)
ifm.register(3, 0, snooze)

# Loop until threshold is reached
cnt = countTweets(query)
while(cnt < threshold):
    time.sleep(TIMEOUT)
    cnt = countTweets(query)
    if(cnt < 0):
        sys.stderr.write("countTweets returned error\n")
        break;
    sys.stdout.write("There are " + str(cnt) + " Tweets that match " + query + "\n")
    sys.stdout.write("Alarm will" + (" not " if (cnt < threshold) else " ") + "sound\n")

# Sound alarm if threshold has been reached
led = 0
if(cnt >= threshold):
    p = subprocess.Popen(["aplay", "alarm.wav"])
    while(p.poll() == None):
        pfd.leds[led].toggle()
        led = (led + 1) % 8
        pface.wait_for_input(ifm, loop=True, timeout=1)
    # Exit on a happy note
    sys.exit(EXIT_SUCCESS)
else:
    # Or not...
    sys.exit(EXIT_FAILURE)
