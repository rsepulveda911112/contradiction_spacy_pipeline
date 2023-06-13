import requests
from bs4 import BeautifulSoup
url_wordreference = "https://www.wordreference.com/sinonimos/"


def get_thesaurus(word):
    bs = None
    response = requests.get(url_wordreference + word)
    if response.status_code == 200:
        data = response._content
        bs = BeautifulSoup(data, "html.parser")
    return bs


def get_parser(bs):
    synonyms = []
    antonyns = []
    if bs:
        section = bs.find('div', {'class': 'trans clickable'})
        if section:
            ul = section.find('ul')
            ui = ul.findAll('li')
            for li in ui:
                if li.find('span'):
                    span = li.next
                    list_an = span.text.split(':')
                    antonyns.extend(list_an[1].split(','))
                else:
                    synonyms.extend(li.text.split(','))
    return synonyms, antonyns


def get_synonym_antonyns(word):
    bs = get_thesaurus(word)
    return get_parser(bs)

