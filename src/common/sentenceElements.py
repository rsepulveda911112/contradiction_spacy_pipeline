from typing import Set
from src.common.VerbRelation import VerbRelation
from textacy.spacier.utils import _get_conjuncts

SUBJ_DEPS: Set[str] = {"agent", "csubj", "csubj:pass", "expl", "nsubj", "nsubj:pass", "compound"}
OBJ_DEPS: Set[str] = {"attr", "dobj", "dative", "oprd", "pobj","obj","iobj"}
AUX_DEPS: Set[str] = {"aux", "aux:pass"}
NEG_DEPS: Set[str] = {"neg",'advmod'}
CONJ_DEPS: Set[str] = {"appos", "cc", "conj"}


def get_root(doc):
    root_token = ''
    dep_root = ['root', 'ROOT']
    for token in doc:
        if token.dep_ in dep_root:
            root_token = token
            break
    return root_token


def find_children(token):
    childrens = []
    for child in token.children:
        if not child.is_punct:
            childrens.append(child)
            childrens.extend(find_children(child))
    return childrens


def get_frase(child, noun_chunks):
    frase = None
    found = False
    i = 0
    while i < len(noun_chunks) and not found:
        noun = noun_chunks[i]
        j = 0
        while j < len(noun) and not found:
            token = noun[j]
            if child.idx == token.idx:
                frase = noun
                found = True
            j = j + 1
        i = i + 1
    return frase


def get_conjuncts(token, noun_chunks,):
    conjuncts = []
    # CONST = {}
    # CONST.update(CONJ_DEPS)
    # CONST.update(OBJ_DEPS)
    for child in token.rights:
        if child.dep_ in CONJ_DEPS or child.dep_ in OBJ_DEPS:
            value_aux = get_frase(child, noun_chunks)
            if value_aux:
                conjuncts.append(value_aux)
                conjuncts.extend(get_conjuncts(child, noun_chunks))
    return conjuncts


def get_object(token, noun_chunks):
    all_object = []
    object_value = None
    if token:
        for child in token.rights:
            if child.pos_ == 'VERB':
                continue
            if child.dep_ in OBJ_DEPS:
                frase = get_frase(child, noun_chunks)
                if frase:
                    all_object.append(frase)
                else:
                    all_object.append(child.doc[child.i:child.i + 1])
                for new_child in child.rights:
                    object_value = get_frase(new_child, noun_chunks)
                    if object_value:
                        all_object.append(object_value)
                    else:
                        all_object.append(new_child.doc[new_child.i:new_child.i + 1])
                    all_object.extend(get_conjuncts(new_child, noun_chunks))
                    break
                break
            else:
                for new_child in child.rights:
                    if new_child.dep_ in OBJ_DEPS:
                        if new_child.pos_ == 'VERB':
                            continue
                        all_object.append(child.doc[child.i:child.i + 1])
                        object_value = get_frase(new_child, noun_chunks)
                        if object_value:
                            all_object.append(object_value)
                        else:
                            all_object.append(new_child.doc[new_child.i:new_child.i + 1])
                        all_object.extend(get_conjuncts(new_child, noun_chunks))

        if all_object:
            if len(all_object) > 1:
                all_object = sort_token(all_object)
                last_value = all_object[len(all_object) - 1]
                object_value = token.doc[all_object[0][0].i:last_value[len(last_value) - 1].i + 1].text
            else:
                object_value = all_object[0].text
    return object_value, all_object


def get_subject(token, noun_chunks):
    all_subject = []
    subject_value = None
    if token:
        for child in token.lefts:
            if child.dep_ in SUBJ_DEPS:
                frase = get_frase(child, noun_chunks)
                if frase:
                    all_subject.append(frase)
                else:
                    all_subject.append(child.doc[child.i:child.i + 1])
                for new_child in child.children:
                    subject_value = get_frase(new_child, noun_chunks)
                    if subject_value:
                        all_subject.append(subject_value)
                    else:
                        all_subject.append(new_child.doc[new_child.i:new_child.i + 1])
                    all_subject.extend(get_conjuncts(new_child, noun_chunks))
                    break
                break
        if all_subject:
            if len(all_subject) > 1:
                all_subject = sort_token(all_subject)
                last_value = all_subject[len(all_subject) - 1]
                subject_value = token.doc[all_subject[0][0].i:last_value[len(last_value) - 1].i + 1].text
            else:
                subject_value = all_subject[0].text
    return subject_value, all_subject


