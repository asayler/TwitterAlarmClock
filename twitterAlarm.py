import sys
import argparse
import time
import subprocess

import urllib.request as request
import urllib.parse as parse
import json

TIMEOUT = 10 # in seconds

#Uses Version 1.0 of the Twitter Search API: https://dev.twitter.com/docs/api/1/get/search
APIURL     = "http://search.twitter.com/search.json"
MAXQLENGTH = 1000     # Max 1000 for Twitter Search API
RCOUNT     = 100      # Max 100 for Twitter Search API

ENCODING = 'utf-8'
RESULTSKEY = 'results'

EXIT_FAILURE = -1

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

parser = argparse.ArgumentParser(description='Sound alarm when N tweets are detected')
parser.add_argument('query', type=str,
                   help='Twitter search query')
parser.add_argument('count', type=int,
                   help='Tweet threshold to sound alarm (max 99)')

args = parser.parse_args()
query = args.query
threshold = args.count

cnt = 0
while(cnt < threshold):
    time.sleep(TIMEOUT)
    cnt = countTweets(query)
    if(cnt < 0):
        sys.stderr.write("countTweets returned error\n")
        break;
    sys.stdout.write("There are " + str(cnt) + " Tweets that match " + query + "\n")
    sys.stdout.write("Alarm will" + (" " if (cnt > threshold) else " not ") + "sound\n")

if(cnt >= threshold):
    subprocess.call(["aplay", "alarm.wav"])

sys.exit(0)
