'''
Date: 19/3/2017
Author: Ao Li
Work: Comp90049 Knowledge Technologies Assignmen1
Goal: Implement back-transliteration for Persian to Latin
'''

'''
    Some libraries used in implement:
        1. Levenshtein: System library for GED method.
        2. nltk: System library for creating N-gram for given string
'''
import Levenshtein
import nltk

''' 
  1.Open the Files:
    f1 ---> train.txt: A list of 13K names in the Persian script, with their Latin equivalent
    f2 ---> names.txt: A list of 26K names in the Latin script (Include all of the Persian names)
    
  2.Write the Files(Store the match Latin for the intended Persian):
  
    2.1. Some basic method:
    f3 ---> results_global_myself.txt: Using self-writ GED method. 
    f4 ---> results_global_system.txt: Using system GED method.(import from Levenshtein library)
    f5 ---> results_local_myself.txt: Using self-writ LED method.
    f6 ---> results_2-Gram.txt: Using self-writ N-Gram method, where N = 2.
    
    2.2. Extension:
    
    2.2.1. Use exist substitution score matrix:
    f7 ---> results_Blosum62Matrix.txt: Using Blosum62 substitution score matrix + self-write GED method.
    
    2.2.2. Randomly choose 100/500/1000 lines from the train.txt files for ten times, and use each ten files to trained a matrix.
    f8 ---> results_100TrainedLinesMatrix.txt: Using 100 * 10 lines trained matrix + self-write GED method.
    f9 ---> results_500TrainedLinesMatrix.txt: Using 500 * 10 lines trained matrix + self-write GED method.
    f10 ---> results_1000TrainedLinesMatrix.txt: Using 1000 * 10 lines trained matrix + self-write GED method.
    f11 ---> results_1000TrainedLinesMatrix.txt: Using 1000 * 10 lines trained matrix + self-write GED method + Multiple matches.
    f12 ---> results_1000TrainedLinesMatrix.txt: Using 1000 * 10 lines trained matrix + self-write GED method + Multiple matches + Soundex.
'''
# Open files:
f1 = open('train.txt','r')
f2 = open('names.txt','r')

# Write results from different method to different files:
f3 = open('/home/subjects/comp90049/submission/aol3/results_global_myself.txt','w+')
f4 = open('/home/subjects/comp90049/submission/aol3/results_global_system.txt','w+')
f5 = open('/home/subjects/comp90049/submission/aol3/results_local_myself.txt','w+')
f6 = open('/home/subjects/comp90049/submission/aol3/results_N-Gram.txt','w+')
f7 = open('/home/subjects/comp90049/submission/aol3/results_Blosum62Matrix.txt','w+')
f8 = open('/home/subjects/comp90049/submission/aol3/results_100TrainedLinesMatrix.txt','w+')
f9 = open('/home/subjects/comp90049/submission/aol3/results_500TrainedLinesMatrix.txt','w+')
f10 = open('/home/subjects/comp90049/submission/aol3/results_1000TrainedLinesMatrix.txt','w+')
f11 = open('/home/subjects/comp90049/submission/aol3/results_1000TrainedLinesMatrix_Multi.txt','w+')
f12 = open('/home/subjects/comp90049/submission/aol3/results_1000TrainedLinesMatrix_Multi_Soundex.txt','w+')

''' 
    Method 1: Implement Self-Write Global Edit Distance Method:
    
    1. Specified parameters [m,i,d,r]:
            m ---> Match
            i ---> Insertion
            d ---> Deletion
            r ---> Replace
            
        1.1. Example of general parameters:
    
            1.1.1. "Normal" Distance:
            para1 = [ 1,-1,-1,-1 ]
        
            1.1.2 Levenshtein Distance:
            para2 = [ 0, 1, 1, 1 ]
            
            Note: After testing para1 & para2, find para1 can achieve better precision
                  So, use para1 in the following implement.
            
    2. Read data from data set:
        pNames: represents the list of Persian Names
        lNames: represents the list of Latin Names
        
    3. For each Persian name in train.txt, calculating the GED between it and all the Latin names in name.txt.
       Aim to find the Latin name with "best global distance"  
    
    4. Write the results to the specific file.
       
'''
def selfwrite_GED():
    # Step 1:
    para1 = [ 1,-1,-1,-1 ]
    para2 = [ 0, 1, 1, 1 ]
    
    # Step 2:
    pNames = f1.readlines()
    lNames = f2.readlines()
    
    # Step 3:
    for pName in pNames:
          
        maxDistance = -10000
        matchName = ""
            
        pName = pName.replace(pName," "+pName)
        index = pName.find('\t')
        pName = pName[0:index]
        pName = pName.lower()
      
        for lName in lNames:
          
            lName = lName.replace(lName," "+lName)  
            index = lName.find('\n')
            lName = lName[0:index]
              
            lenP = len( pName )
            lenL = len( lName )  
            distanceG = [[0 for i in range(lenL) ] for i in range(lenP)]
            for i in range(0,lenL):
                distanceG[ 0 ][ i ] = i * para1[ 2 ]
            for i in range(0,lenP):
                distanceG[ i ][ 0 ] = i * para1[ 1 ]
               
            for i in range(1,lenP):
                for j in range(1,lenL):
                    if pName[ i ] == lName[ j ]:
                        distanceG[ i ][ j ] = max(
                        distanceG[ i-1 ][ j-1 ] + para1[0],
                        distanceG[ i-1 ][ j ] + para1[1],
                        distanceG[ i ][ j-1 ] + para1[2]
                        )
                    else:
                        distanceG[ i ][ j ] = max(
                        distanceG[ i-1 ][ j-1 ] + para1[3],
                        distanceG[ i-1 ][ j ] + para1[1],
                        distanceG[ i ][ j-1 ] + para1[2]
                        )
                          
            if distanceG[ lenP-1 ][ lenL-1 ] > maxDistance:
                maxDistance = distanceG[ lenP-1 ][ lenL-1 ]
                matchName = lName
                  
        matchName = matchName[1:]
        pName = pName[1:].upper()
        print pName+ "\t" + matchName 
        
        # Step 4:
        f3.write(pName+ "\t" + matchName + "\n")
    f3.close()
    
'''
    Method 2: Implement System Global Edit Distance Method:
          
    1. Read data from data set:
        pNames: represents the list of Persian Names
        lNames: represents the list of Latin Names
        
    2. For each Persian name in train.txt, calculating the GED between it and all the Latin names in name.txt.
       Aim to find the Latin name with "best global distance"  
    
    3. Write the results to the specific file.
'''
def system_GED():
    # Step 1:
    pNames = f1.readlines()
    lNames = f2.readlines()
    
    # Step 2:
    for pName in pNames:
        dis = 1000000
        matchName = ''
          
        index = pName.find('\t')
        pName = pName[0:index]
        pName = pName.lower()
        print pName,
        for lName in lNames:
            index = lName.find('\n')
            lName = lName[0:index]
            disTemp = Levenshtein.distance(lName,pName)
            if disTemp < dis:
                dis = disTemp
                matchName = lName
        print "\t"+matchName
        
        # Step 3:
        f4.write(pName+ "\t" + matchName + "\n")
    f4.close()

