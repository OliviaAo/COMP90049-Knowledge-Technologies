from StdSuites.Table_Suite import row


f1 = open('/Users/admin/Desktop/Knowledge Technology/Assignment/assignment2/2017S1-KTproj2-data/testData/DeleteAllUnrelated_DecisionTree/train1.arff','r')
f2 = open('/Users/admin/Desktop/Knowledge Technology/Assignment/assignment2/2017S1-KTproj2-data/testData/DeleteAllUnrelated_DecisionTree/dev1.arff','r')
f3 = open('/Users/admin/Desktop/Knowledge Technology/Assignment/assignment2/2017S1-KTproj2-data/testData/DeleteAllUnrelated_NaiveBayes/train1.arff','r')
f4 = open('/Users/admin/Desktop/Knowledge Technology/Assignment/assignment2/2017S1-KTproj2-data/testData/DeleteAllUnrelated_NaiveBayes/dev1.arff','r')
f5 = open('/Users/admin/Desktop/Knowledge Technology/Assignment/assignment2/2017S1-KTproj2-data/testData/train-tweets-Emo.txt','r')
f6 = open('/Users/admin/Desktop/Knowledge Technology/Assignment/assignment2/2017S1-KTproj2-data/testData/dev-tweets-Emo.txt','r')
f7 = open('/Users/admin/Desktop/Knowledge Technology/Assignment/assignment2/2017S1-KTproj2-data/testData/DeleteAllUnrelated_DecisionTree/trainEmo.arff','w+')
f8 = open('/Users/admin/Desktop/Knowledge Technology/Assignment/assignment2/2017S1-KTproj2-data/testData/DeleteAllUnrelated_DecisionTree/devEmo.arff','w+')
f9 = open('/Users/admin/Desktop/Knowledge Technology/Assignment/assignment2/2017S1-KTproj2-data/testData/DeleteAllUnrelated_NaiveBayes/trainEmo.arff','w+')
f10 = open('/Users/admin/Desktop/Knowledge Technology/Assignment/assignment2/2017S1-KTproj2-data/testData/DeleteAllUnrelated_NaiveBayes/devEmo.arff','w+')
trainData_Tree = f1.readlines()
devData_Tree = f2.readlines()
trainData_Naive = f3.readlines()
devData_Naive = f4.readlines()

trainEmo = f5.readlines()
devEmo = f6.readlines()


def addEmoFeature( rawData,emoData,f, index1,index2 ):
    
    for i, row in enumerate(rawData):
        if i<index1: 
            f.write(row)
        else:  
#             print row
            sentiment = row[index2:len(row)]
#             print sentiment
            row = row[0:index2]
            emo = emoData[ i-index1 ][0]+","
            row = row.replace(row,row+emo+sentiment)
#             print row
#             raw_input("test")
            f.write(row)


addEmoFeature(trainData_Naive,trainEmo,f9,31,73 )
addEmoFeature(devData_Naive,devEmo,f10,31,73 )
addEmoFeature(trainData_Tree,trainEmo,f7,27,48 )
addEmoFeature(devData_Tree,devEmo,f8,27,48 )


f1.close()
f2.close()
f3.close()
f4.close()
f5.close()
f6.close()
f7.close()
f8.close()
f9.close()
f10.close()

