import pymongo as pm

client = pm.MongoClient('localhost', 3001)
db = client.feeds_database
articles = db.articles
article_list = articles.find()

