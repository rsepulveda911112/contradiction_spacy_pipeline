import requests
from bs4 import BeautifulSoup
url_conjugador = "https://conjugador.reverso.net/conjugacion-espanol-verbo-"


def get_conjugador(verb):
    bs = None
    response = requests.get(url_conjugador + verb+ '.html')
    if response.status_code == 200:
        data = response._content
        bs = BeautifulSoup(data, "html.parser")
    return bs


# "Mood=Ind|Number=Sing|Person=3|Tense=Fut|VerbForm=Fin"

# numbers = {'Sing', 'Plur'}
# persons = {'1', '2', '3'}
tenses = {'Pres': 'Presente', 'Fut': 'Futuro', 'Past': 'Pretérito imperfecto'}
verbForms = {'Inf': 'Infinitivo', 'Part': 'Participio Pasado', 'Ger': 'Gerundio'}
moods = {'Ind': 'Indicativo', 'Imp': 'Imperativo', 'Sub': 'Subjuntivo'}


def find_div_by_name(value, divs_list):
    div_value = None
    for div in divs_list:

        if 'mobile-title' in div.contents[0].attrs:
            if value in div.contents[0].attrs['mobile-title']:
                div_value = div
                break
    return div_value


def get_all_element(div, number, person):
    text = ''
    ui_list = div.find_all('li')
    if len(ui_list) == 1:
        text = ui_list[0].text
    else:
        index_person = int(person)-1
        if number == 'Plur':
            index_person = int(person) + 2
        text = ui_list[index_person].contents[1].text
    return text


def get_verb_form(morph, bs):
    verb = ''
    number = ''
    person = ''
    if bs:
        section = bs.find_all('div', {'class': 'wrap-three-col'})
        section = section[4:]
        if 'Mood' in morph.keys():
            mood = ''
            tense = ''
            number = ''
            person = ''
            if morph['Mood'] in moods:
                mood = moods[morph['Mood']]
            if 'Tense' in morph.keys():
                if morph['Tense'] in tenses:
                    tense = tenses[morph['Tense']]
            if 'Number' in morph.keys():
                number = morph['Number']
            if 'Person' in morph.keys():
                person = morph['Person']

            div = find_div_by_name(mood + ' ' + tense, section)
        elif 'VerbForm' in morph.keys():
            verbForm = morph['VerbForm']
            verbForm = verbForms[verbForm]
            div = find_div_by_name(verbForm, section)
        if div:
            verb = get_all_element(div, number, person)
        return verb


def get_verb(word, morph):
    bs = get_conjugador(word)
    return get_verb_form(morph, bs)
# "Mood=Ind|Number=Sing|Person=3|Tense=Fut|VerbForm=Fin"
# print(get_verb('ganar', {"Mood": "Ind", "Number": "Sing", "Person": 3,
#                    "Tense": "Fut", "VerbForm": "Fin"}))