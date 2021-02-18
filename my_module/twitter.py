import tweepy
from my_module.models import DB, Tweet, User
import spacy
import os

twitter_key = os.environ['TWITTER_API_KEY']
twitter_key_secret = os.environ['TWITTER_API_KEY_SECRET']
twitter_auth = tweepy.OAuthHandler(twitter_key, twitter_key_secret)
twitter = tweepy.API(twitter_auth)


nlp = spacy.load('my_model')


def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector


def add_or_update_user(handle):
    try:
        twitter_user = twitter.get_user(handle)
        db_user = (User.query.get(twitter_user.id)) or User(id=twitter_user.id, name=handle)
        DB.session.add(db_user)


        tweets = twitter_user.timeline(
            count=200, exclude_replies=True, include_rts=False, tweet_mode="extended"
        )

        for tweet in tweets:

            vectorized_tweet = vectorize_tweet(tweet.full_text)
            db_tweet = Tweet(id=tweet.id, text=tweet.full_text, vect=vectorized_tweet)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)

    except Exception as e:
        print(e)

    else:
        DB.session.commit()