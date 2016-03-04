import bs4
import string
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
import nltk.data


def splitsentences(text):
    #tknz_params = PunktParameters()
    #tknz_params.abbrev_types = set(['dr','mr','mrs', 'ms','cpt','U.S.','U.K.'])
    #tknz = PunktSentenceTokenizer(tknz_params)
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    sents = sent_detector.tokenize(text)
    return sents


def get_article_data(link, bs_article_object):
    print link
    if "cnn.com" in link:
        source = "CNN"
        container = bs_article_object.find('div', {'class': 'l-container'})
        body_text = ["".join(x.findAll(text=True)) for x in container.findAllNext(
            "p", {'class': 'zn-body__paragraph'})]
        body_text_buffer = []
        for sent_index in range(len(body_text)):
            if "(CNN)" in body_text[sent_index]:
                body_text[sent_index] = string.replace(body_text[sent_index], "(CNN)", "")
            if "READ:" in body_text[sent_index]:
                continue
        try:
            image_set = bs_article_object.find(
                'img', {'class': 'media__image'})
            image_source = image_set['src']
            if "data:image/gif;base64" in image_source:
                image_source = image_set['data-src-medium']
        except KeyError, e:
            image_source = 'default.png'
        except TypeError, e:
            image_source = 'default.png'

    elif "reuters.com" in link:
        source = "Reuters"
        container = bs_article_object.find('span', {'id': 'articleText'})
        #body_text = ["".join(x.findAll(text=True)) for x in container.findAllNext("p")]
        article_text = container.text
        body_text = splitsentences(article_text)
        try:
            image_cont = bs_article_object.find('div', {'class':'related-photo-container'})
            print type(image_cont)
            if image_cont is None:
                image_cont = bs_article_object.find('div', {'class':'module-slide-media'})
                image_tag = image_cont.find('img')
                image_source = image_tag['data-lazy']
            else:
               image_tag = image_cont.find('img')
               image_source = image_tag['src']
        except KeyError, e:
            image_source = 'default.png'
        except TypeError, e:
            image_source = 'default.png'
        except AttributeError, e:
            image_source = 'default.png'

    elif "nytimes.com" in link:
        source = "NY Times"
        container = bs_article_object.find('div', {'class':'story-body'})
        body_text = [" ".join(x.findAll(text=True)) for x in container.findAllNext("p")]
        try:
            image_cont = bs_article_object.find('div',{'class':'image'})
            image_tag = image_cont.find('img')
            image_src = image_tag['data-mediaviewer-src']
        except KeyError, e:
            image_source = 'default.png'
        except TypeError, e:
            image_source = 'default.png'
        except AttributeError, e:
            image_source = 'default.png'
    data = (source, body_text, image_source)
    return data
