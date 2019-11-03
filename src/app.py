#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tweepy
import re

from TurkishStemmer import TurkishStemmer

consumer_key = "kZ5jxPjg7rq5XCq0R6LBYF6tY"
consumer_secret = "tI3lpqssacsulSh0YDik5FdUzn0GL5o7E3SfGuF9HTSaoSzlpK"

access_key = "1938234672-fZNrHZNQhMWbI02ef4oe74jlhU1K0oM4TXaDOFG"
access_secret = "jndmA6jdtFDR66TKrEjyFCkiOjMaDAH2HQHPeOjr3N5Ad"


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

api = tweepy.API(auth)

stemmer = TurkishStemmer()

datasets = ['art', 'economy', 'politics', 'sport', 'technology']

config = {
    "apiKey": 'AIzaSyBDgWYe3XTCVmhByPbm213KxDJL0rkcLO4',
    "authDomain": 'project01-f64c4.firebaseapp.com',
    "databaseURL": 'https://project01-f64c4.firebaseio.com',
    "projectId": 'project01-f64c4',
    "storageBucket": 'project01-f64c4.appspot.com',
    "messagingSenderId": '829199127735',
    "appId": '1:829199127735:web:3db486e626e90f66a46932',
}


class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        # Sadece dili türkçe olan tweetleri
        # alıp kullancagız
        if(status.lang == "tr"):
            tweet = status.text

            print(tweet)

            # tweetlerin içinden gereksiz kısımları çıkaracagız.
            # RT, @.. https:.. noktalama işaretleri
            resultRT = tweet.find('RT')
            if(resultRT != -1):
                tweet = tweet.split(tweet[:tweet.find(':') + 2])[1]

            while(tweet.find('@') != -1):
                resultUserTag = tweet.find('@')

                if(resultUserTag != -1):
                    resultSpace = tweet.find(' ', resultUserTag)

                    if(resultSpace == -1):
                        tweet = tweet.split(tweet[resultUserTag:])[0]
                    else:
                        tweet = tweet.split(
                            tweet[resultUserTag:resultSpace])[1]

            # http... olan kısmı çıkarılır
            while(tweet.find('http') != -1):
                resultHttp = tweet.find('http')
                if(resultHttp != -1):
                    resultSpace = tweet.find(' ', resultHttp)

                    tweet = tweet.split(tweet[resultHttp:resultSpace])[0]

            while(tweet.find('#') != -1):
                resultHttp = tweet.find('#')
                if(resultHttp != -1):
                    resultSpace = tweet.find(' ', resultHttp)

                    tweet = tweet.split(tweet[resultHttp:resultSpace])[0]

            # Noktalama işaretlerinden temizlenip
            for removedItem in ['.', ',', ':', '!', '\'', '’', '\n', '+', '%', '&', '❗️', '\"', '-', '_', '(', ')', '?', '..', '...', '[', ']', '{', '}', '“', '“']:
                tweet = tweet.replace(removedItem, ' ')

            for removedItem in [' ve ', ' ile ', ' bu ', ' da ', ' de ', ' ama ', ' fakat ', ' ancak ', ' eger ', ' sayet ', ' veya ']:
                tweet = tweet.replace(removedItem, ' ')

            # Büyük küçük harf farklılıgı olmaması için
            # bütün cümleyi kücük harf yapıyoruz
            tweet = tweet.lower()

            # tweet içindeki kelimelerin kokleri bulunacak
            tweetWords = tweet.split(' ')
            tweet = []
            for tweetWord in tweetWords:
                tweet.append(stemmer.stem(tweetWord))

            tweetTemp = []
            for word in tweet:
                if word != '':
                    tweetTemp.append(word)

            tweet = []
            tweet = tweetTemp

            print(tweet)
            rate = []
            # Database ile Karşılaştırma Yapılacak (AI)
            for dataset in datasets:
                f = open("./database/" + dataset +
                         ".txt", "r", encoding="utf8")

                lines = f.readlines()
                result = 0
                for line in lines:
                    word = line.split(':')
                    if word[0] in tweet:
                        result += int(word[1]) / len(lines)

                if len(tweet) == 0:
                    lengthTweet = 1

                lengthTweet = len(tweet)
                rate.append(result / lengthTweet)

            print(dataset + " - " + str(rate))

            # Bulunan sonuclara göre database güncellenecek

            # print(tweet)


myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

myStream.filter(track=['turkiye'],  is_async=True)
