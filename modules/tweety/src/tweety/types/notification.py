from ..utils import find_objects
from .base import BaseGeneratorClass
from . import *

class TweetNotifications(BaseGeneratorClass):
    def __init__(self, user_id, client, pages=1, wait_time=2, cursor=None):
        super().__init__()
        self.tweets = []
        self.cursor = cursor
        self.cursor_top = cursor
        self.is_next_page = True
        self.client = client
        self.user_id = user_id
        self.pages = pages
        self.wait_time = wait_time

    def get_next_page(self):
        _tweets = []
        if self.is_next_page:

            response = self.client.http.get_tweet_notifications(cursor=self.cursor)
            users = response.get('globalObjects', {}).get('users', {})
            tweets = response.get('globalObjects', {}).get('tweets', {})

            for tweet_id, tweet in tweets.items():
                user = users.get(str(tweet['user_id']))
                user['__typename'] = "User"
                tweet['author'], tweet['rest_id'], tweet['__typename'] = user, tweet_id, "Tweet"

                try:
                    parsed = Tweet(tweet, self.client, response)
                    _tweets.append(parsed)
                except:
                    pass

            self.is_next_page = self._get_cursor(response)
            self._get_cursor_top(response)

            for tweet in _tweets:
                self.tweets.append(tweet)

            self['tweets'] = self.tweets
            self['is_next_page'] = self.is_next_page
            self['cursor'] = self.cursor

        return _tweets

    def __getitem__(self, index):
        if isinstance(index, str):
            return getattr(self, index)

        return self.tweets[index]

    def __iter__(self):
        for __tweet in self.tweets:
            yield __tweet

    def __len__(self):
        return len(self.tweets)