'''
    Method 3: Implement Self-Write Local Edit Distance Method:
    
    Very similar to self-write GED method, just different in the step3 ---  calculating the distance.
    In here just calculate local distance, but global distance.
'''
def selfwrite_LED():
    # Step 1:
    para1 = [ 1,-1,-1,-1 ]
    para2 = [ 0, 1, 1, 1 ]
    
    # Step 2:
    pNames = f1.readlines()
    lNames = f2.readlines()
    
    # Step 3:
    for pName in pNames:
          
        maxDistance = -10000
        matchName = ""
            
        pName = pName.replace(pName," "+pName)
        index = pName.find('\t')
        pName = pName[0:index]
        pName = pName.lower()
        for lName in lNames:
          
            lName = lName.replace(lName," "+lName)  
            index = lName.find('\n')
            lName = lName[0:index]
              
            lenP = len( pName )
            lenL = len( lName ) 
            maxDistanceTemp = 0
            distanceG = [[0 for i in range(lenL) ] for i in range(lenP)]
            for i in range(0,lenL):
                distanceG[ 0 ][ i ] = 0
            for i in range(0,lenP):
                distanceG[ i ][ 0 ] = 0
         
            for i in range(1,lenP):
                for j in range(1,lenL):
                    if pName[ i ] == lName[ j ]:
                        distanceG[ i ][ j ] = max(
                        distanceG[ i-1 ][ j-1 ] + para1[0],
                        distanceG[ i-1 ][ j ] + para1[1],
                        distanceG[ i ][ j-1 ] + para1[2],
                        0
                        )
                    else:
                        distanceG[ i ][ j ] = max(
                        distanceG[ i-1 ][ j-1 ] + para1[3],
                        distanceG[ i-1 ][ j ] + para1[1],
                        distanceG[ i ][ j-1 ] + para1[2],
                        0
                        )
                    if distanceG[ i ][ j ] > maxDistanceTemp:
                        maxDistanceTemp = distanceG[ i ][ j ]  
            if maxDistanceTemp > maxDistance:
                maxDistance = maxDistanceTemp
                matchName = lName
                  
        matchName = matchName[1:]
        pName = pName[1:].upper()
        print pName,"\t",matchName
        f5.write(pName+ "\t" + matchName + "\n")
    f5.close()

'''
    Method 4: Implement N-Gram Method:       
            
    1. Read data from data set:
        pNames: represents the list of Persian Names
        lNames: represents the list of Latin Names
        
    2. For each Persian name in train.txt, calculating the N-Gram distance between it and all the Latin names in name.txt.
       Aim to find the Latin name with "best N-Gram distance" 
        
       2.1. Set value N
       Note: 
            1). After testing different, when N = 2, the method get highest precision.
            2). I use nltk.bigrams() in nltk library to create 2-gram.
    
    3. Write the results to the specific file.
'''
def selfwrite_2Gram():
    # Step 1:
    pNames = f1.readlines()
    lNames = f2.readlines()
    
    # Step 2:
    for pName in pNames:
        index = pName.find('\t')
        pName = pName[0:index]
        pName = pName.lower()
        pName = pName.replace(pName,'#'+pName+'#')
        pName_2gram = list( nltk.bigrams( pName ) )
        gramDistance = 100000
        matchName = ''
        
        # nltk.bigrams can create 2-gram for the string pName
        pLen = len(pName_2gram)
      
        for lName in lNames:  
            index = lName.find('\n')
            lName = lName[0:index]
            lName = lName.replace(lName,'#'+lName+'#')
            
            # nltk.bigrams can create 2-gram for the string lName
            lName_2gram = list( nltk.bigrams( lName ) )
            lLen = len(lName_2gram)
            visit = [0 for i in range( lLen )]
            intersectionTempNum = 0
            for i in range( pLen ):
                for j in range( lLen ):
                    if pName_2gram[i] == lName_2gram[j] and visit[j] != 1:
                        intersectionTempNum += 1
                        visit[ j ] = 1
             
            gramTempDistance = pLen + lLen - 2*intersectionTempNum
            if gramTempDistance < gramDistance:
                gramDistance = gramTempDistance  
                matchName = lName
          
        pName = pName[1:len(pName)-1]
        matchName = matchName[1:len(matchName)-1]
        print pName+ "\t" + matchName
        
        # Step 3:
        f6.write(pName+ "\t" + matchName + "\n") 
    f6.close()

