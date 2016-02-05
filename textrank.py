from nltk.tokenize.punkt import PunktSentenceTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
import networkx as nx
from networkx import drawing
import matplotlib.pyplot as plt



#def pagerank():
    # to-do

def textrank(doc):
    # print doc
    tokenizer = PunktSentenceTokenizer()
    # print "Tokenizer, ", tokenizer
    doclist = tokenizer.tokenize(doc)
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


def gen_summary(docu):
    textrankres = textrank(docu)
    summindices = textrankres[0]
    summsents = textrankres[1]
    summary = ""
    #d = int(raw_input("enter summary len in sentences\n"))
    d = 4
    if d > len(summsents):
        print "Invalid"
    else:
        for i in range(d):
            index = summindices[i]
            summary += summsents[index]
        return summary


def main():
    docu = """
Beirut, Lebanon (CNN)It's a pretty normal bus -- windows slightly cracked, dust, the occasional button missing on the dashboard. But when its passengers say they take it knowing they could be on a one-way ticket to death, they aren't exaggerating. From the dark and dank underpass that is Charles Helou bus station in central Beirut, leaves the bus to Raqqa. It has done so for years, but now that Raqqa is the capital of ISIS' self-declared caliphate, the bus crosses the most dangerous border in the world. And people do pay to get on it. In a 24-hour journey, it travels from Beirut, across the border to regime-held Damascus. Then it heads to Palmyra, held by ISIS, before moving north toward Raqqa. The nine passengers we met were adamant about two things. First that ISIS would most likely let them in to Raqqa. That suggests they know someone there, and they didn't want to go into details. Second, nobody wanted to have their face filmed or name used.  The fear was overpowering and that permeates exactly how you get ready for the trip.  Last cigarettes are smoked. Not as people worry they may not survive the trip, but because ISIS has banned smoking. They've also banned music, and much else that's part of normal lifestyles in the modern world. If you break their atavistic, moral code, you can be flogged, even beheaded.  Read: The terrifying reality of living under ISIS in Raqqa ISIS checks So there is a strange cleansing process on the ride. Smokers douse their fingers in perfume and jettison their cigarettes. Music, racy pictures, numbers of friends close to the Syrian regime -- all are deleted from mobile phones. ISIS check these things thoroughly. The manager of the bus explains the rules for the trip, though it's a journey he never makes.  "A woman that's not dressed right will be sent to Islamic training," he said. "She, of course, needs a male relative to escort her. Men need to leave their beards grown long in their natural state, with mustaches trimmed. Trousers should not be tight and a certain height over shoes. But ISIS realizes when people travel, they can't always look like that, so it's OK." The bus always comes back empty. ISIS rarely lets people out. Which begs the question, why are they surrendering themselves to life under ISIS? Surely they know what they are getting in to? One group of passengers has a specific reason to travel. They are accompanying the body of their relative back to be buried in his hometown. Some shed tears. He died of a heart attack. The process of repatriation is a nightmare. The bus's eventual departure will be delayed, we learn later, by 24 hours, because they have to wait for the appropriate paperwork to be able to take the body out of Lebanon. Dangers The hazards of the route are relayed in the most matter-of-fact chatter.  Sometimes a fighter jet will buzz the coach, flying low. Sometimes the buses are hit by sniper fire. Most of the time they keep on driving.  The manager tells us: "A plane might [drop a bomb] some distance from the bus. It's normal! No one can really pin down where the sniper fire is coming from. That's when the passengers get afraid." Can people ever leave Raqqa on the bus? We hear two stories that suggest it is possible. One man tells us the sick are sometimes given 15 days' leave to seek medical treatment. If they come back late, their property and home is confiscated by ISIS. A woman, we are told, has a daughter in Raqqa, who she is trying to get out. When we talk to her, she insists she has been on a trip to the Gulf region and is just on her way home. Dissimilation is a necessary part of life on this bus. One man tells us, though, of his sorrow for his hometown, where his children have not left the house in the daytime to go to school for four years.  "It used to be my heaven," he says, before ISIS rule. The war against them, the poverty that it caused and now even the trash littering the streets "has made it my hell." 
    """
    print "Article text"
    print docu
    print "Summary\n"
    print gen_summary(docu)


if __name__ == "__main__":
    main()
