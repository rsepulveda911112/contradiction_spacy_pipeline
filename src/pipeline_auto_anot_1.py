import os
import spacy
import pandas as pd
import json
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher
from spacy.language import Language
from spacy.tokens import Doc
from src.component.pattern import MonthsPattern, DaysPattern, OrdinalsPattern, CardinalsPattern, \
    TrimestresPattern, DigitsPattern, TimePattern, SemestresPattern
from src.component.ParserComponent import ParserComponent
from src.component.verb_pattern import VerbsPattern

# f = open(os.getcwd()+'/data/anotar/web_crawler_economia_100_62.json','r')
# datas = []
# datas.extend(json.load(f))
# df = pd.DataFrame(datas)
nlp = spacy.load("es_core_news_lg")

# We're using a component factory because the component needs to be
# initialized with the shared vocab via the nlp object
@Language.factory("months_merger")
def create_months_pattern_merger(nlp, name):
    return MonthsPattern(nlp.vocab, nlp)

@Language.factory("days_merger")
def create_days_pattern_merger(nlp, name):
    return DaysPattern(nlp.vocab, nlp)

@Language.factory("ordinals_merger")
def create_ordinals_pattern_merger(nlp, name):
    return OrdinalsPattern(nlp.vocab, nlp)

@Language.factory("cardinals_merger")
def create_cardinals_pattern_merger(nlp, name):
    return CardinalsPattern(nlp.vocab, nlp)

@Language.factory("trimestres_merger")
def create_trimestres_pattern_merger(nlp, name):
    return TrimestresPattern(nlp.vocab, nlp)

@Language.factory("digits_merger")
def create_digits_pattern_merger(nlp, name):
    return DigitsPattern(nlp.vocab, nlp)

@Language.factory("times_merger")
def create_times_pattern_merger(nlp, name):
    return TimePattern(nlp.vocab, nlp)

@Language.factory("semestres_merger")
def create_semestres_pattern_merger(nlp, name):
    return SemestresPattern(nlp.vocab, nlp)

@Language.factory("parser_component")
def create_parser_merger(nlp, name):
    return ParserComponent(nlp)

@Language.factory("verb_component")
def create_verb_merger(nlp, name):
    return VerbsPattern(nlp.vocab, nlp)

nlp.add_pipe("times_merger", last=True)
nlp.add_pipe("days_merger", last=True)
nlp.add_pipe("ordinals_merger", last=True)
nlp.add_pipe("cardinals_merger", last=True)
nlp.add_pipe("trimestres_merger", last=True)
nlp.add_pipe("digits_merger", last=True)
nlp.add_pipe('semestres_merger', last=True)
nlp.add_pipe('parser_component', last=True)
nlp.add_pipe('verb_component', last=True)


dir_files = os.getcwd()+'/data/anotar/'
dir_files_an = os.getcwd()+'/data/anotados/'

for file in os.listdir(dir_files):
    df = pd.read_json(dir_files+file)
    with open(dir_files_an + os.path.splitext(os.path.basename(file))[0] +'_anotado_spacy' +'.json', "w+") as f:
        docs = []
        for index, row in df.iterrows():
            doc = nlp(row['headline'])
            docs.append({'doc': doc.to_json(["days_pattern", "ordinals_pattern", "cardinals_pattern",
                                             "trimestres_pattern", "digits_pattern", "time_pattern",
                                             "semestres_pattern", "parser_doc", 'main_nouns', 'verbs_pattern'])})
        df_doc = pd.DataFrame(data=docs)
        df = pd.concat([df, df_doc], axis=1)
        values = df.to_dict('records')
        f.write(json.dumps(values, indent=4))