'''
    Method 5: Implement Blosum62 substitution matrix + Self-Write GED Method:       
    
    1. Set different weight to different parameters:
        
        1.1. To match & replace parameter, use the value in Blosum62 substitution score matrix 
        
        Note:
            The original Blosum62 matrix is as below:
                C  S  T  P  A  G  N  D  E  Q  H  R  K  M  I  L  V  F  Y  W
            C  9 -1 -1 -3  0 -3 -3 -3 -4 -3 -3 -3 -3 -1 -1 -1 -1 -2 -2 -2
            S -1  4  1 -1  1  0  1  0  0  0 -1 -1  0 -1 -2 -2 -2 -2 -2 -3
            T -1  1  4  1 -1  1  0  1  0  0  0 -1  0 -1 -2 -2 -2 -2 -2 -3 
            P -3 -1  1  7 -1 -2 -1 -1 -1 -1 -2 -2 -1 -2 -3 -3 -2 -4 -3 -4
            A  0  1 -1 -1  4  0 -1 -2 -1 -1 -2 -1 -1 -1 -1 -1 -2 -2 -2 -3
            G -3  0  1 -2  0  6 -2 -1 -2 -2 -2 -2 -2 -3 -4 -4  0 -3 -3 -2
            N -3  1  0 -2 -2  0  6  1  0  0 -1  0  0 -2 -3 -3 -3 -3 -2 -4
            D -3  0  1 -1 -2 -1  1  6  2  0 -1 -2 -1 -3 -3 -4 -3 -3 -3 -4
            E -4  0  0 -1 -1 -2  0  2  5  2  0  0  1 -2 -3 -3 -3 -3 -2 -3
            Q -3  0  0 -1 -1 -2  0  0  2  5  0  1  1  0 -3 -2 -2 -3 -1 -2
            H -3 -1  0 -2 -2 -2  1  1  0  0  8  0 -1 -2 -3 -3 -2 -1  2 -2
            R -3 -1 -1 -2 -1 -2  0 -2  0  1  0  5  2 -1 -3 -2 -3 -3 -2 -3
            K -3  0  0 -1 -1 -2  0 -1  1  1 -1  2  5 -1 -3 -2 -3 -3 -2 -3
            M -1 -1 -1 -2 -1 -3 -2 -3 -2  0 -2 -1 -1  5  1  2 -2  0 -1 -1   
            I -1 -2 -2 -3 -1 -4 -3 -3 -3 -3 -3 -3 -3  1  4  2  1  0 -1 -3
            L -1 -2 -2 -3 -1 -4 -3 -4 -3 -2 -3 -2 -2  2  2  4  3  0 -1 -2
            V -1 -2 -2 -2  0 -3 -3 -3 -2 -2 -3 -3 -2  1  3  1  4 -1 -1 -3
            F -2 -2 -2 -4 -2 -3 -3 -3 -3 -3 -1 -3 -3  0  0  0 -1  6  3  1
            Y -2 -2 -2 -3 -2 -3 -2 -3 -2 -1  2 -2 -2 -1 -1 -1 -1  3  7  2
            W -2 -3 -3 -4 -3 -2 -4 -4 -3 -2 -2 -3 -3 -1 -3 -2 -3  1  2 11 
            
            which is not ordered and lack of Latin letters. So firstly modified it as below:
            
               A  B  C  D  E  F  G  H  I  J  K  L  M  N  O  P  Q  R  S  T  U  V  W  X  Y  Z
            A  4  *  0 -2 -1 -2  0 -2 -1  * -1 -1 -1 -1  * -1 -1 -1  1 -1  * -2 -3  * -2  *
            B  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  * 
            C  0  *  9 -3 -4 -2 -3 -3 -1  * -3 -1 -1 -3  * -3 -3 -3 -1 -1  * -1 -2  * -2  *
            D -2 -* -3  6  2 -3 -1 -1 -3  * -1 -4 -3  1  * -1  0 -2  0  1  * -3 -4  * -3  *
            E -1  * -4  2  5 -3 -2  0 -3  *  1 -3 -2  0  * -1  2  0  0  0  * -3 -3  * -2  *
            F -2  * -2 -3 -3  6 -3 -1  0  * -3  0  0 -3  * -4 -3 -3 -2 -2  * -1  1  *  3  *
            G  0  * -3 -1 -2 -3  6 -2 -4  * -2 -4 -3 -2  * -2 -2 -2  0  1  *  0 -2  * -3  *     
            H -2  * -3  1  0 -1 -2  8 -3  * -1 -3 -2  1  * -2  0  0 -1  0  * -2 -2  *  2  *
            I -1  * -1 -3 -3  0 -4 -3  4  * -3  2  1 -3  * -3 -3 -3 -2 -2  *  1 -3  * -1  *
            J  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  * 
            K -1  * -3 -1  1 -3 -2 -1 -3  *  5 -2 -1  0  * -1  1  2  0  0  * -3 -3  * -2  *
            L -1  * -1 -4 -3  0 -4 -3  2  * -2  4  2 -3  * -3 -2 -2 -2 -2  *  3 -2  * -1  *
            M -1  * -1 -3 -2  0 -3 -2  1  * -1  2  5 -2  * -2  0 -1 -1 -1  * -2 -1  * -1  *
            N -2  * -3  1  0 -3  0 -1 -3  *  0 -3 -2  6  * -2  0  0  1  0  * -3 -4  * -2  *
            O  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *        
            P -1  * -3 -1 -1 -4 -2 -2 -3  * -1 -3 -2 -1  *  7 -1 -2 -1  1  * -2 -4  * -3  *
            Q -1  * -3  0  2 -3 -2  0 -3  *  1 -2  0  0  * -1  5  1  0  0  * -2 -2  * -1  *
            R -1  * -3 -4  0 -3 -2  0 -3  *  2 -2 -1  0  * -2  1  5 -1 -1  * -3 -3  * -2  *
            S  1  * -1  0  0 -2  0 -1 -2  *  0 -2 -1  1  * -1  0 -1  4  1  * -2 -3  * -2  *
            T -1  * -1  1  0 -2  1  0 -2  *  0 -2 -1  0  *  1  0 -1  1  4  * -2 -3  * -2  *
            U  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *   
            V  0  * -1 -3 -2 -1 -3 -3  3  * -2  1  1 -3  * -2 -2 -3 -2 -2  *  4 -3  * -1  *
            W -3  * -2 -4 -3  1 -2 -2 -3  * -3 -2 -1 -4  * -4 -2 -3 -3 -3  * -3 11  *  2  *
            X  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  * 
            Y -2  * -2 -3 -2  3 -3  2 -1  * -2 -1 -1 -2  * -3 -1 -2 -2 -2  * -1  2  *  7  *
            Z  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  *  * 
            
            Since there is not enough relationship among the rest 6 letter, set the relationship myself.
            when row letter is the same as column letter, set 5 into the matrix, otherwise 0.
            For example: B[ B ] = 5, B[ C ] = 0.. etc
            So the Blosum62 is secondly modified as below: 
                
               A  B  C  D  E  F  G  H  I  J  K  L  M  N  O  P  Q  R  S  T  U  V  W  X  Y  Z
            A  4, 0, 0,-2,-1,-2, 0,-2,-1, 0,-1,-1,-1,-1, 0,-1,-1,-1, 1,-1, 0,-2,-3, 0,-2, 0 
            B  0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 
            C  0, 0, 9,-3,-4,-2,-3,-3,-1, 0,-3,-1,-1,-3, 0,-3,-3,-3,-1,-1, 0,-1,-2, 0,-2, 0 
            D -2, 0,-3, 6, 2,-3,-1,-1,-3, 0,-1,-4,-3, 1, 0,-1, 0,-2, 0, 1, 0,-3,-4, 0,-3, 0 
            E -1, 0,-4, 2, 5,-3,-2, 0,-3, 0, 1,-3,-2, 0, 0,-1, 2, 0, 0, 0, 0,-3,-3, 0,-2, 0 
            F -2, 0,-2,-3,-3, 6,-3,-1, 0, 0,-3, 0, 0,-3, 0,-4,-3,-3,-2,-2, 0,-1, 1, 0, 3, 0 
            G  0, 0,-3,-1,-2,-3, 6,-2,-4, 0,-2,-4,-3,-2, 0,-2,-2,-2, 0, 1, 0, 0,-2, 0,-3, 0    
            H -2, 0,-3, 1, 0,-1,-2, 8,-3, 0,-1,-3,-2, 1, 0,-2, 0, 0,-1, 0, 0,-2,-2, 0, 2, 0 
            I -1, 0,-1,-3,-3, 0,-4,-3, 4, 0,-3, 2, 1,-3, 0,-3,-3,-3,-2,-2, 0, 1,-3, 0,-1, 0 
            J  0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0  
            K -1, 0,-3,-1, 1,-3,-2,-1,-3, 0, 5,-2,-1, 0, 0,-1, 1, 2, 0, 0, 0,-3,-3, 0,-2, 0 
            L -1, 0,-1,-4,-3, 0,-4,-3, 2, 0,-2, 4, 2,-3, 0,-3,-2,-2,-2,-2, 0, 3,-2, 0,-1, 0 
            M -1, 0,-1,-3,-2, 0,-3,-2, 1, 0,-1, 2, 5,-2, 0,-2, 0,-1,-1,-1, 0,-2,-1, 0,-1, 0 
            N -2, 0,-3, 1, 0,-3, 0,-1,-3, 0, 0,-3,-2, 6, 0,-2, 0, 0, 1, 0, 0,-3,-4, 0,-2, 0 
            O  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0         
            P -1, 0,-3,-1,-1,-4,-2,-2,-3, 0,-1,-3,-2,-1, 0, 7,-1,-2,-1, 1, 0,-2,-4, 0,-3, 0 
            Q -1, 0,-3, 0, 2,-3,-2, 0,-3, 0, 1,-2, 0, 0, 0,-1, 5, 1, 0, 0, 0,-2,-2, 0,-1, 0 
            R -1, 0,-3,-4, 0,-3,-2, 0,-3, 0, 2,-2,-1, 0, 0,-2, 1, 5,-1,-1, 0,-3,-3, 0,-2, 0 
            S  1, 0,-1, 0, 0,-2, 0,-1,-2, 0, 0,-2,-1, 1, 0,-1, 0,-1, 4, 1, 0,-2,-3, 0,-2, 0 
            T -1, 0,-1, 1, 0,-2, 1, 0,-2, 0, 0,-2,-1, 0, 0, 1, 0,-1, 1, 4, 0,-2,-3, 0,-2, 0 
            U  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0    
            V  0, 0,-1,-3,-2,-1,-3,-3, 3, 0,-2, 1, 1,-3, 0,-2,-2,-3,-2,-2, 0, 4,-3, 0,-1, 0 
            W -3, 0,-2,-4,-3, 1,-2,-2,-3, 0,-3,-2,-1,-4, 0,-4,-2,-3,-3,-3, 0,-3,11, 0, 2, 0 
            X  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0 
            Y -2, 0,-2,-3,-2, 3,-3, 2,-1, 0,-2,-1,-1,-2, 0,-3,-1,-2,-2,-2, 0,-1, 2, 0, 7, 0 
            Z  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5 
            
            Also, because the matrix above has negative value and positive value, in order to easy calculate the distance,
            setting all value into positive. Since the value is in [-4,11], so transfer it into [0,15]
            Then the final using Blosum62 matrix is as below:
            
               A  B  C  D  E  F  G  H  I  J  K  L  M  N  O  P  Q  R  S  T  U  V  W  X  Y  Z
            A  8, 4, 4, 2, 3, 2, 4, 2, 3, 4, 3, 3, 3, 3, 4, 3, 3, 3, 5, 3, 4, 2, 1, 4, 2, 4
            B  4, 9, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4
            C  4, 4,13, 1, 0, 2, 1, 1, 3, 4, 1, 3, 3, 1, 4, 1, 1, 1, 3, 3, 4, 3, 2, 4, 2, 4
            D  2, 4, 1,10, 6, 1, 3, 3, 1, 4, 3, 0, 1, 5, 4, 3, 4, 2, 4, 5, 4, 1, 0, 4, 1, 4
            E  3, 4, 0, 6, 9, 1, 2, 4, 1, 4, 5, 1, 2, 4, 4, 3, 6, 4, 4, 4, 4, 1, 1, 4, 2, 4
            F  2, 4, 2, 1, 1,10, 1, 3, 4, 4, 1, 4, 4, 1, 4, 0, 1, 1, 2, 2, 4, 3, 5, 4, 7, 4
            G  4, 4, 1, 3, 2, 1,10, 2, 0, 4, 2, 0, 1, 2, 4, 2, 2, 2, 4, 5, 4, 4, 2, 4, 1, 4
            H  2, 4, 1, 5, 4, 3, 2,12, 1, 4, 3, 1, 2, 5, 4, 2, 4, 4, 3, 4, 4, 2, 2, 4, 6, 4
            I  3, 4, 3, 1, 1, 4, 0, 1, 8, 4, 1, 6, 5, 1, 4, 1, 1, 1, 2, 2, 4, 5, 1, 4, 3, 4
            J  4, 4, 4, 4, 4, 4, 4, 4, 4, 9, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4
            K  3, 4, 1, 3, 5, 1, 2, 3, 1, 4, 9, 2, 3, 4, 4, 3, 5, 6, 4, 4, 4, 1, 1, 4, 2, 4
            L  3, 4, 3, 0, 1, 4, 0, 1, 6, 4, 2, 8, 6, 1, 4, 1, 2, 2, 2, 2, 4, 7, 2, 4, 3, 4
            M  3, 4, 3, 1, 2, 4, 1, 2, 5, 4, 3, 6, 9, 2, 4, 2, 4, 3, 3, 3, 4, 2, 3, 4, 3, 4
            N  2, 4, 1, 5, 4, 1, 4, 3, 1, 4, 4, 1, 2,10, 4, 2, 4, 4, 5, 4, 4, 1, 0, 4, 2, 4
            O  4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 9, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4
            P  3, 4, 1, 3, 3, 0, 2, 2, 1, 4, 3, 1, 2, 3, 4,11, 3, 2, 3, 5, 4, 2, 0, 4, 1, 4
            Q  3, 4, 1, 4, 6, 1, 2, 4, 1, 4, 5, 2, 4, 4, 4, 3, 9, 5, 4, 4, 4, 2, 2, 4, 3, 4
            R  3, 4, 1, 0, 4, 1, 2, 4, 1, 4, 6, 2, 3, 4, 4, 2, 5, 9, 3, 3, 4, 1, 1, 4, 2, 4
            S  5, 4, 3, 4, 4, 2, 4, 3, 2, 4, 4, 2, 3, 5, 4, 3, 4, 3, 8, 5, 4, 2, 1, 4, 2, 4
            T  3, 4, 3, 5, 4, 2, 5, 4, 2, 4, 4, 2, 3, 4, 4, 5, 4, 3, 5, 8, 4, 2, 1, 4, 2, 4
            U  4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 9, 4, 4, 4, 4, 4
            V  4, 4, 3, 1, 2, 3, 1, 1, 7, 4, 2, 5, 5, 1, 4, 2, 2, 1, 2, 2, 4, 8, 1, 4, 3, 4
            W  1, 4, 2, 0, 1, 5, 2, 2, 1, 4, 1, 2, 3, 0, 4, 0, 2, 1, 1, 1, 4, 1,15, 4, 6, 4
            X  4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 9, 4, 4
            Y  2, 4, 2, 1, 2, 7, 1, 6, 3, 4, 2, 3, 3, 2, 4, 1, 3, 2, 2, 2, 4, 3, 6, 4,11, 4
            Z  4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 9
            
        1.2. To insertion & deletion parameter, use the average substitution score for each letter in Blosum62 matrix
            For example,
                To letter A:
                   A  B  C  D  E  F  G  H  I  J  K  L  M  N  O  P  Q  R  S  T  U  V  W  X  Y  Z
                A  8, 4, 4, 2, 3, 2, 4, 2, 3, 4, 3, 3, 3, 3, 4, 3, 3, 3, 5, 3, 4, 2, 1, 4, 2, 4
                
                max( A ) ---> 8 ( A ---> A ),   min( A ) ---> 1 ( A --->W )
                So, the insertion and deletion cost will be: round( ( max(A) + min(A) ) / 2 )
                Cost(insertion,deletion) = round( (8+1)/2 ) = 5
        
    2. Read data from data set:
        pNames: represents the list of Persian Names
        lNames: represents the list of Latin Names
        
    3. For each Persian name in train.txt, calculating the GED distance between it and all the Latin names in name.txt.
       Aim to find the Latin name with "best GED distance" 
    
    4. Write the results to the specific file.
'''
def selfwrite_blosum62_GED():
    
    # Step 1.2: Set Blosum62 substitution matrix:
    # Firstly modify the matrix:
    ori_blosum62 = [
        [ 4, 0, 0,-2,-1,-2, 0,-2,-1, 0,-1,-1,-1,-1, 0,-1,-1,-1, 1,-1, 0,-2,-3, 0,-2, 0 ],
        [ 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
        [ 0, 0, 9,-3,-4,-2,-3,-3,-1, 0,-3,-1,-1,-3, 0,-3,-3,-3,-1,-1, 0,-1,-2, 0,-2, 0 ],
        [-2, 0,-3, 6, 2,-3,-1,-1,-3, 0,-1,-4,-3, 1, 0,-1, 0,-2, 0, 1, 0,-3,-4, 0,-3, 0 ],
        [-1, 0,-4, 2, 5,-3,-2, 0,-3, 0, 1,-3,-2, 0, 0,-1, 2, 0, 0, 0, 0,-3,-3, 0,-2, 0 ],
        [-2, 0,-2,-3,-3, 6,-3,-1, 0, 0,-3, 0, 0,-3, 0,-4,-3,-3,-2,-2, 0,-1, 1, 0, 3, 0 ],
        [ 0, 0,-3,-1,-2,-3, 6,-2,-4, 0,-2,-4,-3,-2, 0,-2,-2,-2, 0, 1, 0, 0,-2, 0,-3, 0 ],   
        [-2, 0,-3, 1, 0,-1,-2, 8,-3, 0,-1,-3,-2, 1, 0,-2, 0, 0,-1, 0, 0,-2,-2, 0, 2, 0 ],
        [-1, 0,-1,-3,-3, 0,-4,-3, 4, 0,-3, 2, 1,-3, 0,-3,-3,-3,-2,-2, 0, 1,-3, 0,-1, 0 ],
        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ], 
        [-1, 0,-3,-1, 1,-3,-2,-1,-3, 0, 5,-2,-1, 0, 0,-1, 1, 2, 0, 0, 0,-3,-3, 0,-2, 0 ],
        [-1, 0,-1,-4,-3, 0,-4,-3, 2, 0,-2, 4, 2,-3, 0,-3,-2,-2,-2,-2, 0, 3,-2, 0,-1, 0 ],
        [-1, 0,-1,-3,-2, 0,-3,-2, 1, 0,-1, 2, 5,-2, 0,-2, 0,-1,-1,-1, 0,-2,-1, 0,-1, 0 ],
        [-2, 0,-3, 1, 0,-3, 0,-1,-3, 0, 0,-3,-2, 6, 0,-2, 0, 0, 1, 0, 0,-3,-4, 0,-2, 0 ],
        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],        
        [-1, 0,-3,-1,-1,-4,-2,-2,-3, 0,-1,-3,-2,-1, 0, 7,-1,-2,-1, 1, 0,-2,-4, 0,-3, 0 ],
        [-1, 0,-3, 0, 2,-3,-2, 0,-3, 0, 1,-2, 0, 0, 0,-1, 5, 1, 0, 0, 0,-2,-2, 0,-1, 0 ],
        [-1, 0,-3,-4, 0,-3,-2, 0,-3, 0, 2,-2,-1, 0, 0,-2, 1, 5,-1,-1, 0,-3,-3, 0,-2, 0 ],
        [ 1, 0,-1, 0, 0,-2, 0,-1,-2, 0, 0,-2,-1, 1, 0,-1, 0,-1, 4, 1, 0,-2,-3, 0,-2, 0 ],
        [-1, 0,-1, 1, 0,-2, 1, 0,-2, 0, 0,-2,-1, 0, 0, 1, 0,-1, 1, 4, 0,-2,-3, 0,-2, 0 ],
        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0 ],   
        [ 0, 0,-1,-3,-2,-1,-3,-3, 3, 0,-2, 1, 1,-3, 0,-2,-2,-3,-2,-2, 0, 4,-3, 0,-1, 0 ],
        [-3, 0,-2,-4,-3, 1,-2,-2,-3, 0,-3,-2,-1,-4, 0,-4,-2,-3,-3,-3, 0,-3,11, 0, 2, 0 ],
        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0 ], 
        [-2, 0,-2,-3,-2, 3,-3, 2,-1, 0,-2,-1,-1,-2, 0,-3,-1,-2,-2,-2, 0,-1, 2, 0, 7, 0 ],
        [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5 ], 
    ]
    
    # Secondly modified the Blosum62 matrix:
    ori_blosum62 = [[ ori_blosum62[ row ][ col ]+4 for col in range(26)] for row in range(26) ]
    
    # Step 1.2: Set the cost or deletion and insertion
    letter_empty_average = [[0 for col in range(1)] for row in range(26)]
    for i in range(26):
        letter_empty_average[ i ] = ( min(ori_blosum62[i]) + max(ori_blosum62[i]))/2
    
    # Step 2:
    pNames = f1.readlines()
    lNames = f2.readlines()
    
    # Step 3:
    for pName in pNames:
     
        maxDistance = -10000
        matchNames = ''
           
        pName = pName.replace(pName," "+pName)
        index = pName.find('\t')
        pName = pName[0:index]
        pName = pName.lower()
        
        for lName in lNames:
         
            lName = lName.replace(lName," "+lName)  
            index = lName.find('\n')
            lName = lName[0:index]
              
            lenP = len( pName )
            lenL = len( lName ) 
            distanceG = [[0 for i in range(lenL) ] for i in range(lenP)] 
            distanceG[ 0 ][ 0 ] = 0
            for i in range(1,lenL):
                x = ord( lName[ i ] ) - 97
                if x<0:
                    x = 0
                distanceG[ 0 ][ i ] = distanceG[ 0 ][ i-1 ] - letter_empty_average[ x ]
            for i in range(1,lenP):
                x = ord( pName[i] ) - 97
                if x<0:
                    x = 0
                distanceG[ i ][ 0 ] = distanceG[ i-1 ][ 0 ] - letter_empty_average[ x ]
            
            for i in range(1,lenP):
                x = ord( pName[i] ) - 97
                if x < 0:
                    x = 0
                for j in range(1,lenL):
                    y = ord( lName[j] ) - 97
                    if y < 0:
                        y = 0
                    if pName[ i ] == lName[ j ]:
                        distanceG[ i ][ j ] = max(
                        distanceG[ i-1 ][ j-1 ] + ori_blosum62[ y ][ x ],
                        distanceG[ i-1 ][ j ] - letter_empty_average[x],
                        distanceG[ i ][ j-1 ] - letter_empty_average[y]
                    )
                    else:
                        distanceG[ i ][ j ] = max(
                        distanceG[ i-1 ][ j-1 ] + ori_blosum62[ y ][ x ] - ori_blosum62[ y ][ y ],
                        distanceG[ i-1 ][ j ] - letter_empty_average[x],
                        distanceG[ i ][ j-1 ] - letter_empty_average[y]
                    )
            if distanceG[ lenP-1 ][ lenL-1 ] > maxDistance:
                maxDistance = distanceG[ lenP-1 ][ lenL-1 ]
                matchName = lName
        
        matchName = matchName[1:]           
        pName = pName[1:].upper()
        print pName+"\t", matchName
        
        # Step 4:
        f7.write(pName + "\t" + matchName + "\n")
    f7.close()
    
