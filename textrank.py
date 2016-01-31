from nltk.tokenize.punkt import PunktSentenceTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
import networkx as nx
from networkx import drawing
import matplotlib.pyplot as plt


def textrank(doc):
    #print doc
    tokenizer = PunktSentenceTokenizer()
    #print tokenizer
    doclist = tokenizer.tokenize(doc)
    #print doclist
    vectorizer = TfidfVectorizer()
    #print vectorizer
    docvectors = vectorizer.fit_transform(doclist)
    #print docvectors
    docmatrix = docvectors*docvectors.T
    #print docmatrix
    docgraph = nx.from_scipy_sparse_matrix(docmatrix)
    #print docgraph
    scores = nx.pagerank(docgraph)
    n = len(scores)
    scorelist = []
    for i in range(n):
        scorelist.append((i, scores[i]))
    scoressorted = sorted(scorelist, key = lambda x:x[1], reverse = True)
    sortedsents = [scoressorted[i][0] for i in range(n)]
    return (sortedsents, doclist)


def gen_summary(docu):
    textrankres = textrank(docu)
    summindices = textrankres[0]
    summsents = textrankres[1]
    summary = ""
    #d = int(raw_input("enter summary len in sentences\n"))
    d=7
    if d>len(summsents):
        print "Invalid"
    else:
        for i in range(d):
            index = summindices[i]
            summary += summsents[index]
        return summary

def main():
    docu = """
(CNN)For 36 days, they were trapped 700 feet underground, dependent on food lowered to them by the rescue workers who were plotting to get them out.,On Friday night, the four remaining miners known to have survived a December 25 mine collapse in eastern China were finally pulled to the surface.,Rescuers pulled the miners one by one from the collapsed gypsum mine in eastern China's Pingyi County, with video showing the cable lifting them by a harness.,The rescues were shown on state-run China Central Television. As one of the miners put his feet back on the surface, workers in orange coats and helmets surrounded him as a crowd of reporters and photographers moved in just behind them to record the spectacle.,The miner was put on a gurney and then into an ambulance.,Information on the miners' conditions wasn't immediately available.,At least 1 dead; 13 others missing,Twenty-nine people were working in the gypsum mine on December 25 when it collapsed, CCTV has reported. At least one died, 11 escaped, and 17 were believed to be trapped underground.,Five days later, rescuers who lowered infrared cameras into the mine found four survivors, CCTV reported.,Through narrow relief holes that were drilled, rescuers lowered food, lamps and clothes to the four. The 13 other miners are still missing.,Over time, rescuers drilled a wide hole toward the four survivors. The rescuers initially planned to lower a man-size capsule to the four, CCTV reported this month.,That would have been similar to a method used in 2010 to rescue 33 miners who were trapped 2,300 feet underground in a Chilean mine for more than two months.,Friday's CCTV footage did not show any capsule as the miners appeared above ground. Rather, the video showed the miners emerging from a hole in a platform over the mine, wearing a harness attached to a cable that was pulling them up.  ,Where the rescued Chilean miners are, 5 years after rescue ,The owner of the mine, Ma Congbo, chief executive of Yurong Trade Co., committed suicide two days after the collapse by jumping into a mine well. Four county-level officials were fired on December 29, one day before the survivors were found, according to Xinhua, the Chinese government news agency. ,CNN's Merieme Arif and Tim Schwarz contributed to this report."""
    print docu
    print gen_summary(docu)


if __name__ == "__main__":
    main()
