# !/usr/bin/python3
import tkinter

from tkinter import *
from tkinter import messagebox

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

class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        # Sadece dili türkçe olan tweetleri
        # alıp kullancagız
        if(status.lang == "tr"):
            tweet = status.text

            gui.writeTweets(tweet = tweet)

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

            ratePercent = []

            sum = 0
            for rateSum in rate:
                sum += rateSum

            for result in rate:
                ratePercent.append((100 * result) / sum)


            print(dataset + " - " + str(rate))
            gui.writeRate(dataset + " - " + str(ratePercent))

            # Bulunan sonuclara göre database güncellenecek

            # print(tweet)

class Gui:
    def __init__(self, root):
        self.root = root
        self.writeTweetsGrid = 0

        self.root.geometry("1300x500")

        self.label = Label(root, text="Gercek Zamanli Tweet Isleme :")
        self.label.grid(row = 0, column = 0, sticky = W) 

        self.btnRealTimeStart = Button(root, text = "Baslat", command = self.realTimeTweetStart)
        self.btnRealTimeStart.grid(row = 1, column = 1, sticky = W, pady = 2) 
        
        self.btnRealTimeStop = Button(root, text = "Durdur", command = self.realTimeTweetStop)
        self.btnRealTimeStop.grid(row = 1, column = 2, sticky = W, pady = 2) 

        self.labelframeTweets = LabelFrame(root, text = "Tweet")
        self.labelframeTweets.grid(row = 0, column = 3, columnspan = 1, rowspan = 3, pady = 10) 

        self.labelframeResult = LabelFrame(root, text = "Sonuclar")
        self.labelframeResult.grid(row = 0, column = 4, pady = 10) 

        self.realTimeTweetEntry = Entry(root, bd = 5)
        self.realTimeTweetEntry.grid(row = 1, column = 0) 

        self.Lb1 = Listbox(self.labelframeTweets, width=50)
        self.Lb1.grid(row = 0, column = 0, sticky = W) 
        
        self.Lb2 = Listbox(self.labelframeResult, width=50)
        self.Lb2.grid(row = 0, column = 0, sticky = W) 
        

    def realTimeTweetStart(self):
        myStream.filter(track=[self.realTimeTweetEntry.get()],  is_async=True)

    
    def realTimeTweetStop(self):
        print(1)

    def writeTweets(self, tweet):
        self.Lb1.insert(self.writeTweetsGrid, tweet)
        self.writeTweetsGrid += 1

    def writeRate(self, rate):
        self.Lb2.insert(self.writeTweetsGrid, rate)
        self.writeTweetsGrid += 1


myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

root = Tk()
gui = Gui(root)

root.mainloop()
