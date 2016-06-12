### Libraries
# Standard library
from collections import Counter
from math import log10, log
import re

# Third-party libraries
import nltk.data
from nltk.tokenize import word_tokenize
from stemming.porter2 import stem
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from nltk.corpus import stopwords
from networkx import drawing
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


caps = "([A-Z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov|in)"

def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + caps + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(caps + "[.]" + caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + caps + "[.]"," \\1<prd>",text)
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences


def similarity(s1, s2):
    """Calculates similarity between two sentences, by tokenizing them into words
    and finding intersecting (common) terms. 
    Returns similarity taking into consideration length of both sentences to
    account for long sentences with many terms.
    """
    s1 = s1.split()
    # print "s1 ---", s1
    s2 = s2.split()
    # print "s2 ---", s2
    terms_s1 = set(s1) # eliminate duplicates
    terms_s2 = set(s2)
    # print log(len(terms_s1)), log(len(terms_s2))
    common_terms = terms_s1.intersection(terms_s2)
    # print "len comm terms", len(common_terms)
    if (log(len(terms_s1))+log(len(terms_s2)))==0: sim = 0.001
    else:
        sim = len(common_terms)/(log10(len(terms_s1))+log10(len(terms_s2)))
    return sim

# reference calculations for TF-IDF.. scikit's vectorizer works much better
def term_frequency(term, tokenized_document):
    return tokenized_document.count(term)

def logscaled_term_frequency(term, tokenized_document):
    count = tokenized_document.count(term)
    if count == 0:
        return 0
    else:
        return 1 + math.log(count)

def inverse_document_frequencies(tokenized_documents):
    idf_values = {}
    all_tokens_set = set([item for sublist in tokenized_documents for item in sublist])
    for tkn in all_tokens_set:
        contains_token = map(lambda doc: tkn in doc, tokenized_documents)
        idf_values[tkn] = 1 + math.log(len(tokenized_documents)/(sum(contains_token)))
    return idf_values

def tfidf(documents):
    tokenized_documents = [tokenize(d) for d in documents]
    idf = inverse_document_frequencies(tokenized_documents)
    tfidf_documents = []
    for document in tokenized_documents:
        doc_tfidf = []
        for term in idf.keys():
            tf = logscaled_term_frequency(term, document)
            doc_tfidf.append(tf * idf[term])
        tfidf_documents.append(doc_tfidf)
    return tfidf_documents

def cosine_similarity(vector1, vector2):
    dot_product = sum(p*q for p,q in zip(vector1, vector2))
    magnitude = math.sqrt(sum([val**2 for val in vector1])) * math.sqrt(sum([val**2 for val in vector2]))
    if not magnitude:
        return 0
    return dot_product/magnitude


def getsortedsents(inputscores):
    """Accepts a dictionary consisting of sentence scores ordered by index,
    return sorted indices with decreasing scores. 
    """
    n = len(inputscores)
    scorelist = []
    for i in range(n):
        scorelist.append((i, inputscores[i])) # list of tuples with sentence index and its ranking
    scoressorted = sorted(scorelist, key=lambda x: x[1], reverse=True)
    # for i in scoressorted: print i
    sortedsents = [scoressorted[i][0] for i in range(n)] # get sorted sentence indices
    sortedsents.remove(max(sortedsents)) # remove sentence index corresponding to title, (last since it was appended later)
    return sortedsents


