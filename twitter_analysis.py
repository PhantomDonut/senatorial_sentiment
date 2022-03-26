import os
import json
from dotenv import load_dotenv
import tweepy
import pandas as pd
from us_state_codes import states
import time

class Politician:
    def __init__(self, name, username, party, state):
        self.name = name
        self.username = username
        self.party = party
        self.state = state
        self.tweets = []

    def __str__(self):
        return f'{self.name} ({self.party}) from {self.state} has {len(self.tweets)} Tweets'

    def string_JSON(self, indent_level):
        return json.dumps({'name':self.name, 'username':self.username, 'party':self.party, 'state':self.state, 'tweets':[tweet.as_JSON(indent_level) for tweet in self.tweets]}, indent=indent_level)

class Tweet_Object:
    def __init__(self, id, text, tweeted_at, public_metrics):
        self.id = id
        self.text = text
        self.tweeted_at = str(tweeted_at)
        self.public_metrics = public_metrics

    def __str__(self):
        return f'Tweet: {self.text}\nTimestamp: {self.tweeted_at}\nLikes: {self.public_metrics["like_count"]}'

    def as_JSON(self, indent_level):
        return json.loads(json.dumps({'id':self.id, 'text':self.text, 'tweeted_at':self.tweeted_at, 'public_metrics':self.public_metrics}, indent=indent_level))

def get_user_tweets(account_username):
    client = tweepy.Client(bearer_token=bearer_token,consumer_key=consumer_key,consumer_secret=consumer_secret,access_token=access_token,access_token_secret=access_token_secret)
    tweet_collection = []

    user = client.get_user(username=account_username)

    maximum_tweets = 400 # Actually evaluates for an extra loop of maximum_tweets + 100
    continue_loop = True
    next_token = None
    tweets_evaluated = 0

    result_cap = 100
    
    while(continue_loop):
        if(next_token):
            user_tweets = client.get_users_tweets(id=user.data.id, exclude='retweets', max_results=result_cap, tweet_fields=["created_at", "public_metrics"], pagination_token=next_token)
        else:
            user_tweets = client.get_users_tweets(id=user.data.id, exclude='retweets', max_results=result_cap, tweet_fields=["created_at", "public_metrics"])

        if tweets_evaluated < maximum_tweets and 'next_token' in user_tweets.meta:
            next_token = user_tweets.meta['next_token']
        else:
            continue_loop = False

        if user_tweets.data is None:
            return tweet_collection

        for tweet in user_tweets.data:
            tweet_collection.append(Tweet_Object(tweet.id, tweet.text, tweet.created_at, tweet.public_metrics))
        tweets_evaluated = tweets_evaluated + 100
    
    return tweet_collection

def generate_tweet_data(dir, handle_file, indent_level = 4):
    party_dict = {'D':'Democrat', 'R':'Republican', 'I':'Independent'}
    handles_df = pd.read_excel(os.path.join(dir, handle_file))
    json_string = '[\n'

    for i in range(0, handles_df.shape[0]):
        # current_pol[0] is Name, [1] is Twitter URL, [2] is State, [3] is Party
        current_pol = handles_df.iloc[i]
        test_politician = Politician(reverse_name(current_pol[0]), split_username(current_pol[1]), party_dict[current_pol[3]], states[str(current_pol[2])])
        test_politician.tweets = get_user_tweets(test_politician.username)
        print(f'i is {i} and {test_politician}')
        json_string = f'{json_string}{test_politician.string_JSON(indent_level)},\n'
    
    return f'{json_string[:-2]}\n]'

def write_to_json(file_path, json_string):
    with open(file_path, 'w') as outfile:
        outfile.write(json_string)

def read_from_json(file_path):
    with open(file_path) as json_file:
        return json.loads(json_file.read())

def reverse_name(last_first):
    return ' '.join(last_first.split(', ')[::-1])

def split_username(full_url):
    return full_url.rpartition('/')[-1]

def main():
    dir = os.path.dirname(os.path.realpath(__file__))
    json_path = os.path.join(dir, 'tweet_data.json')

    write_to_json(json_path, generate_tweet_data(dir, 'congress_twitter_handles.xlsx'))

    #loaded_object = read_from_json(json_path)
    
               
if __name__ == "__main__":
    load_dotenv()
    bearer_token = os.environ.get('BEARER_TOKEN')
    consumer_key = os.getenv('CONSUMER_KEY')
    consumer_secret = os.getenv('CONSUMER_SECRET')
    access_token = os.getenv('ACCESS_TOKEN')
    access_token_secret = os.getenv('ACCESS_SECRET')
    main()