import pymongo as pm
from collections import defaultdict
import string
#import nltk
#from nltk import word_tokenize
import math
#from textblob import TextBlob as tb
#from nltk.corpus import stopwords
# from freqsumm import * 


#def tf(word, blob):
#    return blob.words.count(word) / len(blob.words)
#
#def n_containing(word, bloblist):
#    return sum(1 for blob in bloblist if word in blob)
#
#def idf(word, bloblist):
#    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))
#
#def tfidf(word, blob, bloblist):
#    return tf(word, blob) * idf(word, bloblist)



client = pm.MongoClient('localhost', 3001)
db =  client.feeds_database
articles = db.articles
print "collections:"
for collection in db.collection_names():
    print "---", collection

print ""
article_list = articles.find()
article_list = article_list.sort('ID', 1)
#fs = FrequencySummarizer()
aggregate_text = ""
#doc = ["" for x in xrange(0, 8)]
#print doc
for article in article_list:
	print "********************************************"
	print article['ID'], " : "
	print "Title : ", article['Title']
#this gets a list containing the body text
	body_text = article['Body']
#since list output cannot be  formatted as string, we join list elements i.e paragraphs to create text
	body_text_str = ' '.join(body_text)
#unicode chars throw up probs in python 2.7, hence the encoding
#I can't be bothered with python3.3 , as of now, so not taking that way out
	body_text_final = body_text_str.encode("utf-8")
	aggregate_text = aggregate_text + str(body_text_final)
	print "Body : ", body_text_final
	print "--------------------------------"
	#print "Summary : "
	#summary  = fs.summarize(body_text_final,5)
	#for s in summary:
	#		print s,
	#print ""
	print "Link : ", article['Link']
	print "Source : ", article['Source']
        print "Image : ", article['Image']
	print "Date : ", article['Date']
	print ""


#bloblist = doc[0:]
#for i, blob in enumerate(bloblist):
#    print("Top words in document {}".format(i + 1))
#    scores = {word: tfidf(word, blob, bloblist) for word in blob.words}
#    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
#    for word, score in sorted_words[:3]:
#        print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))


#punc_stripped_text = aggregate_text.translate(string.maketrans("",""), string.punctuation)
#tokenized_text = word_tokenize(punc_stripped_text)
#porter = nltk.PorterStemmer()
#stemmed_text = [porter.stem(t) for t in tokenized_text]

#text = ""
#cachedStopWords = stopwords.words("english")
#text = ' '.join([word for word in stemmed_text if word not in cachedStopWords])
#print text
