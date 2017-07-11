This tarball contains eight files (plus this README), in three types, as follows:

{train,dev,test}-tweets.txt: These files contain the raw text of the tweets, one tweet per line, in the following format:
tweet-id TAB tweet-text NEWLINE
Note that the text was pre-processed (folding case, and removing all characters that are not alphabetic ([a-z])) before feature engineering/selection was performed.

{train,dev}-labels.txt: These files contain the manually--assigned sentiment labels, one tweet per line, in the following format:
tweet-id TAB label NEWLINE
The labels are one of "positive", "negative", or "neutral". Note that you will not be given labels for the test data, but you can submit to Kaggle In-class to find the accuracy of your system.

{train,dev,test}.arff: These files combine the information contained within the previous two files. We applied feature selection to generate the frequencies of the best 46 tokens in the training data, and then summarised in a format suitable as input to Weka. (http://www.cs.waikato.ac.nz/ml/weka/)
The ARFF file contains a header, with the following format:
@RELATION twitter-sent-top20	# This is simply a name for the dataset.
@ATTRIBUTE id NUMERIC		# Each of the 48 attributes has a line,
@ATTRIBUTE a NUMERIC		# One for the tweet ID, and
@ATTRIBUTE amazing NUMERIC	# 46 for the (numeric) token frequencies.
@ATTRIBUTE antman NUMERIC	# By convention, the class is given last
@ATTRIBUTE are NUMERIC
@ATTRIBUTE at NUMERIC
@ATTRIBUTE awesome NUMERIC
...
@ATTRIBUTE sentiment {positive,negative,neutral}
@DATA				# This is the final line in the header
The rest of the lines represent the instances, in CSV format.
Note that Weka will insist that the headers are _exactly_ the same; otherwise, it will refuse to evaluate the model and/or predict the classes of the test instances.

