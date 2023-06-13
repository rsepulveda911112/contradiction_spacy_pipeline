import os
import spacy
import pandas as pd
import json

from spacy.tokens.doc import Doc

from update_headlines import update_ent, update_date, update_ant

dir_files = os.getcwd()+'/data/anotados/'
dir_files_mo = os.getcwd()+'/data/modificados/'


count_num = 1700
count_ant = 1800
count_str = 2500

for file in os.listdir(dir_files):
    df = pd.read_json(dir_files+file)
    with open(dir_files_mo + os.path.splitext(os.path.basename(file))[0] +'_modificado' +'.json', "w+") as f:
        docs = []
        df_text_up = pd.DataFrame(['']*len(df), columns=['text_up'])
        df_update = pd.DataFrame([False]*len(df), columns=['update'])
        df = pd.concat([df, df_text_up, df_update], axis=1)
        print(file)

        for index, row in df.iterrows():

            doc = row['doc']
            df_ents = pd.DataFrame(doc['ents'])
            new_text = ''


            if row['label_contradiction'] == 'none':
                if not df_ents.empty:
                    if count_str > 0:
                        new_text = update_ent(doc, df_ents)
                        type_contradiction = 'str'
                        if new_text:
                            count_str -=1
                if not new_text:
                    if count_num > 0:
                        new_text = update_date(doc)
                        type_contradiction = 'num'
                        if new_text:
                            count_num -=1
                if not new_text:
                    if count_ant > 0:
                        new_text = update_ant(doc)
                        type_contradiction = 'ant'
                        if new_text:
                            count_ant -=1

                if new_text:
                    if new_text != doc['text']:
                        df.at[index, 'text_up'] = new_text
                        df.at[index, 'label_contradiction'] = type_contradiction
                        df.at[index, 'update'] = True
        df = df.drop(columns=['doc'])
        values = df.to_dict('records')
        f.write(json.dumps(values, indent=4))