def get_agent(token, noun_chunks):
    all_agent = []
    agent_value = None
    if token:
        for child in token.rights:
            if child.dep_ in SUBJ_DEPS:
                frase = get_frase(child, noun_chunks)
                if frase:
                    all_agent.append(frase)
                else:
                    all_agent.append(child.doc[child.i:child.i + 1])
                for new_child in child.children:
                    agent = get_frase(new_child, noun_chunks)
                    if agent:
                        all_agent.append(agent)
                    else:
                        all_agent.append(new_child.doc[new_child.i:new_child.i + 1])
                    all_agent.extend(get_conjuncts(new_child, noun_chunks))
                    break
                break
        if all_agent:
            if len(all_agent) > 1:
                all_agent = sort_token(all_agent)
                last_value = all_agent[len(all_agent) - 1]
                agent_value = token.doc[all_agent[0][0].i:last_value[len(last_value) - 1].i + 1].text
            else:
                agent_value = all_agent[0].text
    return agent_value, all_agent


def sort_token(tokens):
    subject_value = []
    subject_value_text = []
    lesser_value = None
    for token in tokens:
        if not lesser_value:
            lesser_value = token
        else:
            if lesser_value[0].i > token[0].i:
                lesser_value = token
    if len(tokens) == 1:
        subject_value.append(lesser_value)
    else:
        tokens.remove(lesser_value)
        subject_value.append(lesser_value)
        subject_value.extend(sort_token(tokens))
    return subject_value


def token_per_text(text, doc):
    token_value = ''
    for token in doc:
        if token.text == text:
            token_value = token
            break
    return token_value


def get_dependence(dep_to_ext, token):
    return [child.text for child in token.children if child.dep_ in dep_to_ext]


def get_verb_dependece_root(token):
    childs = []
    if token:
        for child in token.children:
            if child.pos_ == 'VERB' and child.dep_ not in AUX_DEPS:
                # aux = get_dependence(AUX_DEPS, child)
                # neg = get_dependence(NEG_DEPS, child)
                # Verb(child, neg, aux)
                childs.append(child.text)
    return childs


def fix_element_with_punct(span):
    new_span = []
    value = None
    for token in span:
        if not token.is_punct:
            new_span.append(token)
    if new_span:
        value = span.doc[new_span[0].i:new_span[len(new_span) - 1].i + 1]
    return value


def verb_dependence(token):
    dep = []
    for child in token.children:
        if child.pos_ == 'VERB':
            dep.append(child)
    return dep
    # return [child for child in token.children if child.dep_ in dep_to_ext]


def get_verb_relation(token, noun_chunks):
    subject_value, subject_value_array = get_subject(token, noun_chunks)
    object_value, object_value_array = get_object(token, noun_chunks)
    # object_value = get_objects_of_verb(token, noun_chunks)
    agent_value, agent_value_array = get_agent(token, noun_chunks)
    aux = get_dependence(AUX_DEPS, token)
    neg = get_dependence(NEG_DEPS, token)
    verbs = get_verb_dependece_root(token)
    return VerbRelation(text=token, subject_value=subject_value, subject_value_array=subject_value_array,
                        object_value=object_value, object_value_array=object_value_array, agent_value=agent_value,
                        agent_value_array=agent_value_array,neg=neg, aux=aux, verbs=verbs)

# def get_main_verbs_of_sent(sent):
#     """Return the main (non-auxiliary) verbs in a sentence."""
#     return [
#         tok.text for tok in sent if tok.pos == VERB and tok.dep_ not in AUX_DEPS
#     ]


def get_nouns_of_sent(sent, cluster_noun_chunks):
    list_noun = {}
    for main_noun in cluster_noun_chunks:
        for noun in cluster_noun_chunks[main_noun][1:len(cluster_noun_chunks)]:
            if noun.sent == sent:
                list_noun[noun] = cluster_noun_chunks[main_noun][0]
    return list_noun


def get_objects_of_verb(verb, noun_chunks):
    """
    Return all objects of a verb according to the dependency parse,
    including open clausal complements.
    """
    object_value = None
    aux_value = None

    objs = [tok for tok in verb.rights if tok.dep_ in OBJ_DEPS]
    # get open clausal complements (xcomp)
    objs.extend(tok for tok in verb.rights if tok.dep_ == "xcomp")
    # get additional conjunct objects
    objs.extend(tok for obj in objs for tok in _get_conjuncts(obj))
    if objs:
        aux_value = sort_token(objs)
    if aux_value:
        object_value = get_frase(aux_value, noun_chunks)

        # object_value = verb.doc[aux_value[0].i:aux_value.pop().i + 1]
    return object_value


def is_element(element, list):
    found = False
    for elem in list:
        if element == elem:
            found = True
            break
    return found