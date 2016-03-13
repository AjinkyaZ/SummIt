import feedparser
import bs4
import urllib2
from datetime import datetime
import json
import pymongo as pm
from hashlib import md5
import textrank
import parser


def todb_article(source_feed, num_articles):
    titles = {}
    article_text = {}
    date_now = datetime.now()
    date_now = date_now.strftime('%Y-%m-%d')

    for article_num in range(num_articles):
        print "fetching data -- link", (article_num+1)
        article_link = source_feed['entries'][article_num]['link']
        article_main = urllib2.urlopen(article_link).read()
        parsed_article = bs4.BeautifulSoup(article_main, 'html.parser')
        titles[article_num] = parsed_article.h1.text
        article_title = titles[article_num]
        article_title = article_title.encode("utf-8")
        article_id = md5(article_title).hexdigest()

        display_data = parser.get_article_data(article_link, parsed_article)
        article_src = display_data[0]
        article_body = display_data[1]
        image_src = display_data[2]

        if len(article_body) < 10:  # article is too short
            print "length of article insufficient"
            continue

        body_text_str = (" ").join(article_body)
        #body_text_final = body_text_str.encode("utf-8")
        article_summary = textrank.gen_summary(body_text_str, article_title)
        #if summary is too short, skip article
        if len(article_summary) < 200:
            print "summary too short"
            continue
        if len(article_summary) > 1200:
            print "summary too long"
            continue

        len_body_words = textrank.tokencount(body_text_str)
        len_summary_words = textrank.tokencount(article_summary)
        compression_ratio = (len_body_words-len_summary_words)/(len_body_words*1.0)
        # for i in range(15):
        #   article_text[article_num][i]=parsed_article.p.text
        #   print article_text[article_num][i]

        yield {
            'ID': article_id,
            'Title': article_title,
            'Body': article_body,
            'Body_Length': len_body_words,
            'Summary': article_summary,
            'Summary_Length': len_summary_words,
            'Compression_Ratio': compression_ratio,
            'Link': article_link,
            'Source': article_src,
            'Image': image_src,
            'Date': date_now
        }


def main():
    # News sources
    #cnn_top = feedparser.parse('http://rss.cnn.com/rss/edition.rss')
    cnn_world = feedparser.parse('http://rss.cnn.com/rss/edition_world.rss')
    #cnn_tech = feedparser.parse('http://rss.cnn.com/rss/edition_technology.rss')
    reuters_top = feedparser.parse('http://feeds.reuters.com/reuters/INtopNews')
    #cnn_sport = feedparser.parse('http://rss.cnn.com/rss/edition_sport.rss')
    et_top = feedparser.parse('http://economictimes.indiatimes.com/rssfeedstopstories.cms')
    # Main code starts here
    #src_feed = cnn_tech
    start = datetime.now()

    client = pm.MongoClient('localhost', 3001)
    db = client.feeds_database
    articles = db.articles
    db.articles.remove({})
    print db.collection_names()
    # print "Source Feed ", src_feed
    sources = [cnn_world, reuters_top]
    insertcount = 0
    for src_feed in sources:
        len_src_feed = len(src_feed['entries'])
        print "No. of articles in source feed", len_src_feed
        #print "Enter no. of articles to parse, must be less than", len_src_feed
        #n = int(raw_input())
        n=len_src_feed
        for article in todb_article(src_feed, n):
            article_id = articles.insert_one(article).inserted_id
            insertcount += 1
            print "inserting into db"
            print article['ID']
            print article['Title']
            print article['Image']
            # print article_id
            # print articles.find_one(article_id)
    print "Articles parsed : ", n*len(sources)
    print "Articles fetched : ", insertcount
    print "Time taken :", datetime.now()-start


if __name__ == "__main__":
    main()
