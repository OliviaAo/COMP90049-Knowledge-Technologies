import re
import nltk
import itertools
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from __builtin__ import True
from nltk import word_tokenize

f1 = open('/Users/admin/Desktop/Knowledge Technology/Assignment/assignment2/2017S1-KTproj2-data/train-tweets.txt','r')
f2 = open('/Users/admin/Desktop/Knowledge Technology/Assignment/assignment2/2017S1-KTproj2-data/dev-tweets.txt','r')
f3 = open('/Users/admin/Desktop/Knowledge Technology/Assignment/assignment2/2017S1-KTproj2-data/testData/train_bigram.txt','w+')
f4 = open('/Users/admin/Desktop/Knowledge Technology/Assignment/assignment2/2017S1-KTproj2-data/testData/dev_bigram.txt','w+')
f5 = open('/Users/admin/Desktop/Knowledge Technology/Assignment/assignment2/2017S1-KTproj2-data/testData/posTweets.txt','r')
f6 = open('/Users/admin/Desktop/Knowledge Technology/Assignment/assignment2/2017S1-KTproj2-data/testData/negTweets.txt','r')
f7 = open('/Users/admin/Desktop/Knowledge Technology/Assignment/assignment2/2017S1-KTproj2-data/testData/neuTweets.txt','r')


def printLine(values, num, keyOrValue, tag):
    tmpValue = []
    for key in sorted(values.items(), key=lambda d: d[1], reverse=True)[:num]:
        tmpValue.append(key[keyOrValue])
    print(tag, ":", tmpValue)
    
    
# printLine(posfd,100, 0, "Bigrams")
# printLine(posfd,100, 1, "Counts")
# print pos_fd.most_common(50)
trainData = f1.readlines()
devData = f2.readlines()
posData = f5.readlines()
negData = f6.readlines() 
neuData = f7.readlines() 

def bigram( data ):
    words_bigram = [] 
    for row in data:
        words = row.split()
        words_bigram +=  nltk.bigrams( words ) 
    return words_bigram

def calculateSentimentScore( gram, sentimentList ):
#     print gram
#     raw_input("test3")
    for k,v in sentimentList:
#         print gram, k,v
        if gram == k:
#             print "Same!!!!: " 
#             print gram, k
            return v
    return 0
def maxScore(s1,s2,s3):
    if s1 > s2 and s1 > s3:
        return True
    else:
        return False
        
def addBigramFeature(data,posBigramList, negBigramList, neuBigramList,f):
    
    for row in data:
        if row[0] != '@':
            newRow = row[19:len(row)-1]
            newRow=' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",newRow).split())
#             newRow = "in the you are"
            words = newRow.split()
            row_bigram = nltk.bigrams( words ) 
            row_bigram= nltk.FreqDist(row_bigram)
#             print list(row_bigram)
           
#             for (key, count) in row_bigram.items():
#                 print key, count
#                 raw_input("test");
            posScore = negScore = neuScore = 0
            for key,count in row_bigram.items():
#                 print key
#                 raw_input("test1")
                posTempScore = calculateSentimentScore( key,posBigramList )
#                 raw_input("test2")
                negTempScore = calculateSentimentScore( key,negBigramList )
                neuTempScore = int(calculateSentimentScore( key,neuBigramList )/2)
#                 print posTempScore,negTempScore,neuTempScore
#                 raw_input("test2")
                if maxScore(posTempScore,negTempScore,neuTempScore) and posTempScore > posScore:
                    posScore += posTempScore
                elif maxScore(negTempScore,posTempScore,neuTempScore) and negTempScore > negScore:
                    negScore += negTempScore 
                elif maxScore(neuTempScore,negTempScore,posTempScore) and neuTempScore > neuScore:
                    neuScore += neuTempScore
#                 print "total: ",
#             print posScore,negScore,neuScore
            if posScore == negScore == neuScore:
#                 print "neutral"
                f.write("1\n")
            elif posScore >= negScore and posScore >= neuScore:
#                 print "positive"
                f.write("2\n")
            elif negScore >= posScore and negScore >= neuScore:
#                 print "negative"
                f.write("0\n")
            elif neuScore >= posScore and neuScore >= negScore:
#                 print "neutral"
                f.write("1\n")
            
#             raw_input("test")

# addBigramFeature(posWords, negWords)
pos_bigram = bigram( posData )
pos_fd = nltk.FreqDist(pos_bigram)
pos_Common100 = pos_fd.most_common(100)
    
neg_bigram = bigram( negData )
neg_fd = nltk.FreqDist(neg_bigram)
neg_Common100 = neg_fd.most_common(100)

neu_bigram = bigram( neuData )
neu_fd = nltk.FreqDist(neu_bigram)
neu_Common100 = neu_fd.most_common(100)


addBigramFeature(trainData, pos_Common100, neg_Common100,neu_Common100,f3)
addBigramFeature(devData, pos_Common100, neg_Common100,neu_Common100,f4)
f1.close()
f2.close()
f3.close()
f4.close()
f5.close()
f6.close()
f7.close()



