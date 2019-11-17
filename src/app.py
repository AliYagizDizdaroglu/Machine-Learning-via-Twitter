#!/usr/bin/env python
# -*- coding: utf-8 -*-
from TurkishStemmer import TurkishStemmer

import numpy as np
import tweepy
import re

consumer_key = "kZ5jxPjg7rq5XCq0R6LBYF6tY"
consumer_secret = "tI3lpqssacsulSh0YDik5FdUzn0GL5o7E3SfGuF9HTSaoSzlpK"

access_key = "1938234672-fZNrHZNQhMWbI02ef4oe74jlhU1K0oM4TXaDOFG"
access_secret = "jndmA6jdtFDR66TKrEjyFCkiOjMaDAH2HQHPeOjr3N5Ad"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

api = tweepy.API(auth)

stemmer = TurkishStemmer()

datasets = ['art', 'economy', 'politics', 'sport', 'technology']


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

            for removedItem in [' ki ', ' ve ', ' ile ', ' bu ', ' da ', ' de ', ' ama ', ' fakat ', ' ancak ', ' eger ', ' sayet ', ' veya ']:
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
                        try:
                            result += int(word[1]) / len(lines)
                        except:
                            result += 0

                if len(tweet) == 0:
                    lengthTweet = 1

                lengthTweet = len(tweet)
                if lengthTweet != 0:
                    rate.append(result / lengthTweet)

            print(dataset + " - " + str(rate))
            # sonucların yazılacagı dosya
            # results.txt
            # sonuclar rate değişkeninde bulunuyor.
            # rate değişkeninde hangi kategori en yüksek puanda
            # bulunacak.
            # en yüksek puan da olan kategorinin dosyadaki
            # degeri bir arttırılacak. Dosyaya geri kaydedilecek

            dizi = rate
            results = []

            f = open("results.txt", "r", encoding="utf8")
            try:

                diziMaxNumber = np.amax(dizi)
                diziMax = dizi.index(diziMaxNumber)
                lines = f.readlines()

                f2 = open("results.txt", "w", encoding="utf8")

                for line in lines:
                    a = line.split(':')
                    results.append(int(a[1]))

                results[diziMax] = results[diziMax]+1
                print(results)

                for i in range(0, 5):
                    b = lines[i].split(':')
                    f2.write(b[0]+':'+str(results[i])+'\n')
            except:
                print('hata')


myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

myStream.filter(track=['turkiye'],  is_async=True)
