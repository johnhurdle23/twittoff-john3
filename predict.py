from sklearn.linear_model import LogisticRegression
from models import User
import numpy as np
from twitter import vectorize_tweet


def predict_user(user1_handle, user2_handle, tweet_text):
    user1 = User.query.filter(User.name == user1_handle).one()
    user2 = User.query.filter(User.name == user2_handle).one()
    user1_vectors = np.array([tweet.vect for tweet in user1.tweets])
    user2_vectors = np.array([tweet.vect for tweet in user2.tweets])
    X = np.vstack([user1_vectors, user2_vectors])
    y = np.concatenate([np.zeros(len(user1.tweets)), np.ones(len(user2.tweets))])
    model = LogisticRegression()
    model.fit(X, y)
    y_pred = model.predict([vectorize_tweet(tweet_text)])
    user_map = {0: user1_handle, 1: user2_handle}
    user_pred = user_map[int(y_pred[0])]
    return user_pred
