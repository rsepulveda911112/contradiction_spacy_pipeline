from spacy.matcher import PhraseMatcher
from spacy.matcher import Matcher
from spacy.tokens import Token
from spacy.tokens import Doc
from src.update_headlines import months, days, cardinales, ordinales, trimestres


class MonthsPattern:

    def __init__(self, vocab, nlp):
        patterns_months = [nlp(month) for month in months]
        # Register a new token extension to flag bad HTML
        Token.set_extension("months_pat", default=False)
        Doc.set_extension("months_pattern", default=False)
        self.matcher = PhraseMatcher(vocab)
        self.matcher.add("Months_PATTERN", patterns_months)

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
        doc._.months_pattern = spans_month
        with doc.retokenize() as retokenizer:
            for span in spans:
                retokenizer.merge(span)
                for token in span:
                    token._.months_pat = True  # Mark token as bad HTML
        return doc


class DaysPattern:

    def __init__(self, vocab, nlp):
        patterns_days = [nlp(day) for day in days]
        # Register a new token extension to flag bad HTML
        Token.set_extension("days_pat", default=False)
        Doc.set_extension("days_pattern", default=False)
        self.matcher = PhraseMatcher(vocab)
        self.matcher.add("Days_PATTERN", patterns_days)

    def __call__(self, doc):
        # This method is invoked when the component is called on a Doc
        matches = self.matcher(doc)
        spans = []  # Collect the matched spans here
        spans_days = []
        for match_id, start, end in matches:
            span = doc[start:end]
            spans.append(span)
            spans_days.append({'id': span.start, 'start': span.start_char, 'end':span.end_char})
        doc._.days_pattern = spans_days
        with doc.retokenize() as retokenizer:
            for span in spans:
                retokenizer.merge(span)
                for token in span:
                    token._.days_pat = True  # Mark token as bad HTML
        return doc


class TimePattern:

    def __init__(self, vocab, nlp):
        pattern = [{'MORPH': "AdvType=Tim"}]
        # Register a new token extension to flag bad HTML
        Doc.set_extension("time_pattern", default=False)
        self.matcher = Matcher(vocab)
        self.matcher.add("times", patterns=[pattern])

    def __call__(self, doc):
        # This method is invoked when the component is called on a Doc
        matches = self.matcher(doc)
        spans = []
        for match_id, start, end in matches:
            span = doc[start:end]
            spans.append({'id': span.start, 'start': span.start_char, 'end': span.end_char})
        doc._.time_pattern = spans
        return doc


class OrdinalsPattern:

    def __init__(self, vocab, nlp):
        pattern = [{'MORPH': "Gender=Masc|NumType=Ord|Number=Sing"}]
        # Register a new token extension to flag bad HTML
        Doc.set_extension("ordinals_pattern", default=False)
        self.matcher = Matcher(vocab)
        self.matcher.add("ordinals", patterns=[pattern])

    def __call__(self, doc):
        # This method is invoked when the component is called on a Doc
        matches = self.matcher(doc)
        spans = []
        for match_id, start, end in matches:
            span = doc[start:end]
            spans.append({'id': span.start, 'start': span.start_char, 'end':span.end_char})
        doc._.ordinals_pattern = spans
        return doc


class CardinalsPattern:

    def __init__(self, vocab, nlp):
        # "NumForm=Digit|NumType=Card"
        pattern = [{'MORPH': "NumType=Card|Number=Plur"}]
        # Register a new token extension to flag bad HTML
        Doc.set_extension("cardinals_pattern", default=False)
        self.matcher = Matcher(vocab)
        self.matcher.add("cardinals", patterns=[pattern])

    def __call__(self, doc):
        # This method is invoked when the component is called on a Doc
        matches = self.matcher(doc)
        spans = []
        for match_id, start, end in matches:
            span = doc[start:end]
            spans.append({'id': span.start, 'start': span.start_char, 'end':span.end_char})
        doc._.cardinals_pattern = spans
        return doc


class DigitsPattern:

    def __init__(self, vocab, nlp):
        pattern = [{'MORPH': "NumForm=Digit|NumType=Card"}]
        # Register a new token extension to flag bad HTML
        Doc.set_extension("digits_pattern", default=False)
        self.matcher = Matcher(vocab)
        self.matcher.add("digits", patterns=[pattern])

    def __call__(self, doc):
        # This method is invoked when the component is called on a Doc
        matches = self.matcher(doc)
        spans = []
        for match_id, start, end in matches:
            span = doc[start:end]
            spans.append({'id': span.start, 'start': span.start_char, 'end': span.end_char})
        doc._.digits_pattern = spans
        return doc


class TrimestresPattern:

    def __init__(self, vocab, nlp):
        pattern = [{'MORPH': "Gender=Masc|NumType=Ord|Number=Sing"}, {"TEXT": "trimestre"}]
        # Register a new token extension to flag bad HTML
        Doc.set_extension("trimestres_pattern", default=False)
        self.matcher = Matcher(vocab)
        self.matcher.add("trimestre", patterns=[pattern])

    def __call__(self, doc):
        # This method is invoked when the component is called on a Doc
        matches = self.matcher(doc)
        spans = []
        for match_id, start, end in matches:
            span = doc[start:end]
            spans.append({'id': span.start, 'start': span.start_char, 'end': span.end_char})
        doc._.trimestres_pattern = spans
        return doc


class SemestresPattern:

    def __init__(self, vocab, nlp):
        pattern = [{'MORPH': "Gender=Masc|NumType=Ord|Number=Sing"}, {"TEXT": "semestre"}]
        # Register a new token extension to flag bad HTML
        Doc.set_extension("semestres_pattern", default=False)
        self.matcher = Matcher(vocab)
        self.matcher.add("semestre", patterns=[pattern])

    def __call__(self, doc):
        # This method is invoked when the component is called on a Doc
        matches = self.matcher(doc)
        spans = []
        for match_id, start, end in matches:
            span = doc[start:end]
            spans.append({'id': span.start, 'start': span.start_char, 'end': span.end_char})
        doc._.semestres_pattern = spans
        return doc


