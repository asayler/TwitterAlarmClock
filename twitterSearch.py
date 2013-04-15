import urllib.request as request
import urllib.parse as parse

def searchTweets(query):

    print("Searching for: " + query)
    encQuery = parse.quote(query)
    print("Searching for (encoded): " + encQuery)
    res = request.urlopen("http://search.twitter.com/search.json?q="+encQuery)
    resText = res.read()
    print("Result:\n" + resText.decode('utf-8'))

# we will search tweets about "fc liverpool" football team
searchTweets("#CU_CSFP_RPi")
