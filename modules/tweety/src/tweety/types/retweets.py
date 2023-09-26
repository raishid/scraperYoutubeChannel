from .base import BaseGeneratorClass
from .twDataTypes import User
from ..utils import find_objects


class TweetRetweets(BaseGeneratorClass):
    def __init__(self, tweet_id, client, pages=1, wait_time=2, cursor=None):
        super().__init__()
        self.users = []
        self.cursor = cursor
        self.cursor_top = cursor
        self.is_next_page = True
        self.client = client
        self.tweet_id = tweet_id
        self.pages = pages
        self.wait_time = wait_time

    def __repr__(self):
        return "TweetRetweets(tweet_id={}, count={})".format(
            self.tweet_id,
            len(self.users)
        )

    @staticmethod
    def _get_tweet_content_key(response):
        if str(response['entryId']).split("-")[0] == "user":
            return [response['content']['itemContent']['user_results']['result']]

        return []

    def get_next_page(self):
        _users = []
        if self.is_next_page:
            response = self.client.http.get_tweet_retweets(tweet_id=self.tweet_id, cursor=self.cursor)

            entries = self._get_entries(response)

            for entry in entries:
                users = self._get_tweet_content_key(entry)
                for user in users:
                    try:
                        parsed = User(user, self.client)
                        _users.append(parsed)
                    except:
                        pass

            self.is_next_page = self._get_cursor(response)
            self._get_cursor_top(response)

            for user in _users:
                self.users.append(user)

            self['users'] = self.users
            self['is_next_page'] = self.is_next_page
            self['cursor'] = self.cursor

        return _users

    def __getitem__(self, index):
        if isinstance(index, str):
            return getattr(self, index)

        return self.users[index]

    def __iter__(self):
        for __tweet in self.users:
            yield __tweet

    def __len__(self):
        return len(self.users)
