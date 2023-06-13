import numpy as np
import pandas as pd
import os
import random
from src.common.wordreference import get_synonym_antonyns
from src.common.verb_tense import get_verb

ordinales = ['primero', 'segundo', 'tercero', 'cuarto', 'quinto', 'sexto', 'séptimo', 'octavo', 'noveno', 'décimo',
             'decimoprimero', 'undécimo','decimosegundo','duodécimo','decimotercero','decimocuarto','decimoquinto',
             'decimosexto' ,'decimoséptimo', 'decimoctavo', 'decimonoveno', 'vigésimo', 'vigésimo primero',
             'vigésimo segundo', 'vigésimo tercero', 'trigésimo', 'cuadragésimo', 'quincuagésimo', 'sexagésimo',
             'septuagésimo', 'octogésimo', 'nonagésimo', 'centésimo', 'centésimo primero', 'ducentésimo', 'tricentésimo',
             'cuadringentésimo', 'quingentésimo', 'sexcentésimo', 'septingentésimo', 'octingentésimo', 'noningentésimo',
             'milésimo','millonésimo',]

cardinales = ['uno', 'dos', 'tres', 'cuatro', 'cinco', 'seis', 'siete', 'ocho', 'nueve', 'diez', 'once',
              'doce', 'trece', 'catorce', 'quince', 'dieciséis', 'diecisiete', 'dieciocho', 'diecinueve',
              'veinte', 'veintiuno', 'veintidós', 'veintitrés', 'treinta', 'cuarenta', 'cincuenta', 'sesenta',
              'setenta', 'ochenta', 'noventa', 'cien', 'ciento uno', 'ciento veinticinco', 'doscientos',
              'trescientos', 'cuatrocientos', 'quinientos', 'seiscientos', 'setecientos', 'ochocientos',
              'novecientos', 'mil', 'millón', 'diez millones',]

months = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre',]
days = ['domingo', 'lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado',]
trimestres = ['primer', 'segundo', 'tercer', 'cuarto']
semestres = ['primer', 'segundo']


####################### Organization #######################################3
df_in_org_lower = pd.read_csv(os.getcwd() + '/data/value.csv', sep='\t')
for column in df_in_org_lower.columns:
    df_in_org_lower[column] = df_in_org_lower[column].dropna().apply(lambda x:x.lower())

df_in_org = pd.read_csv(os.getcwd() + '/data/value.csv', sep='\t')

####################### Contry #######################################
df_in_contry = pd.read_csv(os.getcwd() + '/data/country.csv', sep='\t')

####################### Provincia #######################################
df_in_province = pd.read_csv(os.getcwd() + '/data/ca_provincias.csv', sep='\t')

######################### Antonimos #####################################