'''
    Method 6/7/8: Implement 100/500/1000 lines trained substitution matrix + Self-Write GED Method:       
    
    1. Set different weight to different parameters:
        
        1.1. To match & replace parameter, use the value in the following substitution score matrix 
        
        Take trained 100 lines matrix as example:
        The initial trained score matrix is as below:
            A    B   C    D   E   F    G   H    I   J    K    L    M    N    O   P  Q    R    S    T    U   V   W  X   Y   Z
        A 763,   4,  3,   3, 31,  0,   2,  3,  43,  0,   1,   3,   1,   4,  82,  0, 0,   7,  47,   2,  65,  0,  2, 0, 16,  1 
        B   3, 147,  0,   0,  3,  0,   0,  0,   0,  0,   0,   0,   0,   0,   1,  0, 0,   0,   1,   0,   1,  0,  1, 0,  0,  0 
        C   0,   0,  2,   0,  0,  0,   0,  1,   0,  0,   0,   0,   0,   0,   0,  0, 0,   0,   0,   0,   0,  0,  0, 0,  0,  0 
        D   0,   0,  0, 226,  4,  0,   1,  0,   1,  1,   0,   0,   0,   0,   0,  0, 0,   0,   0,   0,   1,  0,  0, 0,  0,  0 
        E   0,   0,  0,   0,  0,  0,   0,  0,   0,  0,   0,   0,   0,   0,   0,  0, 0,   0,   0,   0,   0,  0,  0, 0,  0,  0 
        F   0,   0,  0,   0,  0, 68,   0,  0,   0,  1,   0,   0,   0,   0,   0,  0, 0,   0,   0,   0,   0,  1,  0, 0,  0,  0 
        G   3,   0,  0,   0,  3,  0, 142,  0,   2,  0,   0,   4,   0,   2,   0,  0, 2,   0,   0,   0,   0,  0,  0, 0,  0,  0 
        H   3,   0,  0,   0, 22,  0,   0, 70,   0,  0,   0,   0,   0,   0,   0,  0, 0,   0,   0,   0,   0,  0,  0, 0,  0,  0 
        I   0,   0,  0,   0,  0,  0,   0,  0,   0,  0,   0,   0,   0,   0,   0,  0, 0,   0,   0,   0,   0,  0,  0, 0,  0,  0 
        J   1,   0,  0,   0,  5,  0,   7,  0,   0, 44,   0,   0,   0,   0,   0,  0, 0,   0,   0,   0,   0,  0,  0, 0,  0,  0 
        K   2,   0, 79,   0,  8,  0,   0,  0,   3,  0, 173,   0,   0,   1,   2,  0, 8,   1,   0,   0,   3,  0,  2, 3,  0,  0 
        L   5,   0,  0,   0, 12,  0,   0,  0,   1,  0,   0, 278,   0,   0,   1,  0, 0,   1,   0,   1,   0,  0,  0, 0,  0,  0 
        M   3,   0,  0,   0,  3,  0,   0,  0,   2,  0,   0,   0, 219,   0,   0,  0, 0,   0,   0,   0,   0,  0,  0, 0,  0,  0 
        N   2,   0,  1,   1, 14,  0,   8,  0,   2,  0,   0,   1,   0, 466,   2,  0, 0,   1,   1,   4,   0,  0,  0, 0,  0,  0 
        O   0,   0,  0,   0,  0,  0,   0,  0,   0,  0,   0,   0,   0,   0,   0,  0, 0,   0,   0,   0,   0,  0,  0, 0,  0,  0 
        P   1,   0,  0,   0,  4,  0,   0,  0,   1,  0,   0,   1,   0,   0,   0, 84, 0,   0,   0,   0,   0,  0,  0, 0,  0,  0  
        Q   0,   0,  0,   0,  0,  0,   0,  0,   0,  0,   2,   0,   0,   0,   0,  0, 0,   0,   0,   0,   0,  0,  0, 0,  0,  0 
        R   4,   1,  0,   0,  8,  0,   1,  0,  10,  0,   1,   0,   0,   3,   2,  0, 0, 365,   1,   0,   0,  0,  0, 0,  0,  1 
        S   2,   1,  9,   0,  6,  0,   1,  0,   1,  0,   5,   5,   3,   6,   2,  4, 1,   0, 250,  26,   1,  0,  1, 4,  0,  0 
        T   5,   0,  0,   0, 10,  0,   0,  4,   3,  3,   0,   0,   0,   0,   5,  0, 0,   4,   2, 202,   2,  0,  0, 0,  0,  1 
        U   0,   0,  0,   0,  0,  0,   0,  0,   0,  0,   0,   0,   0,   0,   0,  0, 0,   0,   0,   0,   0,  0,  0, 0,  0,  0 
        V   6,   2,  0,   1, 16,  2,   0,  0,   2,  0,   0,   6,   4,   2, 310,  1, 2,   8,   3,   2, 134, 49, 60, 2,  0,  0 
        W   0,   0,  0,   0,  0,  0,   0,  0,   0,  0,   0,   0,   0,   0,   0,  0, 0,   0,   0,   0,   0,  0,  0, 0,  0,  0 
        X   0,   0,  0,   0,  0,  0,   0,  0,   0,  0,   0,   0,   0,   0,   0,  0, 0,   0,   0,   0,   0,  0,  0, 0,  0,  0 
        Y  22,   1,  3,   4, 80,  1,   3,  0, 447,  0,   4,   9,   1,  21,   2,  2, 0,  11,   5,  11,  18,  3,  1, 0, 98,  4 
        Z   4,   1,  0,   0,  2,  0,   0,  0,   0,  4,   0,   0,   0,   0,   0,  0, 0,   0,  29,   0,   0,  0,  0, 0,  0, 44 
        
        A problem with the matrix above is that the value in it is very uneven, For example, sometimes up to 763, 
        and sometimes down to 0. So modified into [1,26], The final used matrix is as below:
        Note: although this will cue down some of the relationship information, but it's still working as well.
           A   B   C   D   E   F   G   H   I   J   K   L   M   N   O   P   Q   R   S   T   U   V   W   X   Y   Z
        A 26,  1,  1,  1,  2,  1,  1,  1,  2,  1,  1,  1,  1,  1,  4,  1,  1,  1,  3,  1,  3,  1,  1,  1,  2,  1 
        B  2, 26,  1,  1,  2,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 
        C  1,  1, 26,  1,  1,  1,  1, 14,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 
        D  1,  1,  1, 26,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 
        E  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 
        F  1,  1,  1,  1,  1, 26,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 
        G  2,  1,  1,  1,  2,  1, 26,  1,  1,  1,  1,  2,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 
        H  2,  1,  1,  1,  9,  1,  1, 26,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 
        I  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 
        J  2,  1,  1,  1,  4,  1,  5,  1,  1, 26,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 
        K  1,  1, 12,  1,  2,  1,  1,  1,  1,  1, 26,  1,  1,  1,  1,  1,  2,  1,  1,  1,  1,  1,  1,  1,  1,  1 
        L  1,  1,  1,  1,  2,  1,  1,  1,  1,  1,  1, 26,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 
        M  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 26,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 
        N  1,  1,  1,  1,  2,  1,  1,  1,  1,  1,  1,  1,  1, 26,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 
        O  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 
        P  1,  1,  1,  1,  2,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 26,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 
        Q  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 26,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 
        R  1,  1,  1,  1,  2,  1,  1,  1,  2,  1,  1,  1,  1,  1,  1,  1,  1, 26,  1,  1,  1,  1,  1,  1,  1,  1 
        S  1,  1,  2,  1,  2,  1,  1,  1,  1,  1,  2,  2,  1,  2,  1,  1,  1,  1, 26,  4,  1,  1,  1,  1,  1,  1 
        T  2,  1,  1,  1,  2,  1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  1,  1,  1,  1, 26,  1,  1,  1,  1,  1,  1 
        U  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 
        V  1,  1,  1,  1,  2,  1,  1,  1,  1,  1,  1,  1,  1,  1, 26,  1,  1,  2,  1,  1, 12,  5,  6,  1,  1,  1 
        W  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 
        X  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 
        Y  2,  1,  1,  1,  5,  1,  1,  1, 26,  1,  1,  2,  1,  2,  1,  1,  1,  2,  1,  2,  2,  1,  1,  1,  6,  1 
        Z  3,  2,  1,  1,  2,  1,  1,  1,  1,  3,  1,  1,  1,  1,  1,  1,  1,  1, 17,  1,  1,  1,  1,  1,  1, 26 
               
            
        1.2. To insertion & deletion parameter, use the average substitution score for each letter in above matrix
        
    2. Read data from data set:
        pNames: represents the list of Persian Names
        lNames: represents the list of Latin Names
        
    3. For each Persian name in train.txt, calculating the GED distance between it and all the Latin names in name.txt.
       Aim to find the Latin name with "best GED distance" 
    
    4. Write the results to the specific file.
'''
# Step 1.1:
improvedMatrix_100_Modified = [
    [ 26,  1,  1,  1,  2,  1,  1,  1,  2,  1,  1,  1,  1,  1,  4,  1,  1,  1,  3,  1,  3,  1,  1,  1,  2,  1 ],
    [  2, 26,  1,  1,  2,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  1,  1, 26,  1,  1,  1,  1, 14,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  1,  1,  1, 26,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  1,  1,  1,  1,  1, 26,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  2,  1,  1,  1,  2,  1, 26,  1,  1,  1,  1,  2,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  2,  1,  1,  1,  9,  1,  1, 26,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  2,  1,  1,  1,  4,  1,  5,  1,  1, 26,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  1,  1, 12,  1,  2,  1,  1,  1,  1,  1, 26,  1,  1,  1,  1,  1,  2,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  1,  1,  1,  1,  2,  1,  1,  1,  1,  1,  1, 26,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 26,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  1,  1,  1,  1,  2,  1,  1,  1,  1,  1,  1,  1,  1, 26,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  1,  1,  1,  1,  2,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 26,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 26,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  1,  1,  1,  1,  2,  1,  1,  1,  2,  1,  1,  1,  1,  1,  1,  1,  1, 26,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  1,  1,  2,  1,  2,  1,  1,  1,  1,  1,  2,  2,  1,  2,  1,  1,  1,  1, 26,  4,  1,  1,  1,  1,  1,  1 ],
    [  2,  1,  1,  1,  2,  1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  1,  1,  1,  1, 26,  1,  1,  1,  1,  1,  1 ],
    [  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  1,  1,  1,  1,  2,  1,  1,  1,  1,  1,  1,  1,  1,  1, 26,  1,  1,  2,  1,  1, 12,  5,  6,  1,  1,  1 ],
    [  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  2,  1,  1,  1,  5,  1,  1,  1, 26,  1,  1,  2,  1,  2,  1,  1,  1,  2,  1,  2,  2,  1,  1,  1,  6,  1 ],
    [  3,  2,  1,  1,  2,  1,  1,  1,  1,  3,  1,  1,  1,  1,  1,  1,  1,  1, 17,  1,  1,  1,  1,  1,  1, 26 ]
]

