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

            f3 = open("resultsTweets.txt", "a", encoding="utf8")
            f3.write(str(tweet) + '\n')
                        
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
                f.close()
                result = 0
                for line in lines:
                    word = line.split(':')
                    if word[0] in tweet: # Database'deki kelime, gelen tweette geciyorsa
                        try:
                            result += int(word[1]) / len(lines) # len(lines) kategoride kac kelime oldugu
                        except:
                            result += 0

                if len(tweet) == 0:
                    lengthTweet = 1

                lengthTweet = len(tweet)
                if lengthTweet != 0:
                    rate.append(result / lengthTweet) # lengthTweet gelen tweetteki kelime sayisi

            #print(dataset + " - " + str(rate))
            # sonucların yazılacagı dosya
            # results.txt
            # sonuclar rate değişkeninde bulunuyor.
            # rate değişkeninde hangi kategori en yüksek puanda
            # bulunacak.
            # en yüksek puan da olan kategorinin dosyadaki
            # degeri bir arttırılacak. Dosyaya geri kaydedilecek

            dizi = rate
            results = []
            # oranların bulundugu dizi eğer boş gelirse
            # bu kısmın hiç çalışmaması için.
            if len(dizi) > 0:  
                a = dizi.index(max(dizi))
                try:
                    # v - oranların en büyüğüne ait kategorideki dosyadan kelimeleri okuduk
                    fd = open("./database/"+str(datasets[a])+".txt",encoding = 'utf-8')
                    liness = fd.readlines()

                    resultDataset = []
                    for line in liness:
                        word = line.split(':')
                        # kelimeler gelen tweette var ise 
                        # yeni bir diziye(resultDataset) kelime sayısı 1 arttırılarak kaydedilir
                        if word[0] in tweet:
                            # kelimenin sayısını bir arttırdık
                            tempDataset = word[0] + ":" + str(int(word[1]) + 1) + "\n"
                            resultDataset.append(tempDataset)
                        else:
                            # eğer kelime tweette geçmiyor ise
                            # yeni diziye(resultDataset) direk oynanmadan kaydedilir
                            # orginal hali ile.
                            # bunun sebebi dizilerde update olmadıgından.
                            # güncellenmesi gereken kelimeyi güncelleyip
                            # orginal halde olan kelimeyi aynı tutup kaydediyorum
                            # bu sayede dosyada sanki silip tekrar yazmış gibi güncellemiş oluyorum. 
                            resultDataset.append(line)
                    fd.close()
                    fdw = open("./database/"+str(datasets[a])+".txt", "w", encoding="utf8")
                    # resultDataset güncellenmiş olan kelime dizimizi 
                    # tekrar dosyaya yazıyoruz.
                    for data in resultDataset:
                        fdw.write(data)
                    fdw.close()           
                except:
                    print("dosya acılamadı")
                    f.close() 

                # yagızın bölgesi
                diziMax = 0
                f = open("results.txt", "r", encoding="utf8")
                try:
                    diziMaxNumber = np.amax(dizi)
                    diziMax = dizi.index(diziMaxNumber)
                    lines = f.readlines()
                    f.close()

                    f2 = open("results.txt", "w", encoding="utf8")

                    for line in lines:
                        a = line.split(':')
                        results.append(int(a[1]))

                    results[diziMax] = results[diziMax]+1
                    print(results)
                    
                    for i in range(0, 5):
                        b = lines[i].split(':')
                        f2.write(b[0]+':'+str(results[i])+'\n')

                    f2.close()
                except:
                    print('hata')
                
                if diziMax == 0:
                    print('art' + " - " + str(rate) + '\n')
                elif diziMax == 1:
                    print('economy' + " - " + str(rate) + '\n')
                elif diziMax == 2:
                    print('politics' + " - " + str(rate) + '\n')
                elif diziMax == 3:
                    print('sport' + " - " + str(rate) + '\n')
                else:                
                    print('technology' + " - " + str(rate) + '\n')
                                    
                if diziMax == 0:
                    f3.write('art' + " - " + str(rate) + '\n\n')
                elif diziMax == 1:
                    f3.write('economy' + " - " + str(rate) + '\n\n')
                elif diziMax == 2:
                    f3.write('politics' + " - " + str(rate) + '\n\n')
                elif diziMax == 3:
                    f3.write('sport' + " - " + str(rate) + '\n\n')
                else:                
                    f3.write('technology' + " - " + str(rate) + '\n\n')
                
                f3.close()
                # yagızın bölgesi bitiş
                


myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

myStream.filter(track=['turkiye'],  is_async=True)
