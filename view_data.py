### Libraries
# Standard library
from collections import defaultdict
import string
import math

# Third-party libraries
import pymongo as pm
from textrank import *


def main():
    """Test program to check/view data stored in the database.
    """
    client = pm.MongoClient('localhost', 3001)
    db = client.feeds_database
    articles = db.articles
    print "collections:"
    for collection in db.collection_names():
        print "---", collection

    print ""
    article_list = articles.find()
    article_list = sorted(article_list)
    aggregate_text = ""
    total_compression_ratio = 0
    processed_articles = 0
    for article in article_list:
        print "********************************************"
        print article['ID'], " : "
        print "Title : ", article['Title']
        # this gets a list containing the body text
        body_text = article['Body']
        # since list output cannot be  formatted as string, we join list elements
        # i.e paragraphs to create text
        body_text_str = ' '.join(body_text)
        # unicode chars throw up probs in python 2.7 (for display), hence the encoding
        body_text_final = body_text_str.encode("utf-8")
        aggregate_text = aggregate_text + str(body_text_final)
        print "Body : ", body_text_final
        print "--------------------------------"
        summary = article['Summary']
        summary = summary.encode("utf-8")
        print "Summary : ", summary
        print "Length of Body (chars) : ", article['Body_Length']
        print "Length of Summary (chars) : ", article['Summary_Length']
 
        total_compression_ratio += article['Compression_Ratio']
        print("Compression achieved : {0:.2f}%").format(article['Compression_Ratio']*100)
        print "--------------------------------"
        print "Link : ", article['Link']
        print "Source : ", article['Source']
        print "Image : ", article['Image']
        print "Date : ", article['Date']
        print ""
        processed_articles +=1
    print "Articles in database :", processed_articles
    print("Average Compression achieved : {0:.2f}%").format((total_compression_ratio/processed_articles)*100)


if __name__ == "__main__":
	main()