improvedMatrix_500_Modified = [
    [ 26,  1,  1,  1,  2,  1,  1,  1,  2,  1,  1,  1,  1,  1,  4,  1,  1,  1,  2,  1,  3,  1,  1,  1,  1,  1 ],
    [  1, 26,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  1,  1,  4,  1,  1,  1,  1, 26,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  3,  1,  1,  1,  1,  1,  1 ],
    [  1,  1,  1, 26,  2,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  1,  1,  1,  1,  1, 26,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  1,  1,  1,  1,  2,  1, 26,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  2,  1,  1,  1,  7,  1,  1, 26,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  1,  1,  1,  1,  2,  1,  6,  1,  1, 26,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  1,  1, 14,  1,  2,  1,  1,  1,  1,  1, 26,  1,  1,  1,  1,  1,  3,  1,  1,  1,  1,  1,  1,  2,  1,  1 ],
    [  1,  1,  1,  1,  2,  1,  1,  1,  1,  1,  1, 26,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 26,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  1,  1,  1,  1,  2,  1,  1,  1,  1,  1,  1,  1,  1, 26,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  1,  1,  1,  1,  2,  1,  1,  1,  1,  1,  1,  1,  1,  1,  2, 26,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 26,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 26,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  1,  1,  3,  1,  2,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  1,  1, 26,  3,  1,  1,  1,  2,  1,  1 ],
    [  1,  1,  1,  1,  2,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 26,  1,  1,  1,  1,  1,  1 ],
    [  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  1,  1,  1,  1,  2,  1,  1,  1,  1,  1,  1,  1,  1,  1, 26,  1,  1,  1,  1,  1, 12,  5,  6,  1,  1,  1 ],
    [  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  2,  1,  1,  1,  5,  1,  1,  1, 26,  1,  1,  1,  1,  2,  1,  1,  1,  1,  2,  1,  2,  1,  1,  1,  7,  1 ],
    [  2,  1,  1,  1,  2,  1,  1,  1,  1,  2,  1,  1,  1,  1,  1,  1,  1,  1, 20,  1,  1,  1,  1,  1,  1, 26 ]
]  

