import pymongo as pm
import networkx as nx
from networkx import drawing
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from collections import Counter
from datetime import datetime

client = pm.MongoClient('localhost', 3001)
db = client.feeds_database
articles = db.articles
article_list = articles.find()

documents = []
for article in article_list:
    documents.append(article['Body'])

n = len(documents)
documents_termlists = []
documents_termfreqs = [Counter() for i in range(n)]
G = [[] for i in range(n)]
start = datetime.now()
for i in range(n):
    print len(documents[i])
    G[i] = nx.Graph()
    for j in documents[i]:
        G[i].add_node(j)
    docu_str = (',').join(documents[i])
    # print docu_str
    docu_terms = docu_str.split()
    # print docu_terms
    stop = stopwords.words('english')  # list of stopwords
    docu_terms = docu_terms.split()
    remove_punc = dict((ord(char), None) for char in ",.!?(){}")
    docu_terms_filtered = [term.translate(remove_punc) for term in docu_terms if term not in stop]
    # for i in docu_terms_filtered:
    #    print i
    documents_termlists.append(docu_terms_filtered)
    for term in documents_termlists[i]:
    	term = term
    	documents_termfreqs[i][term]+=1

    # print docu_terms
    #nx.draw_networkx(G[i], arrows=True, with_labels=True)
    # plt.show()

print documents_termfreqs[4]
print datetime.now()-start