def update_date(doc):
    text = doc['text']
    new_text = ''
    value_old = ''
    value_new = ''
    ############### Dates ####################
    times_values = doc['_']['time_pattern']
    if times_values:
        time = times_values[0]
        value_old = text[time['start']:time['end']]
        value_old_lower = value_old.lower()
        if value_old_lower in months:
            new_months = []
            new_months.extend(months)
            new_months.remove(value_old_lower)
            index = random.randint(0, len(months)-2)
            value_new = new_months[index]
        elif value_old_lower in days:
            new_days = []
            new_days.extend(days)
            new_days.remove(value_old_lower)
            index = random.randint(0, len(days)-2)
            value_new = new_days[index]
        elif len(value_old) == 4 and ('.' or ',') not in value_old:
            value_int = random.randint(1, 10)
            value_new = str(int(value_old) - value_int)

    ############### Trimestre ####################
    if not value_new:
        trimestres_values = doc['_']['trimestres_pattern']
        if trimestres_values:
            trimestre = trimestres_values[0]
            index = random.randint(0, len(trimestres)-2)
            value_old = text[trimestre['start']:trimestre['end']]
            value_old = value_old.replace(' trimestre', '')
            value_old_lower = value_old.lower()
            if value_old_lower in trimestres:
                new_trimestres = []
                new_trimestres.extend(trimestres)
                new_trimestres.remove(value_old_lower)
                value_new = new_trimestres[index]
    ############### Semestre ####################
    if not value_new:
        semestres_values = doc['_']['semestres_pattern']
        if semestres_values:
            semestre = semestres_values[0]
            value_old = text[semestre['start']:semestre['end']]
            value_old = value_old.replace(' semestre', '')
            value_old_lower = value_old.lower()
            if value_old_lower in semestres:
                new_semestres = []
                new_semestres.extend(semestres)
                new_semestres.remove(value_old_lower)
                value_new = new_semestres[0]
    ############### Ordinal ####################
    if not value_new:
        ordinals_values = doc['_']['ordinals_pattern']
        if ordinals_values:
            for ordinal in ordinals_values:
                index = random.randint(0, len(ordinales)-2)
                value_old = text[ordinal['start']:ordinal['end']]
                value_old_lower = value_old
                if value_old_lower in ordinales:
                    new_ordinales = []
                    new_ordinales.extend(ordinales)
                    new_ordinales.remove(value_old_lower)
                    value_new = new_ordinales[index]
                    break
    ############### Cardinal ####################
    if not value_new:
        cardinals_values = doc['_']['cardinals_pattern']
        if cardinals_values:
            if value_old in cardinales:
                for cardinal in cardinals_values:
                    index = random.randint(0, len(cardinales)-2)
                    value_old = text[cardinal['start']:cardinal['end']]
                    value_old_lower = value_old.lower()
                    if value_old_lower in cardinales:
                        new_cardinales = []
                        new_cardinales.extend(cardinales)
                        new_cardinales.remove(value_old_lower)
                        value_new = new_cardinales[index]
    ############### Digits ####################
    if not value_new:
        digits_values = doc['_']['digits_pattern']
        if digits_values:
            digits = digits_values[0]
            value_old = text[digits['start']:digits['end']]
            tokens = doc['tokens']
            digits_id = digits['id']
            actual_token = tokens[digits_id]
            if len(tokens) > digits_id+1:

                next_token = tokens[digits_id+1]
                if next_token["morph"] == "NumForm=Digit" and next_token["lemma"] == "%":
                    try:
                        value_old_cal = int(value_old)
                        max_range = 100 - value_old_cal
                        value = random.randint(1, round(max_range/2))
                    except:
                        value_old_cal = float(value_old.replace(',','.'))
                        # value_old_cal = float(value_old)
                        max_range = 100 - value_old_cal
                        value = round(random.uniform(0.2, min(2, max_range)), 2)
                    value_new = str(value_old_cal + value)
                else:
                    value_new = update_num(value_old, actual_token)
            else:
                value_new = update_num(value_old, actual_token)

    if value_new:
        if value_old[0].isupper():
            value_new = value_new[0].upper()+value_new[1:]
        new_text = text.replace(value_old, value_new)
    return new_text


def update_num(value_old, actual_token):
    value_new = ''
    if actual_token["morph"] == "NumForm=Digit|NumType=Card":
        value = ''
        try:
            value_old_cal = int(value_old)
            value = random.randint(1, 200)
        except:
            try:
                value_old_cal = float(value_old.replace(',','.'))
                value = random.uniform(0.2, 5)
            except:
                pass
        if value:
            value_new = str(round(value_old_cal + value, 2))
    return value_new


def update_ent(doc, df_ents):
    text = doc['text']
    new_text = ''
    # en = text[start:end]
    df_ents['name'] = df_ents.apply(lambda x: text[x['start']: x['end']], axis=1)
    count_ents = len(df_ents)
    if count_ents == 1:
        new_text, update_index = cambiar_ner(doc, df_ents, text)
    else:
        update_index = random.randint(0, 1)
        if update_index == 0:
            new_text, update_index = cambiar_ner(doc, df_ents, text)
        if update_index == 1:
            new_text = inter_cambiar_ner(doc, df_ents, text)
            if not new_text:
                new_text, _ = cambiar_ner(doc, df_ents, text)
    return new_text


def update_ant(doc):
    text = doc['text']
    tokens = doc['tokens']
    token_verb = ''
    for token in tokens:
        if token['dep'] == 'ROOT':
            if token['pos'] == 'VERB':
                token_verb = token
                break
                # morph = token['morph']
                # verb = token['lemma']

    new_text = ''
    if token_verb:
        ants = []
        syn, ants = get_synonym_antonyns(token_verb['lemma'])

        ant_value = ''
        if ants:
            ant_value = ants[0]

        morph = token_verb['morph']
        if ant_value and morph:
            morph = get_dic(morph)
            new_verb = ''
            try:
                new_verb = get_verb(ant_value, morph)
            except:
                pass
            if new_verb:
                new_text = text.replace(text[token['start']:token['end']], new_verb)
    return new_text


def get_dic(morph):
    morph_dict = {}
    morphs = morph.split('|')
    for mo in morphs:
        key,value = mo.split('=')
        morph_dict[key] = value
    return morph_dict

def add_ant(doc):
    text = doc['text']
    new_text = ''
    tokens = doc['tokens']
    sentences = doc['_']['parser_doc']['sent_parse']
    # for token in tokens:

    # if count_ents == 1:
    #     new_text, update_index = cambiar_ner(doc, df_ents, text)
    # else:
    #     update_index = random.randint(0, 1)
    #     if update_index == 0:
    #         new_text, update_index = cambiar_ner(doc, df_ents, text)
    #     if update_index == 1:
    #         new_text = inter_cambiar_ner(doc, df_ents, text)
    #         if not new_text:
    #             new_text, _ = cambiar_ner(doc, df_ents, text)
    return new_text