improvedMatrix_1000_Modified = [
    [ 26,  1,  1,  1,  2,  1,  1,  1,  3,  1,  1,  1,  1,  1,  3,  1,  1,  1,  2,  1,  3,  1,  1,  1,  1,  1 ],
    [  1, 26,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  1,  1, 11,  1,  1,  1,  1, 26,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  3,  1,  1,  1,  1,  1,  1 ],
    [  1,  1,  1, 26,  2,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  1,  1,  1,  1,  1, 26,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  1,  1,  1,  1,  2,  1, 26,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  2,  1,  1,  1,  8,  1,  1, 26,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  1,  1,  1,  1,  2,  1,  6,  1,  1, 26,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  1,  1, 15,  1,  2,  1,  1,  1,  1,  1, 26,  1,  1,  1,  1,  1,  3,  1,  1,  1,  1,  1,  1,  2,  1,  1 ],
    [  1,  1,  1,  1,  2,  1,  1,  1,  1,  1,  1, 26,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 26,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  1,  1,  1,  1,  2,  1,  1,  1,  1,  1,  1,  1,  1, 26,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  1,  1,  1,  1,  2,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 26,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 21,  1,  1,  1,  1,  1, 26,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 26,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  1,  1,  3,  1,  2,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  1,  1, 26,  3,  1,  1,  1,  2,  1,  1 ],
    [  2,  1,  1,  1,  2,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1, 26,  1,  1,  1,  1,  1,  1 ],
    [  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  1,  1,  1,  1,  2,  1,  1,  1,  1,  1,  1,  1,  1,  1, 26,  1,  1,  2,  1,  1, 12,  5,  6,  1,  1,  1 ],
    [  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  1,  1,  1,  1,  1,  1,  1, 26,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1 ],
    [  2,  1,  1,  1,  6,  1,  1,  1, 26,  1,  1,  1,  1,  2,  1,  1,  1,  1,  2,  1,  2,  1,  1,  1,  7,  1 ],
    [  2,  1,  1,  1,  3,  1,  1,  1,  1,  2,  1,  1,  1,  1,  1,  1,  1,  1, 21,  1,  1,  1,  1,  2,  1, 26 ]
]

