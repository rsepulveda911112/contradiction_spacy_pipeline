import nltk
import os


class Wordnet:

    def __init__(self):
        self.wordnet = nltk.corpus.reader.wordnet.WordNetCorpusReader(os.getcwd()+'/resource/es', None)

    def get_synonymous(self, word):
        synonymous = []
        for ss1 in self.wordnet.synsets(word):
            synonymous.extend(ss1.lemma_names())
        return synonymous

    def get_antonyms(self, word):
        antonyms = []
        for syn in self.wordnet.synsets(word):
            for lm in syn.lemmas():
                if lm.antonyms():
                    # antonyms.append(lm.antonyms()[0].name())
                    for an in lm.antonyms():
                        # ant = self.get_synonymous(an._name)
                        antonyms.extend([an._name])
        return list(set(antonyms))

    def get_hypernyms(self, word):
        hypernyms = []
        for syn in self.wordnet.synsets(word):
            # hypernyms.extend(syn.hypernyms())
            for lm in syn.hypernyms():
                hypernyms.extend([lm._name])
        return list(set(hypernyms))

    def get_hyponyms(self, word):
        hyponyms = []
        for syn in self.wordnet.synsets(word):
            for lm in syn.hyponyms():
                hyponyms.extend([lm._name])
        return list(set(hyponyms))

# wordnet = Wordnet()
# print(wordnet.get_synonymous("abandonar"))
# print(wordnet.get_antonyms("abandonar"))
# print(wordnet.get_hypernyms("gato"))
# print(wordnet.get_hypernyms("gato"))

# first = wordnet.wordnet.synset('carro')
# second = wordnet.wordnet.synset('automovil')
# print(first.path_similarity(second) )
# print(wordnet.synset("comprar.n.01").definition)
