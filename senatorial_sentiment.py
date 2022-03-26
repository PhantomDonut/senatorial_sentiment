import pandas as pd
import os
import regex as re
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import twitter_analysis

def load_word_frequency_chart(file_name):
    df = pd.read_csv(file_name)

    #most_common_100 = df['word'].iloc[:100]
    #print(most_common_100)

    frequency_dict = dict(df.values)
    print(frequency_dict['the'])

def create_word_freq(word_list):
    word_frequency = {}
    for word in word_list:
        if word in word_frequency:
            word_frequency[word] = word_frequency[word] + 1
        else:
            word_frequency[word] = 1
    return word_frequency

def inverse_lerp(a, b, v):
    return (v - a) / (b - a)

def main():
    dir = os.path.dirname(os.path.realpath(__file__))
    json_path = os.path.join(dir, 'tweet_data.json')
    loaded_object = twitter_analysis.read_from_json(json_path)

    #stopwords = nltk.corpus.stopwords.words("english")
    sia = SentimentIntensityAnalyzer()

    polarity_database = {}

    #for i in range(0, 1):
    for i in range(0, len(loaded_object)):
        politician = loaded_object[i]
        #print(f"{politician['name']} ({politician['party']}) from {politician['state']} has {len(politician['tweets'])} Tweets")
        overall_polarity = 0
        for tweet in politician['tweets']:
            #clean_alt = re.sub("[^\w\d'\s]+", "", tweet['text'])
            cleaned_tweet = re.sub(r'http\S+', '', tweet['text'])
            #print(cleaned_tweet)
            polarity = sia.polarity_scores(cleaned_tweet)
            overall_polarity = overall_polarity + polarity['compound']
            #print('\n\n')
        overall_polarity = overall_polarity / len(politician['tweets'])
        polarity_database[politician['name']] = [overall_polarity, 0, politician['party'], politician['state']]
    
    min = 1
    max = -1

    for polarity in polarity_database.values():
        if polarity[0] < min:
            min = polarity[0]
        elif polarity[0] > max:
            max = polarity[0]

    data_holder = []
    #output_df = pd.DataFrame(data_dict)

    for politician in polarity_database:
        polarity_database[politician][1] = inverse_lerp(min, max, polarity_database[politician][0])
        #print(f'{politician} has a relative polarity of {polarity_database[politician][1]} and an absolute of {polarity_database[politician][0]}')
        data_holder.append({'Politician':politician, 'Party':polarity_database[politician][2], 'State':polarity_database[politician][3], 'Polarity':polarity_database[politician][0], 'Relative Polarity':polarity_database[politician][1]})
    
    output_df = pd.DataFrame(data_holder)

    print(output_df.head)
    output_df.to_csv(os.path.join(dir, 'polarity.csv'), index=False)

    #string_no_punctuation = re.sub("[^\w\d'\s]+", "", test_tweet)
    #string_split = string_no_punctuation.lower().split()

    #cleaned_words = [word for word in string_split if word not in stopwords]


    #print(sia.polarity_scores(test_tweet_2))
    #print(sia.polarity_scores(test_tweet))

    # create_word_freq(cleaned_words)
    #load_word_frequency_chart(os.path.join(dir, 'unigram_freq.csv'))

if __name__ == '__main__':
    main()
