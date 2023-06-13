from spacy.tokens import Doc
from src.common.sentenceElements import get_root, fix_element_with_punct, get_verb_relation, \
                                    get_nouns_of_sent, is_element
from textacy.spacier.utils import get_main_verbs_of_sent
from spacy.language import Language


class ParserComponent:

    '''
    A SpaCy pipeline component for Parser
    '''

    def __init__(self, nlp):
        self.nlp = nlp
        Doc.set_extension('parser_doc', default=False)
        Doc.set_extension('main_nouns', default=False)

    def __call__(self, doc):
        parser_doc = {}
        list_parser_sent = []
        ent_verb_subject = {}
        ent_verb_object = {}
        ent_verb_agent = {}
        clusters_dict = {}
        doc_nouns = {}
        all_verbs = []

        # if doc._.has_coref:
        #     for cluster in doc._.coref_clusters:
        #         # if (cluster.main.root.ent_type_ in type_ent) or (cluster.main.root.lemma_ == '-PRON-'):
        #         new_main = fix_element_with_punct(cluster.main)
        #         if new_main:
        #             mentions = []
        #             for mention in cluster.mentions:
        #                 new_mention = fix_element_with_punct(mention)
        #                 if new_mention:
        #                     mentions.append(new_mention)
        #             clusters_dict[new_main] = mentions

        index = 0
        for sent in doc.sents:
            cluster_coref = {}
            ents_sent = []
            noun_chunks_sent = []
            main_noun_chunks = {}
            noun_chunks = []
            for ent in sent.ents:
                ents_sent.append(ent.text)
            for noun_chunk in sent.noun_chunks:
                new_noun_chunk = fix_element_with_punct(noun_chunk)
                if new_noun_chunk:
                    noun_chunks.append(new_noun_chunk)
                    noun_chunks_sent.append(new_noun_chunk.text)
                    main_noun_chunks[new_noun_chunk] = new_noun_chunk
                # if noun_chunk.text not in doc_nouns:
                #     doc_nouns.append(noun_chunk.text)

            noun_chunks_of_sent = get_nouns_of_sent(sent, clusters_dict)
            main_noun_chunks.update(noun_chunks_of_sent)
            root = get_root(sent)
            main_verbs = get_main_verbs_of_sent(sent)
            verb_relations = []
            for verb in main_verbs:
                #los verbos de la oración en lista
                all_verbs.append(verb.text)
                verb_relation = get_verb_relation(verb, noun_chunks)
                verbs_dependeces = verb_relation.verbs
                verbs_dependeces.append(verb.text)
                # verbs_dependeces = set(verbs_dependeces)

                for noun in main_noun_chunks:
                    if verb_relation.main_subject and self.find_coincidence(noun, verb_relation.subject_value_array):
                        if main_noun_chunks[noun].text in ent_verb_subject.keys():
                            list_value = ent_verb_subject[main_noun_chunks[noun].text]
                            # list_value.update(verbs_dependeces)
                            list_value.extend(verbs_dependeces)
                            ent_verb_subject[main_noun_chunks[noun].text] = list_value
                        else:
                            ent_verb_subject[main_noun_chunks[noun].text] = verbs_dependeces
                    elif verb_relation.agent and self.find_coincidence(noun, verb_relation.agent_value_array):
                        if main_noun_chunks[noun].text in ent_verb_agent.keys():
                            list_value = ent_verb_agent[main_noun_chunks[noun].text]
                            # list_value.update(verbs_dependeces)
                            list_value.extend(verbs_dependeces)
                            ent_verb_agent[main_noun_chunks[noun].text] = list_value
                        else:
                            ent_verb_agent[main_noun_chunks[noun].text] = verbs_dependeces
                    elif verb_relation.object and self.find_coincidence(noun, verb_relation.object_value_array):
                        if main_noun_chunks[noun].text in ent_verb_object.keys():
                            list_value = ent_verb_object[main_noun_chunks[noun].text]
                            # list_value.update(verbs_dependeces)
                            list_value.extend(verbs_dependeces)
                            ent_verb_object[main_noun_chunks[noun].text] = list_value
                        else:
                            ent_verb_object[main_noun_chunks[noun].text] = verbs_dependeces

                verb_relations.append({'verb': verb_relation.text.text, 'subject': verb_relation.main_subject,
                                       'object': verb_relation.object, 'agent': verb_relation.agent,
                                       'aux': verb_relation.aux, 'neg': verb_relation.neg,
                                       'verbs_relation': verb_relation.verbs})
            # doc_nouns.update()
            # , sent._.srl
            #
            new_noun_chunks_of_sent = self.convert_dict_noun(noun_chunks_of_sent)
            list_parser_sent.append({'root': root.text, 'verb_relations': verb_relations,
                                     'noun_chunks': noun_chunks_sent, 'ent': ents_sent,
                                     'cluster_coref':{'sent_index': index,'cluster': new_noun_chunks_of_sent}})

            # parser_doc = {'ent_verb_subject': ent_verb_subject, 'ent_verb_object': ent_verb_object,
            #               'ent_verb_agent': ent_verb_agent}
            index = index + 1
        parser_doc = {'sent_parse': list_parser_sent, 'ent_verb_subject': ent_verb_subject,
                      'ent_verb_object': ent_verb_object, 'ent_verb_agent': ent_verb_agent}
        doc._.parser_doc = parser_doc
        doc_nouns = [noun.text for noun in doc.noun_chunks]
        doc._.main_nouns = doc_nouns
        return doc

    def convert_dict_noun(self, noun_chunks_of_sent):
        value = {}
        for noun in noun_chunks_of_sent:
            if is_element(noun_chunks_of_sent[noun].text,value.keys()):
                list_value = value[noun_chunks_of_sent[noun].text]
                list_value.extend([noun.text])
                value[noun_chunks_of_sent[noun].text] = list_value
            else:
                value[noun_chunks_of_sent[noun].text] = [noun.text]
        return value


    def find_coincidence(self, span, list_span):
        found = False
        i = 0
        span_text = span.text
        if list_span:
            while i < len(list_span) and not found:
                if span_text == list_span[i].text:
                    found = True
                i = i+1
        return found