def selfwrite_trainedMatrix_GED( trainedMatrix, method ):
    # Step 1.2:
    letter_empty_average = [[0 for col in range(1)] for row in range(26)]
    for i in range(26):
        letter_empty_average[ i ] = ( min(trainedMatrix[i]) + max(trainedMatrix[i]))/2
    
    # Step 2:
    pNames = f1.readlines()
    lNames = f2.readlines()
    
    # Step 3:
    for pName in pNames:
     
        maxDistance = -10000
        matchNames = ''
           
        pName = pName.replace(pName," "+pName)
        index = pName.find('\t')
        pName = pName[0:index]
        pName = pName.lower()
            
        for lName in lNames:
         
            lName = lName.replace(lName," "+lName)  
            index = lName.find('\n')
            lName = lName[0:index]
              
            lenP = len( pName )
            lenL = len( lName )      
            distanceG = [[0 for i in range(lenL) ] for i in range(lenP)] 
            distanceG[ 0 ][ 0 ] = 0
            for i in range(1,lenL):
                x = ord( lName[ i ] ) - 97
                if x<0:
                    x = 0
                distanceG[ 0 ][ i ] = distanceG[ 0 ][ i-1 ] - letter_empty_average[ x ]
            for i in range(1,lenP):
                x = ord( pName[i] ) - 97
                if x<0:
                    x = 0
                distanceG[ i ][ 0 ] = distanceG[ i-1 ][ 0 ] - letter_empty_average[ x ]
                
            for i in range(1,lenP):
                x = ord( pName[i] ) - 97
                if x < 0:
                    x = 0
                for j in range(1,lenL):
                    y = ord( lName[j] ) - 97
                    if y < 0:
                        y = 0
                    if pName[ i ] == lName[ j ]:
                        distanceG[ i ][ j ] = max(
                        distanceG[ i-1 ][ j-1 ] + trainedMatrix[ y ][ x ],
                        distanceG[ i-1 ][ j ] - letter_empty_average[x],
                        distanceG[ i ][ j-1 ] - letter_empty_average[y]
                    )
                    else:
                        distanceG[ i ][ j ] = max(
                        distanceG[ i-1 ][ j-1 ] + trainedMatrix[ y ][ x ] - trainedMatrix[ y ][ y ],
                        distanceG[ i-1 ][ j ] - letter_empty_average[x],
                        distanceG[ i ][ j-1 ] - letter_empty_average[y]
                    )
            if distanceG[ lenP-1 ][ lenL-1 ] > maxDistance:
                maxDistance = distanceG[ lenP-1 ][ lenL-1 ]
                matchName = lName
        
        matchName = matchName[1:]           
        pName = pName[1:].upper()
        print pName+"\t", matchName
        
        # Step 4:
        if method == 100:
            f8.write(pName + "\t" + matchName + "\n")
        elif method == 500:
            f9.write(pName + "\t" + matchName + "\n")
        else:
            f10.write(pName + "\t" + matchName + "\n")
    if method == 100:
        f8.close()
    elif method == 500:
        f9.close()
    else:
        f10.close()

'''
    Method 9: Implement 1000 lines trained substitution matrix + Self-Write GED Method + Multiple output:       
    
    1. Set different weight to different parameters:
        
        1.1. To match & replace parameter, use the value in the following substitution score matrix        
        1.2. To insertion & deletion parameter, use the average substitution score for each letter in above matrix
        
    2. Read data from data set:
        pNames: represents the list of Persian Names
        lNames: represents the list of Latin Names
        
    3. For each Persian name in train.txt, calculating the GED distance between it and all the Latin names in name.txt.
       Aim to find all the Latin names with "best GED distance" 
       
       Note: return all match Latin names not just random one.
    
    4. Write the results to the specific file.
'''
def selfwrite_trainedMatrix_GED_Multi( trainedMatrix ):
    # Step 1:
    letter_empty_average = [[0 for col in range(1)] for row in range(26)]
    for i in range(26):
        letter_empty_average[ i ] = ( min( trainedMatrix[i] ) + max( trainedMatrix[i] ))/2
    
    # Step 2:
    pNames = f1.readlines()
    lNames = f2.readlines()

    # Step 3:
    for pName in pNames:
         
        maxDistance = -10000
        matchNames = []
           
        pName = pName.replace(pName," "+pName)
        index = pName.find('\t')
        pName = pName[0:index]
        pName = pName.lower()
        
        for lName in lNames:
         
            lName = lName.replace(lName," "+lName)  
            index = lName.find('\n')
            lName = lName[0:index]
   
            lenP = len( pName )
            lenL = len( lName )      
            distanceG = [[0 for i in range(lenL) ] for i in range(lenP)]     
            distanceG[ 0 ][ 0 ] = 0
            for i in range(1,lenL):
                x = ord( lName[ i ] ) - 97
                if x<0:
                    x = 0
                distanceG[ 0 ][ i ] = distanceG[ 0 ][ i-1 ] - letter_empty_average[ x ]
            for i in range(1,lenP):
                x = ord( pName[i] ) - 97
                if x<0:
                    x = 0
                distanceG[ i ][ 0 ] = distanceG[ i-1 ][ 0 ] - letter_empty_average[ x ]
                
            for i in range(1,lenP):
                x = ord( pName[i] ) - 97
                if x < 0:
                    x = 0
                for j in range(1,lenL):
                    y = ord( lName[j] ) - 97
                    if y < 0:
                        y = 0
                    if pName[ i ] == lName[ j ]:
                        distanceG[ i ][ j ] = max(
                        distanceG[ i-1 ][ j-1 ] + trainedMatrix[ y ][ x ],
                        distanceG[ i-1 ][ j ] - letter_empty_average[x],
                        distanceG[ i ][ j-1 ] - letter_empty_average[y]
                    )
                    else:
                        distanceG[ i ][ j ] = max(
                        distanceG[ i-1 ][ j-1 ] + trainedMatrix[ y ][ x ] - trainedMatrix[ y ][ y ],
                        distanceG[ i-1 ][ j ] - letter_empty_average[x],
                        distanceG[ i ][ j-1 ] - letter_empty_average[y]
                    )     
            if distanceG[ lenP-1 ][ lenL-1 ] > maxDistance:
                maxDistance = distanceG[ lenP-1 ][ lenL-1 ]
                matchNames = []
                matchNames.append( lName )
            elif distanceG[ lenP-1 ][ lenL-1 ] == maxDistance:
                matchNames.append( lName )
                     
        pName = pName[1:].upper()
        print pName+"\t",
         
        # Step 4:
        f11.write(pName)
        count = 0
        lenC = len(matchNames)
        for matchName in matchNames:
            matchName = matchName[1:]

            count += 1
            if count != lenC:
                print matchName + " ",
            else:
                print matchName,
            f11.write("\t"+matchName)
        print   
        f11.write("\n")
    f11.close()
    