def get_main_noun(value, main_nouns):
    for noun in main_nouns:
        if value in noun:
            value = noun
            break
    return value


def inter_cambiar_ner(doc, df_ents, text):
    new_text = ''
    main_nouns = doc['_']['main_nouns']
    for group_id, group in df_ents.groupby("label"):
        if len(group) > 1:
            if (group.iloc[1]['start'] - group.iloc[0]['end']) > 3:
                first = get_main_noun(group.iloc[0]['name'], main_nouns)
                second = get_main_noun(group.iloc[1]['name'], main_nouns)
                new_text = text.replace(second, 'xxx')
                new_text = new_text.replace(first, second)
                new_text = new_text.replace('xxx', first)
                break
    return new_text


def split_ner(tokens, value, text):
    split_text = True
    for token in tokens:
        if value == text[token['start']:token['end']]:
            token_id = token['id']
            if token_id > 0:
                if tokens[token_id-1]["dep"] == "case":
                    split_text = False
                    break
    return split_text


def cambiar_ner(doc, df_ents, text):
    update_index = 0
    new_text = ''
    main_nouns = doc['_']['main_nouns']
    for index, row in df_ents.iterrows():
        name = row['name']
        value = get_org_value(name)
        if not value:
            value = get_value_iter(row['name'])
        if value:
            value_changed = df_ents.iloc[index]['name']
            if split_ner(doc['tokens'], df_ents.iloc[index]['name'], text):
                value_changed = get_main_noun(value_changed, main_nouns)
            new_text = text.replace(value_changed, value)
            break
        elif index == len(df_ents)-1:
            update_index = 1
    return new_text, update_index


def get_value_iter(value_in):
    result = ''
    # [df_in_province, 'name_mun', 'cod_pro']
    list_param = [[df_in_province, 'name_pro', 'name_ca'],
                  [df_in_contry, 'capital', 'continente'],
                  [df_in_contry, 'pais', 'continente'],
                  [df_in_province, 'name_ca', None]]
    for value in list_param:
        result = get_other_specific_value(value[0], value_in, value[1], value[2])
        if result:
            break
    return result


def get_other_specific_value(df_in, value_in, column_name, link_name):
    pais_desambiation = {'EEUU': ["Estados Unidos", 'EE.UU.', 'EE.UU', 'EEUU']}
    if column_name == 'pais':
        if value_in in list(pais_desambiation.values())[0]:
            value_in = list(pais_desambiation.keys())[0]
    value_out = ''
    value_in = value_in.lower()
    df_in['lower' + column_name] = df_in[column_name].apply(lambda x: x.lower())
    row_value = df_in[df_in['lower' + column_name].values == value_in]
    if not row_value.empty:
        if link_name:
            df_filter = df_in[df_in[link_name] == row_value.iloc[0][link_name]]
            if df_filter.empty:
                df_filter = df_in[df_in[column_name] != row_value.iloc[0][column_name]]
        else:
            df_filter = df_in[df_in[column_name] != row_value.iloc[0][column_name]]
        df_filter = df_filter[df_filter['lower' + column_name] != value_in]

        if len(df_filter) > 0:
            index = random.randint(0, len(df_filter)-1)
            value_out = df_filter.iloc[index][column_name]
    return value_out


def get_org_value(value_in):
    value_out = ''
    value_columns = df_in_org_lower.columns
    for column in value_columns:
        values_serie = df_in_org_lower[column]
        values_serie = values_serie.dropna()
        values = list(values_serie.values)
        if value_in.lower() in values:
            value_index = values.index(value_in.lower())
            values.remove(value_in.lower())
            if len(values) > 0:
                index = random.randint(0, len(values)-1)
                column_value = df_in_org[column].dropna()
                column_value = list(column_value.values)
                value_to_remove = column_value[value_index]
                column_value.remove(value_to_remove)
                value_out = column_value[index]
                if not isinstance(value_out,str):
                    if np.isnan(value_out):
                        print('nannnnnnnnnnnnnnnn')
                # if value_out == np.nan:
                #     print('nannnnnnnnnnnnnnnn')
            break
    return value_out

# 'name_pro', 'name_ca'
# 'capital', 'continente'
# 'pais', 'continente'
# 'name_mun', 'cod_pro'


# get_other_specific_value(df_in_contry, 'Andalucía', 'name_ca', None)
# get_other_value('FIAT')


