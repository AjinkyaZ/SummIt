import pymongo as pm
import networkx as nx
from networkx import drawing
import matplotlib.pyplot as plt
from nltk.corpus import stopwords

client = pm.MongoClient('localhost', 3001)
db = client.feeds_database
articles = db.articles
article_list = articles.find()

documents = []
for article in article_list:
    documents.append(article['Body'])

n = len(documents)
documents_termlists = []
documents_termfreqs = {}
G = [[] for i in range(n)]
for i in range(1):
    print len(documents[i])
    G[i] = nx.Graph()
    for j in documents[i]:
        G[i].add_node(j)
    docu_str = (',').join(documents[i])
    # print docu_str
    docu_terms = docu_str.split()
    #print docu_terms
    stop = stopwords.words('english') #list of stopwords
    docu_terms_filtered = [term.encode("utf-8").translate(None, ",.!?(){}").decode("utf-8") for term in docu_terms if term not in stop]
    #for i in docu_terms_filtered:
    #    print i
    documents_termlists.append(docu_terms_filtered)
    for i in range(1):
    	for j in documents_termlists[i]:
    		print j

    # print docu_terms
    #nx.draw_networkx(G[i], arrows=True, with_labels=True)
    # plt.show()