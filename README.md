<p align="center"><a href="https://phantomdonut.github.io/senatorial-sentiment" target="_blank" rel="noopener noreferrer"><img src="images/senatorial_logo.png?raw=true" alt="re-frame logo"></a></p>

# Senatorial Sentiment

## Overview
Quantitative **sentiment analysis** of all Tweets made by **U.S. Senators** in the 117th Congress. The overall goal of the project is to gain a better understanding for how the sentiment of public officials has changed over time in America's increasingly polarized political climate. Additionally, studying the intersection of the **polarity** of the **sentiment** of the Tweets in relation to illuminate if certain sentiments garner more **interaction** than usual. 

Created for the William & Mary [Cypher VII Hackathon](https://cypher-vii.devpost.com/), March 25 - 27, 2022.

## Acquiring the Tweets
* Congressional Twitter URLs for all 100 members of the 117th Congress are sourced from [USCD](https://ucsd.libguides.com/congress_twitter/home) political scientists.
* The corresponding username IDs are found and scraped using [Twitter API v2](https://developer.twitter.com/en/docs/twitter-api)
* The Python [Tweepy](https://www.tweepy.org/) module is utilized efficiently scrape the most recent several thousand Tweets from each Senator.
  * These Tweets are later processed to remove any retweets as they are not indicative of the Senator's own Tweeting patterns.
* Each Tweet is stored as an object containing the Tweet ID, the text, the creation date, and the public interaction metrics such as likes and retweets.
* Every politician is assigned a list containing their respective Tweet objects as well as their state and party affiliation before being written externally in a JSON format to reduce further API calls when performing subsequent analysis.

## Analysis Methodology
The [Natural Language Toolkit](https://www.nltk.org/) is a tool for classifying, tokenizing, parsing, and otherwise processing language data. The NLTK Python Module contains a variety of sentiment analysis tools which have been trained from billions of social media posts to discern the tone and sentiment of a string of text. Four scores are presented per string inputted into the NLTK - positive, negative, neutral, and compound. Based on the phrasing, word choice, and sentence structures the module approximates how much of the sentiment of the string, the Tweet in this case, was positive vs. negative vs. neutral. These scores are then arithmetically calculated into a single compound sentiment score. 

Prior to this process the Tweets will have any URLs filtered out via Regex as the NLTK works most effectively with natural speech rather than computer-specific text strings. Each compound score is added and averaged by the number of Tweets downloaded from each Senator (~3,000) to provide an overall sentiment of the Senator's online Twitter presence. 

Twitter's own API limits pose an interference in compiling a comprehensive chronological archive of each Senator's Twitter presence, as a maximum of only the 3,200 most recent Tweets from each user are acquirable. This results in an incomplete archive of the Senators' Tweets and introduces inconsistencies regarding from which point in time each Senator is being analyzed from. Political and world events which overlapped with the timelines of only some Senators are therefore unaccounted for in the above analysis. Possible solutions this problem would include more advanced scraping tools which bypass the Twitter API limitations.

## Display & Visualization
The sentiment scores, political affiliation, and state for each Senator are exported as a .csv for further exploration. Tableau is then used to parse the *.csv* into a variety of comprehensive and easily-readable tables, charts, and visualizations.

*Disclaimer: No individual non-public figures are included in the dataset in-depth nor are any individual Tweets presented as data viewable by the end-user.*

## Usage & Modification
Anyone wishing to perform analysis on the compiled Twitter data can import the [*full_tweet_data.json*](full_tweet_data.json) file into any JSON-compatible processor. The [*sentiment_analysis.py*](sentiment_analysis.py) Python script provides an example of importing, navigating the structure of, and performing sentiment analysis on this data. Please note that the full data file contains ~2.7 million lines of text and may be slow to view and operate upon.

Operating the included [*twitter_analysis.py*](twitter_analysis.py) Python script requires the creation of *.env* file in the same local folder with the Twitter Developer bearer token, access token, client token, and corresponding secrets. These can be acquired by applying for a [Twitter Developer Account](https://developer.twitter.com/)
