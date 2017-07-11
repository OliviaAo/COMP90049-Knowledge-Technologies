from StdSuites.Table_Suite import row


f1 = open('/Users/admin/Desktop/Knowledge Technology/Assignment/assignment2/2017S1-KTproj2-data/testData/DeleteAllUnrelated_DecisionTree/train1.arff','r')
f2 = open('/Users/admin/Desktop/Knowledge Technology/Assignment/assignment2/2017S1-KTproj2-data/testData/DeleteAllUnrelated_DecisionTree/dev1.arff','r')
f3 = open('/Users/admin/Desktop/Knowledge Technology/Assignment/assignment2/2017S1-KTproj2-data/testData/DeleteAllUnrelated_NaiveBayes/train1.arff','r')
f4 = open('/Users/admin/Desktop/Knowledge Technology/Assignment/assignment2/2017S1-KTproj2-data/testData/DeleteAllUnrelated_NaiveBayes/dev1.arff','r')
f5 = open('/Users/admin/Desktop/Knowledge Technology/Assignment/assignment2/2017S1-KTproj2-data/testData/train_bigram.txt','r')
f6 = open('/Users/admin/Desktop/Knowledge Technology/Assignment/assignment2/2017S1-KTproj2-data/testData/dev_bigram.txt','r')
f7 = open('/Users/admin/Desktop/Knowledge Technology/Assignment/assignment2/2017S1-KTproj2-data/testData/DeleteAllUnrelated_DecisionTree/trainBigram1.arff','w+')
f8 = open('/Users/admin/Desktop/Knowledge Technology/Assignment/assignment2/2017S1-KTproj2-data/testData/DeleteAllUnrelated_DecisionTree/devBigram1.arff','w+')
f9 = open('/Users/admin/Desktop/Knowledge Technology/Assignment/assignment2/2017S1-KTproj2-data/testData/DeleteAllUnrelated_NaiveBayes/trainBigram1.arff','w+')
f10 = open('/Users/admin/Desktop/Knowledge Technology/Assignment/assignment2/2017S1-KTproj2-data/testData/DeleteAllUnrelated_NaiveBayes/devBigram1.arff','w+')
trainData_Tree = f1.readlines()
devData_Tree = f2.readlines()
trainData_Naive = f3.readlines()
devData_Naive = f4.readlines()
trainBigram = f5.readlines()
devBigram = f6.readlines()


def addBigramFeature( rawData,bigramData,f, index1,index2 ):
    
    for i, row in enumerate(rawData):
        if i<index1: 
            f.write(row)
        else:  
#             print row
            sentiment = row[index2:len(row)]
#             print sentiment
            row = row[0:index2]
            bigram = bigramData[ i-index1 ][0]+","
            row = row.replace(row,row+bigram+sentiment)
#             print row
#             raw_input("test")
            f.write(row)


addBigramFeature(trainData_Naive,trainBigram,f9,31,73 )
addBigramFeature(devData_Naive,devBigram,f10,31,73 )
addBigramFeature(trainData_Tree,trainBigram,f7,27,48 )
addBigramFeature(devData_Tree,devBigram,f8,27,48 )


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

