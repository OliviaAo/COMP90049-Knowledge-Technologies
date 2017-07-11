


f1 = open('/Users/admin/Desktop/Knowledge Technology/Assignment/assignment2/2017S1-KTproj2-data/testData/train.arff','r')
f2 = open('/Users/admin/Desktop/Knowledge Technology/Assignment/assignment2/2017S1-KTproj2-data/testData/dev.arff','r')
f3 = open('/Users/admin/Desktop/Knowledge Technology/Assignment/assignment2/2017S1-KTproj2-data/testData/train1.arff','w+')
f4 = open('/Users/admin/Desktop/Knowledge Technology/Assignment/assignment2/2017S1-KTproj2-data/testData/dev1.arff','w+')

trainData = f1.readlines()
devData = f2.readlines()

def delAttribute( data,index, f,length ):
    
    for row in data:
        if row[0] == '@': 
            f.write(row)
        else:  
            index = index
            row1 = row;
            row = row[0:index]
            row2 = row1[index+length:len(row1)]
            row = row.replace(row,row+row2)
            f.write(row)


# Delete @ATTRIBUTE a NUMERIC 
# delAttribute(trainData,101,f3,2)
# delAttribute(devData,101,f4,2)

# Delete @ATTRIBUTE are NUMERIC 
def deleteAll_J48(data, f):
      
    for row in data:
        if row[0] == '@': 
            f.write(row)
        else:  
            # amazing:
            newRow = row[21:23]
            # awesome+best+birthday+cant:
            newRow = newRow.replace(newRow,newRow+row[29:37])
            # day+death+drone+excited+fake+fuck+fucking+good+great:
            newRow = newRow.replace(newRow,newRow+row[39:57])
            # happy+hate:
            newRow = newRow.replace(newRow,newRow+row[59:63])
            # ice:
            newRow = newRow.replace(newRow,newRow+row[65:67])
            # leftists:
            newRow = newRow.replace(newRow,newRow+row[71:73])
            # love:
            newRow = newRow.replace(newRow,newRow+row[75:77])
            # not:
            newRow = newRow.replace(newRow,newRow+row[85:87])
            # people:
            newRow = newRow.replace(newRow,newRow+row[89:91])
            # shit+so+stupid:
            newRow = newRow.replace(newRow,newRow+row[95:101])
            # sentiment:
            newRow = newRow.replace(newRow,newRow+row[111:len(row)])
            f.write(newRow)
               
deleteAll_J48(trainData,f3)             
deleteAll_J48(devData,f4)   

def deleteAll_NaiveBayes(data, f):
     
    for row in data:
        if row[0] == '@': 
            f.write(row)
        else:  
            # id:
            newRow = row[0:19]
            # amazing+antman:
            newRow = newRow.replace(newRow,newRow+row[21:25])
            # awesome+best+birthday+cant:
            newRow = newRow.replace(newRow,newRow+row[29:37])
            # day+death+drone+excited+fake+fuck+fucking+good+great:
            newRow = newRow.replace(newRow,newRow+row[39:57])
            # happy+hate:
            newRow = newRow.replace(newRow,newRow+row[59:63])
            # liberals+love+my:
            newRow = newRow.replace(newRow,newRow+row[73:79])
            # nazi:
            newRow = newRow.replace(newRow,newRow+row[81:83])
            # not+obama:
            newRow = newRow.replace(newRow,newRow+row[85:89])
            # shit:
            newRow = newRow.replace(newRow,newRow+row[95:97])
            # stupid+supremacists:
            newRow = newRow.replace(newRow,newRow+row[99:103])
            # trump+sentiment:
            newRow = newRow.replace(newRow,newRow+row[109:len(row)])
            f.write(newRow)
            
# deleteAll_NaiveBayes(trainData, f3)           
# deleteAll_NaiveBayes(devData, f4)

f1.close()
f2.close()
f3.close()
f4.close()
