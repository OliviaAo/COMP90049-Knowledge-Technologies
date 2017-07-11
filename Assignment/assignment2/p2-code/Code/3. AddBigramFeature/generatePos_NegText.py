import re


f1 = open('/Users/admin/Desktop/Knowledge Technology/Assignment/assignment2/2017S1-KTproj2-data/train-tweets.txt','r')
f2 = open('/Users/admin/Desktop/Knowledge Technology/Assignment/assignment2/2017S1-KTproj2-data/train-labels.txt','r')
f3 = open('/Users/admin/Desktop/Knowledge Technology/Assignment/assignment2/2017S1-KTproj2-data/testData/posTweets.txt','w+')
f4 = open('/Users/admin/Desktop/Knowledge Technology/Assignment/assignment2/2017S1-KTproj2-data/testData/negTweets.txt','w+')
f5 = open('/Users/admin/Desktop/Knowledge Technology/Assignment/assignment2/2017S1-KTproj2-data/testData/neuTweets.txt','w+')


trainData = f1.readlines()
labelData = f2.readlines()


def classifyTweets( rawData, labelData,f3,f4,f5,index):
    
    for i, row in enumerate(rawData):
        label = labelData[i][index:len(labelData[i])-1]
        newRow = row[index:len(row)]
        newRow=' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",newRow).split())
        if label == 'positive':
            f3.write(newRow+'\n')
        elif label == 'negative':
            f4.write(newRow+'\n')
        else:
            f5.write(newRow+'\n')
        
classifyTweets(trainData,labelData,f3,f4,f5,19)

f1.close()
f2.close()
f3.close()
f4.close()
