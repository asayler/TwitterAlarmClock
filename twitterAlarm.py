import sys
import urllib.request as request
import urllib.parse as parse
import json

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

query = "@EmWatson" #"#CU_CSFP_RPi"
cnt = countTweets(query)
print("There are " + str(cnt) + " Tweets that match " + query)


