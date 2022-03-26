<p align="center"><a href="https://phantomdonut.github.io/senatorial-sentiment" target="_blank" rel="noopener noreferrer"><img src="images/senatorial_logo.png?raw=true" alt="re-frame logo"></a></p>

# Senatorial Sentiment

## Overview
Quantitative **sentiment analysis** of all Tweets made by U.S. Senators in the 117th Congress.

Created for the William & Mary [Cypher VII Hackathon](https://cypher-vii.devpost.com/), March 25 - 27, 2022.

## How It Works
* Congressional Twitter URLs sourced from [USCD](https://ucsd.libguides.com/congress_twitter/home) political scientists. 
* Corresponding usernames are found and scraped using [Twitter API v2](https://developer.twitter.com/en/docs/twitter-api) via [Tweepy](https://www.tweepy.org/).
* Each Senator's tweets (including interaction metrics) are converted to JSON and stored to reduce API calls
* Tweets are analyzed and given a compound sentiment score based on their positive, negative, and neutral scores from the [Natural Language Toolkit](https://www.nltk.org/)

## Usage & Modification
Operating the included Python scripts requires the creation of *.env* file with the Twitter Developer bearer token, access token, client token, and corresponding secrets.
