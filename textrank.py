from nltk.tokenize.punkt import PunktSentenceTokenizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from nltk.corpus import stopwords
from collections import Counter
from math import log10, log
from networkx import drawing
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np



#def pagerank():
    # to-do

def similarity(s1, s2):
    s1 = s1.split()
    #print "s1 ---", s1
    s2 = s2.split()
    #print "s2 ---", s2
    terms_s1 = set(s1) #eliminate duplicates
    terms_s2 = set(s2)
    #print log(len(terms_s1)), log(len(terms_s2))
    common_terms = terms_s1.intersection(terms_s2)
    #print "len comm terms", len(common_terms)
    if (log(len(terms_s1))+log(len(terms_s2)))==0: sim = 0.001
    else:
        sim = len(common_terms)/(log10(len(terms_s1))+log10(len(terms_s2)))
    return sim

def getsortedsents(inputscores):
    n = len(inputscores)
    scorelist = []
    for i in range(n):
        scorelist.append((i, inputscores[i])) #list of tuples with sentence index and its ranking
    scoressorted = sorted(scorelist, key=lambda x: x[1], reverse=True)
    #for i in scoressorted: print i
    sortedsents = [scoressorted[i][0] for i in range(n)] #get sorted sentence indices
    sortedsents.remove(max(sortedsents)) #remove sentence index corresponding to title, (last since it was appended later)
    return sortedsents


def textrank(doc, title):
    if "(CNN)" in doc:
       doc = doc.strip("(CNN)") #remove that irritating (CNN) tag
    pstoken = PunktSentenceTokenizer()
    doclist = pstoken.tokenize(doc) #split into sentences
    doclist.append(title) #append title to list for additional info
    n = len(doclist)
    #for i in range(n):
    #    print i, "-->", doclist[i]
    #print "\n\n"
    stoplist = stopwords.words('english')
    #print stoplist, "\n\n"
    doclist_nostop = doclist[:]  #create working copy of doclist
    removed_stops = doclist[:]
    #the below statements remove all stopwords from every sentence in the list
    #the sentences were split into separate terms and reconstructed without stopwords
    #stopword removal is significantly affecting performance (better summaries!)
    for i in range(n):
        doclist_nostop[i] = [term for term in doclist[i].split() if term.lower() not in stoplist]
        doclist_nostop[i] = (' ').join(doclist_nostop[i])
        removed_stops[i] = [term for term in doclist[i].split() if term.lower() in stoplist]
        removed_stops[i] = (' ').join(removed_stops[i])
        #print i, "-->", doclist_nostop[i]
    sim_arr = [[1 for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(n):
            sim_arr[i][j]=float("{0:.4f}".format(float(similarity(doclist_nostop[i], doclist_nostop[j])))) #scale to 4 decimals
    for i in range(n):
        minVal = min(sim_arr[i])
        maxVal = max(sim_arr[i])
        #print i, minVal, maxVal
        sim_arr[i] = [(q-minVal)/(maxVal-minVal) for q in sim_arr[i]] #normalize between 0 and 1 
    docmatrix = np.array(sim_arr)
    dg = nx.from_numpy_matrix(docmatrix)
    scores = nx.pagerank(dg)
    sortedsents = getsortedsents(scores)
    return (sortedsents, doclist)





def textrank_tfidf(doc):
    # print doc
    tokenizer = PunktSentenceTokenizer()
    # print "Tokenizer, ", tokenizer
    docterms = word_tokenize(doc)
    stoplist = stopwords.words('english')
    docterms_nostop = [term.lower() for term in docterms if term not in stoplist]
    doclist = tokenizer.tokenize(doc)
    #print docterms_nostop
    # print "Doc list: ", doclist
    vectorizer = TfidfVectorizer()
    # print "Vectorizer:", vectorizer
    docvectors = vectorizer.fit_transform(doclist)
    # print "Docvectors", docvectors
    # print "Docvectors array", docvectors.toarray()
    docmatrix = docvectors*docvectors.T
    # print "Docmatrix", docmatrix
    # print "Docmatrix array", docmatrix.toarray()
    docgraph = nx.from_scipy_sparse_matrix(docmatrix)
    # print docgraph
    scores = nx.pagerank(docgraph)
    n = len(scores)
    scorelist = []
    for i in range(n):
        scorelist.append((i, scores[i]))
    scoressorted = sorted(scorelist, key=lambda x: x[1], reverse=True)
    sortedsents = [scoressorted[i][0] for i in range(n)]
    return (sortedsents, doclist)


def gen_summary(docu, title):
    textrankres = textrank(docu, title)
    summindices = textrankres[0]
    summsents = textrankres[1]
    summary = ""
    #d = int(raw_input("enter summary len in sentences\n"))
    d = 3
    if d > len(summsents):
        print "Invalid"
    else:
        for i in range(d):
            index = summindices[i]
            summary += " "+summsents[index]
        return summary


def main():
    text = """(CNN)After eluding capture for years, two Mafia bosses have been arrested in an underground bunker in southern Italy.   Police seized mobsters Giuseppe Ferraro, 47, and Giuseppe Crea, 37,  in Calabria region Friday, according to Italian news agency Ansa.  Ferraro was found guilty of murder and Mafia association decades ago, and had been a fugitive since 1998. Crea was convicted of Mafia association and had been on the run for nine years, according to the news agency. Their hideout had an array of weapons, including rifles, pistols and machine guns. "Today is another great day for everyone and for the country because justice has won," Interior Minister Angelino Alfano said after their arrest.  Beyond Italian borders The two men are part of 'Ndrangheta, a dangerous criminal organization that has tentacles worldwide. The group is based in Calabria, where the two men were arrested.   'Ndrangheta's power has grown beyond Italian borders.  Two years ago, Italian officials said the group is linked to drug trafficking  in South and Central America, Canada and the United States.  The 'Ndrangheta was formed in the 1860s, and is involved in kidnappings, corruption, drug trafficking, gambling and murders, according to the FBI.  It has between 100-200 members in the United States, mostly in New York and Florida.  Opinion: Will Mafia ever loosen its grip on Italy? """
    title = """Italian police arrest 2 fugitive Mafia bosses in underground bunker"""
    print "Article text"
    print text
    print "Summary\n"
    print gen_summary(text, title)


if __name__ == "__main__":
    main()
