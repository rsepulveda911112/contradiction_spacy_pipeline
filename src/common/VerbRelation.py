class VerbRelation:

    def __init__(self, text, subject_value,subject_value_array, object_value, object_value_array,
                 agent_value, agent_value_array, neg, aux, verbs):
        self.text = text
        self.main_subject = subject_value
        self.subject_value_array = subject_value_array
        self.object = object_value
        self.object_value_array = object_value_array
        self.agent = agent_value
        self.agent_value_array = agent_value_array
        self.neg = neg
        self.aux = aux
        self.verbs = verbs


class Verb:

    def __init__(self, verb, neg, aux):

        self.verb = verb
        self.neg = neg
        self.aux = aux