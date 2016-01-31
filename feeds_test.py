import feedparser
import bs4
import urllib2
from datetime import datetime
import json
import pymongo as pm
from hashlib import md5
import textrank


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
        article_id = md5(article_title).hexdigest()
        if "cnn.com" in article_link:
            article_src = "CNN"
            try:
                image_set = parsed_article.find(
                    'img', attrs={'class': 'media__image'})
                image_src = image_set['data-medium-src']
            except KeyError, e:
                image_src = 'dota.jpg'
            except TypeError, e:
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
            image_src = 'dota.jpg'

        if len(article_body) < 12:  # article is too short
            print "length of article insufficient"
            continue

        body_text_str = ' '.join(article_body)
        #body_text_final = body_text_str.encode("utf-8")
        article_summary = textrank.gen_summary(body_text_str)
        # for i in range(15):
        #   article_text[article_num][i]=parsed_article.p.text
        #   print article_text[article_num][i]

        yield {
            'ID': article_id,
            'Title': article_title,
            'Body': article_body,
            'Summary': article_summary,
            'Link': article_link,
            'Source': article_src,
            'Image': image_src,
            'Date': date_now
        }


def main():
    # News sources
    #cnn_top = feedparser.parse('http://rss.cnn.com/rss/edition.rss')
    cnn_world = feedparser.parse('http://rss.cnn.com/rss/edition_world.rss')
    cnn_tech = feedparser.parse(
        'http://rss.cnn.com/rss/edition_technology.rss')
    reuters_top = feedparser.parse('http://feeds.reuters.com/reuters/topNews')
    #cnn_sport = feedparser.parse('http://rss.cnn.com/rss/edition_sport.rss')

    # Main code starts here
    src_feed = cnn_world
    len_src_feed = len(src_feed['entries'])
    print "No. of articles in source feed", len_src_feed
    print "Enter no. of articles to parse, must be less than", len_src_feed
    n = int(raw_input())
    start = datetime.now()

    client = pm.MongoClient('localhost', 3001)
    db = client.feeds_database
    articles = db.articles
    db.articles.remove({})
    print db.collection_names()
    # print "Source Feed ", src_feed
    for article in todb_article(src_feed, n):
        article_id = articles.insert_one(article).inserted_id
        print "inserting into db"
        print article['ID']
        print article['Title']
        print article['Image']
        # print article_id
        # print articles.find_one(article_id)
    print datetime.now()-start


if __name__ == "__main__":
    main()
