import pandas as pd
import os
import regex as re
from nltk.sentiment import SentimentIntensityAnalyzer
import twitter_analysis
import datetime
import numpy as np

def compile_tweet_sentiments(dir, politician_collection):
    sia = SentimentIntensityAnalyzer()
    
    tweet_database = []
    politician_database = []
    
    for i in range(0, len(politician_collection)):
        politician = politician_collection[i]
        overall_statistics = np.array([0, 0, 0, 0, 0])

        for tweet in politician['tweets']:
            cleaned_tweet = re.sub(r'http\S+', '', tweet['text'])
            sentiment = sia.polarity_scores(cleaned_tweet)
            tweet_database.append({'Politician':politician['name'],'Party':politician['party'],'State':politician['state'],\
            'Negative Sentiment':sentiment['neg'],'Neutral Sentiment':sentiment['neu'],'Positive Sentiment':sentiment['pos'],'Compound':sentiment['compound'],\
            'Date':datetime.datetime.fromisoformat(tweet['tweeted_at']).strftime('%m/%d/%Y'),'Likes':tweet['public_metrics']['like_count']})
            overall_statistics = np.add(overall_statistics, np.array([tweet_database[-1]['Negative Sentiment'], tweet_database[-1]['Neutral Sentiment'], tweet_database[-1]['Positive Sentiment'], tweet_database[-1]['Compound'], tweet_database[-1]['Likes']]))

        overall_statistics = overall_statistics / len(politician['tweets'])
        politician_database.append({'Politician':politician['name'],'Party':politician['party'],'State':politician['state'],\
            'Negativity':overall_statistics[0],'Neutrality':overall_statistics[1],'Positivity':overall_statistics[2],'Compound':overall_statistics[3], 'Average Likes':overall_statistics[4]})
    
    tweet_df = pd.DataFrame(tweet_database)
    poli_df = pd.DataFrame(politician_database)

    print(tweet_df.head)
    print(poli_df)
    tweet_df.to_csv(os.path.join(dir, 'tweet_sentiments.csv'), index=False)
    poli_df.to_csv(os.path.join(dir, 'politician_sentiments.csv'), index=False)

def main():
    dir = os.path.dirname(os.path.realpath(__file__))
    #json_path = os.path.join(dir, 'sample_tweet_data.json')
    json_path = os.path.join(dir, 'full_tweet_data.json')
    loaded_object = twitter_analysis.read_from_json(json_path)

    #stopwords = nltk.corpus.stopwords.words("english")
    compile_tweet_sentiments(dir, loaded_object)

if __name__ == '__main__':
    main()
