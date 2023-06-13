# from spacy.matcher import PhraseMatcher
from spacy.matcher import Matcher
from spacy.tokens import Token
from spacy.tokens import Doc
from src.update_headlines import months, days, cardinales, ordinales, trimestres
verbs = ['andar', 'seguir', 'venir']


class VerbsPattern:

    def __init__(self, vocab, nlp):
        patterns = [{'POS': 'VERB', 'LEMMA': {"IN": ['comenzar', 'echar', 'empezar', 'liar', 'meter', 'pasar',
                                                     'principiar', 'dar', 'tornar', 'volver', 'venir', 'andar', 'seguir', 'acabar', 'alcanzar',
                                                     'llegar', 'estar', 'termianr', 'dejar', 'llevar', 'quedar', 'tener', 'traer', 'poder',
                                                     'soler', 'querer', 'deber', 'haber']}},
                    {'LEMMA': {"IN": ['a', 'por', 'de', 'que', '']}},
                    {'POS': 'VERB', 'MORPH': {'IS_SUBSET': ["VerbForm=Inf", "VerbForm=Part", "VerbForm=Ger"]}}]
        # , 'MORPH': {'IS_SUBSET': ["VerbForm=Inf", "VerbForm=Part", "VerbForm=Ger"]}
        # {'POS': 'VERB', 'LEMMA': {"IN": ['comenzar', 'echar', 'empezar', 'liar', 'meter', 'pasar',
        #                                   'principiar', 'dar', 'tornar', 'volver', 'venir', 'andar', 'seguir', 'acabar', 'alcanzar',
        #                                   'llegar', 'estar', 'termianr', 'dejar', 'llevar', 'quedar', 'tener', 'traer', 'poder',
        #                                   'soler', 'querer', 'deber', 'haber']}},
        # {'LEMMA': {"IN": ['a', 'por', 'de', 'que', '']}},

        # Register a new token extension to flag bad HTML
        Doc.set_extension("verbs_pattern", default=False)
        # self.matcher = PhraseMatcher(vocab)
        self.matcher = Matcher(vocab)
        self.matcher.add("Verbs_PATTERN", patterns=[patterns])

    def __call__(self, doc):
        # This method is invoked when the component is called on a Doc
        matches = self.matcher(doc)
        # spans_month = [{'start': doc[start:end].start_char, 'end':doc[start:end].end_char} for match_id, start, end in matches(doc)]
        spans = []  # Collect the matched spans here
        spans_month = []
        for match_id, start, end in matches:
            span = doc[start:end]
            spans.append(span)
            spans_month.append({'id': span.start, 'start': span.start_char, 'end':span.end_char})
        doc._.verbs_pattern = spans_month
        # with doc.retokenize() as retokenizer:
        #     for span in spans:
        #         retokenizer.merge(span)
        #         for token in span:
        #             token._.months_pat = True  # Mark token as bad HTML
        return doc






