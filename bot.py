import tweepy, threading
from credentials import *
from time import gmtime, strftime
from forismatic import Forismatic

bot_username = 'DailyQuotesFF'
logfile_name = bot_username + ".log"
f = Forismatic()

def create_tweet():
    """ Gets a random quote from Forismatic's API, checks if it fits in a tweet and returns it. """
    text = getQuote()
    while(len(text)>140): #while the length is bigger than the max allowed by Twitter we get another quote.
        text = getQuote()
    return text

def getQuote():
    try:
        q = f.get_quote(lang="en")
        quote = q.quote + "- " + q.author
    except:
        log("There was an error while attempting to get a quote.")
    return quote

def tweet(text):
    """ Tweets using Tweepy, stores a log of what has been tweeted or the error occurred. """
    auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
    auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
    api = tweepy.API(auth)
    try:
        api.update_status(text)
    except tweepy.error.TweepError as e:
        log(e.message)
    else:
        log("Tweeted: " + text)

def log(message):
    """ Creates or updates the logfile. """
    with open(logfile_name, 'a+') as f:
        t = strftime("%d %b %Y %H:%M:%S", gmtime())
        f.write("\n" + t + " " + str(message))

def main():
    threading.Timer(60.0, main).start()
    tweet_text = create_tweet()
    tweet(tweet_text)

if __name__ == "__main__":
    main()