def textrank(doc, title):
    """TextRank implementation that uses word overlap as similarity measure.
    Tokenizes document into sentences, appends title as another sentence,
    and constructs a set of sentences consisting of stemmed words with 
    stopwords and punctuations stripped.
    Calculates similarity for each sentence pair, normalized between 0 and 1.
    After transforming list into a numpy array, converts it to a graph and 
    applies PageRank to get final scores. 
    Returns sorted indices and tokenized sentence list.
    """
    # psparams = PunktParameters()
    # psparams.abbrev_types = set(['dr','mr','mrs', 'ms','U.S.','U.K.'])
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    # pstoken = PunktSentenceTokenizer(psparams)
    doclist = split_into_sentences(doc) # split into sentences
    doclist.append(title) # append title to list for additional info
    n = len(doclist)    # for i in range(n):
    #     print i, "-->", doclist[i]
    # print "\n\n"
    stoplist = stopwords.words('english')
    punclist = [',', '.', ':', ';', '\'', '"', '?', '!', '``', '\'\'', '\'s', '``', '(', ')']
    # print stoplist, "\n\n"
    doclist_nostop = doclist[:]  # create working copy of doclist
    removed_stops = doclist[:]
    # the below statements remove all stopwords from every sentence in the list
    # the sentences were split into separate terms and reconstructed without stopwords
    # stopword removal is significantly affecting performance (better summaries!)
    for i in range(n):
        doclist_nostop[i] = [stem(term.lower()) for term in doclist[i].split() if term.lower() not in stoplist and term not in punclist]
        doclist_nostop[i] = (' ').join(doclist_nostop[i])
        removed_stops[i] = [term for term in doclist[i].split() if term.lower() in stoplist]
        removed_stops[i] = (' ').join(removed_stops[i])
        # print i, "-->", doclist_nostop[i]
    sim_arr = [[1 for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(n):
            sim_arr[i][j]=float("{0:.4f}".format(float(similarity(doclist_nostop[i], doclist_nostop[j])))) # scale to 4 decimals
    for i in range(n):
        minVal = min(sim_arr[i])
        maxVal = max(sim_arr[i])
        # print i, minVal, maxVal
        sim_arr[i] = [(q-minVal)/(maxVal-minVal) for q in sim_arr[i]] # normalize between 0 and 1 
    docmatrix = np.array(sim_arr)
    dg = nx.from_numpy_matrix(docmatrix)
    scores = nx.pagerank(dg)
    sortedsents = getsortedsents(scores)
    return (sortedsents, doclist)





def textrank_tfidf(doc, title):
    """TextRank implementation that uses TF-IDF as similarity measure.
    Tokenizes document into sentences, appends title as another sentence,
    and constructs a set of sentences consisting of stemmed words with 
    stopwords and punctuations stripped.
    Constructs a vectorized representation of the resulting sentence list, 
    Multiplies result with its transpose to obtain a NxN matrix, converting to a graph
    and applying PageRank to obtain final scores. 
    Returns sorted indices and tokenized sentence list.
    """
    # print doc
    # tokenizer = PunktSentenceTokenizer()
    # print "Tokenizer, ", tokenizer
    # docterms = word_tokenize(doc)
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    doclist = split_into_sentences(doc)
    doclist.append(title)
    n = len(doclist)
    stoplist = stopwords.words('english')
    punclist = [',','.',':',';','\'','"','?','``','\'\'','\'s','(',')',"``","`","[","]"]
    doclist_nostop = [0 for i in range(n)]
    for i in range(n):
        doclist_nostop[i] = [stem(term.lower()) for term in doclist[i].split() if term.lower() not in stoplist and term not in punclist]
        doclist_nostop[i] = (' ').join(doclist_nostop[i])
    # print docterms_nostop
    # print "Doc list: ", doclist
    punc_stoplist = punclist+stoplist
    vectorizer = TfidfVectorizer(tokenizer = word_tokenize, ngram_range = (1,3), norm = 'l2')
    #print "Vectorizer:", vectorizer
    docvectors = vectorizer.fit_transform(doclist_nostop)
    # print vectorizer.get_feature_names()
    # print "Docvectors", docvectors
    # print "Docvectors array", docvectors.toarray()
    docmatrix = docvectors*docvectors.T
    # print "Docmatrix", docmatrix
    # print "Docmatrix array", docmatrix.toarray()
    docgraph = nx.from_scipy_sparse_matrix(docmatrix)
    # print docgraph
    scores = nx.pagerank(docgraph)
    sortedsents = getsortedsents(scores)
    return (sortedsents, doclist)


def gen_summary(doc, title, summ_func):
    """Accepts article body, title and summarization function to be used as parameter.
    Constructs summary from list of sorted/ranked sentence indices and corresponding sentences.
    """
    summ_funcres = summ_func(doc, title)
    summindices = summ_funcres[0]
    summsents = summ_funcres[1]
    summary = ""
    # d = int(raw_input("enter summary len in sentences\n"))
    d = 4
    if d > len(summsents):
        print "Invalid"
    else:
        for i in range(d):
            index = summindices[i]
            if len(summary)==0:
                summary += summsents[index]
            else:
                summary += " "+summsents[index]
        return summary


def tokencount(text):
    """Tokenizes entire document (article) into words,
    including stopwords but omitting common punctuations.
    Returns number of such tokens in the document.
    """
    text_tokens = word_tokenize(text)
    punclist = [',','.',':',';','\'','"','?','``','\'\'','\'s']
    text_tokens_nopunc = [term for term in text_tokens if term not in punclist]
    return len(text_tokens_nopunc)


def main():
    text = """After eluding capture for years, two Mafia bosses have been arrested in an underground bunker in southern Italy.   Police seized mobsters Giuseppe Ferraro, 47, and Giuseppe Crea, 37,  in Calabria region Friday, according to Italian news agency Ansa. Ferraro was found guilty of murder and Mafia association decades ago, and had been a fugitive since 1998. Crea was convicted of Mafia association and had been on the run for nine years, according to the news agency. Their hideout had an array of weapons, including rifles, pistols and machine guns. "Today is another great day for everyone and for the country because justice has won," Interior Minister Angelino Alfano said after their arrest.  Beyond Italian borders The two men are part of 'Ndrangheta, a dangerous criminal organization that has tentacles worldwide. The group is based in Calabria, where the two men were arrested.   'Ndrangheta's power has grown beyond Italian borders.  Two years ago, Italian officials said the group is linked to drug trafficking  in South and Central America, Canada and the United States.  The 'Ndrangheta was formed in the 1860s, and is involved in kidnappings, corruption, drug trafficking, gambling and murders, according to the FBI.  It has between 100-200 members in the United States, mostly in New York and Florida.  Opinion: Will Mafia ever loosen its grip on Italy? """
    title = """Italian police arrest 2 fugitive Mafia bosses in underground bunker"""
    # text = raw_input("Enter body text\n")
    # title = raw_input("Enter title\n")
    print "Article text"
    print text
    print "Summary\n"
    summary_function = textrank_tfidf
    print gen_summary(text, title, summary_function)


if __name__ == "__main__":
    main()
