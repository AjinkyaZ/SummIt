### Libraries
# Standard library
import string

# Third-party libraries
import bs4
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
import nltk.data
from textrank import split_into_sentences

def get_article_data(link, bs_article_object):
    """Parses each article, given a BeautifulSoup article object (html).
    Returns source name, article body text and url to main image,
    following rules corresponding to source URL
    """
    print link
    if "cnn.com" in link:
        source = "CNN"
        container = bs_article_object.find('div', {'class': 'l-container'})
        body_text = ["".join(x.findAll(text=True)) for x in container.findAllNext(
            "div", {'class': 'zn-body__paragraph'})]
        body_text_temp = (' ').join(body_text)
        body_text = split_into_sentences(body_text_temp)
        for sent_index in range(len(body_text)):
            if "(CNN)" in body_text[sent_index]:
                body_text[sent_index] = string.replace(body_text[sent_index], "(CNN)", "")
            if "READ:" in body_text[sent_index]:
                body_text[sent_index] = string.replace(body_text[sent_index], "READ:", "")
            if "MORE:" in body_text[sent_index]:
                body_text[sent_index] = string.replace(body_text[sent_index], "MORE:", "")
            if "Read more:" in body_text[sent_index]:
                body_text[sent_index] = string.replace(body_text[sent_index], "Read more:", "")
        try:
            image_set = bs_article_object.find(
                'img', {'class': 'media__image'})
            image_source = image_set['src']
            if "data:image/gif;base64" in image_source:
                image_source = image_set['data-src-medium']
        except KeyError, e:
            print "Exception encountered! \n", e
            image_source = 'default.png'
        except TypeError, e:
            print "Exception encountered! \n", e
            image_source = 'default.png'

    elif "reuters.com" in link:
        source = "Reuters"
        container = bs_article_object.find('span', {'id': 'articleText'})
        # body_text = ["".join(x.findAll(text=True)) for x in container.findAllNext("p")]
        article_text = container.text
        body_text = split_into_sentences(article_text)
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
            print "Exception encountered! \n", e
            image_source = 'default.png'
        except TypeError, e:
            print "Exception encountered! \n", e
            image_source = 'default.png'
        except AttributeError, e:
            print "Exception encountered! \n", e
            image_source = 'default.png'

    elif "economictimes.indiatimes" in link:
        source = "Economic Times"
        container = bs_article_object.find('div', {'class': 'Normal'})
        article_text = container.text
        body_text = split_into_sentences(article_text)
        try:
            image_cont = bs_article_object.find('figure')
            image_tag = image_cont.find('img')
            image_source = image_tag['src']
        except KeyError, e:
            print "Exception encountered! \n", e
            image_source = 'default.png'
        except TypeError, e:
            print "Exception encountered! \n", e
            image_source = 'default.png'
        except AttributeError, e:
            print "Exception encountered! \n", e
            image_source = 'default.png'

    elif "fossbytes.com" in link:
        source = "FossBytes"
        container = bs_article_object.find('div', {'class':'su-column-inner'})
        article_text = container.text
        body_text = split_into_sentences(article_text)
        try:
            image_tag = bs_article_object.find('img', {'class':'size-full'})
            image_source = image_tag['src']
        except KeyError, e:
            print "Exception encountered! \n", e
            image_source = 'default.png'
        except TypeError, e:
            print "Exception encountered! \n", e
            image_source = 'default.png'
        except AttributeError, e:
            print "Exception encountered! \n", e
            image_source = 'default.png'
    data = (source, body_text, image_source)
    return data
