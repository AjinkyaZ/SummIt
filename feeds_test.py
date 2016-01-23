import feedparser
import bs4
import urllib2
from datetime import datetime
import json
import pymongo as pm

# News sources
#cnn_top = feedparser.parse('http://rss.cnn.com/rss/edition.rss')
cnn_world = feedparser.parse('http://rss.cnn.com/rss/edition_world.rss')
cnn_tech = feedparser.parse('http://rss.cnn.com/rss/edition_technology.rss')
reuters_top = feedparser.parse('http://feeds.reuters.com/reuters/topNews')
#cnn_sport = feedparser.parse('http://rss.cnn.com/rss/edition_sport.rss')

# Main code starts here
src_feed = cnn_tech
len_src_feed = len(src_feed['entries'])
print len_src_feed

date_now = datetime.now()
date_now = date_now.strftime('%Y-%m-%d')

titles = {}
article_text = {}
start = datetime.now()


def todb_article():
    for article_num in range(5):
        print "fetching data -- link", (article_num+1)
        article_link = src_feed['entries'][article_num]['link']
        article_main = urllib2.urlopen(article_link).read()
        parsed_article = bs4.BeautifulSoup(article_main, 'html.parser')
        titles[article_num] = parsed_article.h1.text
        article_title = titles[article_num]
        if "cnn.com" in article_link:
            article_src = "CNN"
            image_set = parsed_article.find('img', attrs={'class':'media__image'})
            try:
                image_src = image_set['data-medium-src']
            except KeyError, e:
                image_src = 'dota.jpg'
            container = parsed_article.find(
                'div', attrs={'class': 'l-container'})
            article_body = ["".join(x.findAll(text=True)) for x in container.findAllNext(
                "p", attrs={'class': 'zn-body__paragraph'})]
        elif "reuters.com" in article_link:
            article_src = "Reuters"
            container = parsed_article.find(
                'span', attrs={'id': 'articleText'})
            article_body = ["".join(x.findAll(text=True))
                            for x in container.findAllNext("p")]

        # for i in range(15):
        #	article_text[article_num][i]=parsed_article.p.text
        #	print article_text[article_num][i]

        yield {
            'ID': (article_num+1),
            'Title': article_title,
            'Body': article_body,
            'Link': article_link,
            'Source': article_src,
            'Image': image_src,
            'Date': date_now
        }

client = pm.MongoClient('localhost', 3001)
db = client.feeds_database
articles = db.articles
db.articles.remove({})
# print db.collection_names()

for article in todb_article():
    article_id = articles.insert_one(article).inserted_id
    print "inserting into db"
    print article['ID']
    print article['Title']
    print article['Image']
    # print article_id
    # print articles.find_one(article_id)
print datetime.now()-start
