import pymongo as pm
from collections import defaultdict
import string
import math
from textrank import *


def main():
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
        summary = gen_summary(body_text_str)
        #summary = summary.decode("utf-8")
        print "Summary : ", summary
        print "--------------------------------"
        print "Link : ", article['Link']
        print "Source : ", article['Source']
        print "Image : ", article['Image']
        print "Date : ", article['Date']
        print ""


if __name__ == "__main__":
	main()