'''
    Method 9: Implement 1000 lines trained substitution matrix + Self-Write GED Method + Multiple output:       
    
    1. Set different weight to different parameters:
        
        1.1. To match & replace parameter, use the value in the following substitution score matrix        
        1.2. To insertion & deletion parameter, use the average substitution score for each letter in above matrix
    
    2. Set suitable translating table for first letter:
        From Soudex algorithm, we know that the first letter is very important in the translation,
        So, I build a translating table from the observing the wrong prediction names. 
        For example,
            The name which is named with first letter 'v', are more possible to translate to the name with first letter 'w' ...etc
            Part of the examples:
                vytvl whitwell
                vyt waite
                vyt wheat
                vyt wiebe
                vytykr whitaker
                vytyk wittick
                vytyngtvn whittington
                vytz waites
                vyvr weaver
                vyvvr wiewer
            
        According to above relationships, the final first letter translating table is like:
            
            a ---->   a/e/i/o/s/u        n ---->   n/k
            c ---->   c/s/g              q ---->   q/g
            d ---->   d/b/t/z            r ---->   r/k/v
            f ---->   f/p                s ---->   s/c/t
            g ---->   g/q                v ---->   v/w
            h ---->   h/d/r              x ---->   k
            j ---->   j/g/t/d            y ---->   y/u/i
            k ---->   k/c/q              z ---->   z/j
        
    3. Read data from data set:
        pNames: represents the list of Persian Names
        lNames: represents the list of Latin Names
        
    4. For each Persian name in train.txt, calculating the GED distance between it and all the Latin names 
       not only in names.txt, but also it is satisfied with the first letter translating table.
       Aim to find all the Latin names with "best GED distance" 
       
       Note: return all match Latin names not just random one.
    
    5. Write the results to the specific file.
'''     
def selfwrite_trainedMatrix_GED_Multi_Soundex( trainedMatrix ):
    # Step 1:
    letter_empty_average = [[0 for col in range(1)] for row in range(26)]
    for i in range(26):
        letter_empty_average[ i ] = ( min( trainedMatrix[i]) + max( trainedMatrix[i]) )/2
    
    # Step 2:
    translatingTable = [
        [ 1,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,0,0 ],
        [ 0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 ],
        [ 0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0 ],
        [ 0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1 ],
        [ 0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 ],
        [ 0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0 ],
        [ 0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0 ],
        [ 0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0 ],
        [ 0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 ],
        [ 0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0 ],
        [ 0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0 ],
        [ 0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0 ],
        [ 0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0 ],
        [ 0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0 ],
        [ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0 ],
        [ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0 ],
        [ 0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0 ],
        [ 0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0 ],
        [ 0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0 ],
        [ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0 ],
        [ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0 ],
        [ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0 ],
        [ 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0 ],
        [ 0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 ],
        [ 0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0 ],
        [ 0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1 ]
    ]
      
    # Step 3:
    pNames = f1.readlines()
    lNames = f2.readlines()

    # Step 4:
    for pName in pNames:
         
        maxDistance = -10000
        matchNames = []
           
        pName = pName.replace(pName," "+pName)
        index = pName.find('\t')
        pName = pName[0:index]
        pName = pName.lower()
        t1 = ord(pName[1]) - 97
        if t1 < 0:
            t1 = 0
            
        for lName in lNames:
         
            lName = lName.replace(lName," "+lName)  
            index = lName.find('\n')
            lName = lName[0:index]
            t2 = ord(lName[1]) - 97
            if t2 < 0:
                t2 = 0
          
            # Just calculating the names satisfied with the translating table:
            if translatingTable[ t1 ][ t2 ] == 1:
             
                lenP = len( pName )
                lenL = len( lName )        
                distanceG = [[0 for i in range(lenL) ] for i in range(lenP)]
                distanceG[ 0 ][ 0 ] = 0
                for i in range(1,lenL):
                    x = ord( lName[ i ] ) - 97
                    if x<0:
                        x = 0
                    distanceG[ 0 ][ i ] = distanceG[ 0 ][ i-1 ] - letter_empty_average[ x ]
                for i in range(1,lenP):
                    x = ord( pName[i] ) - 97
                    if x<0:
                        x = 0
                    distanceG[ i ][ 0 ] = distanceG[ i-1 ][ 0 ] - letter_empty_average[ x ]
                
                for i in range(1,lenP):
                    x = ord( pName[i] ) - 97
                    if x < 0:
                        x = 0
                    for j in range(1,lenL):
                        y = ord( lName[j] ) - 97
                        if y < 0:
                            y = 0
                        if pName[ i ] == lName[ j ]:
                            distanceG[ i ][ j ] = max(
                            distanceG[ i-1 ][ j-1 ] + trainedMatrix[ y ][ x ],
                            distanceG[ i-1 ][ j ] - letter_empty_average[x],
                            distanceG[ i ][ j-1 ] - letter_empty_average[y]
                        )
                        else:
                            distanceG[ i ][ j ] = max(
                            distanceG[ i-1 ][ j-1 ] + trainedMatrix[ y ][ x ] - trainedMatrix[ y ][ y ],
                            distanceG[ i-1 ][ j ] - letter_empty_average[x],
                            distanceG[ i ][ j-1 ] - letter_empty_average[y]
                        )   
                if distanceG[ lenP-1 ][ lenL-1 ] > maxDistance:
                    maxDistance = distanceG[ lenP-1 ][ lenL-1 ]
                    matchNames = []
                    matchNames.append( lName )
                elif distanceG[ lenP-1 ][ lenL-1 ] == maxDistance:
                    matchNames.append( lName )
                     
        pName = pName[1:].upper()
        print pName+"\t", 
        
        # Step 5:
        f12.write(pName)
        count = 0
        lenC = len(matchNames)
        for matchName in matchNames:
            matchName = matchName[1:]
            count += 1
            if count != lenC:
                print matchName + " ",
            else:
                print matchName,
            f12.write("\t"+matchName)
        print   
        f12.write("\n")
    f12.close()

'''
    Now you can test each method above:
    1. GED self-write
    2. GED system
    3. LED self-write
    4. 2-Gram self-write
    5. Blosum62Matrix + GED self-write
    6. 100linesTrainedMatrix + GED self-write
    7. 500linesTrainedMatrix + GED self-write
    8. 1000linesTrainedMatrix + GED self-write
    9. 1000linesTrainedMatrix + GED + MultipleMatches self-write
   10. 1000linesTrainedMatrix + GED + MultipleMatches + "Soundex" self-write  
'''
# Method 1
selfwrite_GED( )
# Method 2
system_GED( )
# Method 3
selfwrite_LED( )
# Method 4
selfwrite_2Gram( )
# Method 5
selfwrite_blosum62_GED( )
# Method 6
selfwrite_trainedMatrix_GED( improvedMatrix_100_Modified, 100 )
# Method 7
selfwrite_trainedMatrix_GED( improvedMatrix_500_Modified, 500 )
# Method 8
selfwrite_trainedMatrix_GED( improvedMatrix_1000_Modified, 1000 )
# # Method 9
selfwrite_trainedMatrix_GED_Multi( improvedMatrix_1000_Modified )
# Method 10
selfwrite_trainedMatrix_GED_Multi_Soundex( improvedMatrix_1000_Modified )

# Close the Files:
f1.close()
f2.close()
