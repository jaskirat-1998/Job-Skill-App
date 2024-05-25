import pandas as pd
from scipy import sparse
import re
import numpy as np
from collections import Counter
import io


# getting the data
annot = pd.read_csv('data/final_annotated_data.csv')
all_data = pd.read_csv('data/all_data.csv')

# getting a set of all skills
skill_set = set()
for i in range(len(annot)):
    skill_list = [i.strip() for i in annot.iloc[i]['skills'].split(',') if i != '']
    skill_set.update(skill_list)

# creating dictionaries to map skills to ids and vice versa
skill_to_id = {}
for i, skill in enumerate(skill_set):
    skill_to_id[skill] = i
    
id_to_skill = {v:k for k,v in skill_to_id.items()}


# building the skill-job matrix representing which skills are present in each of the job data
skill_job_matrix = np.zeros((len(all_data), len(skill_set)))

for i in range(len(all_data)):
    words = re.sub(r'[^\w\s]', '', all_data.iloc[i]['job_description'].lower()).split()
    tokens = set(words)
    for j, skill in enumerate(skill_set):
        skill_job_matrix[i,j] = skill in tokens



def get_query_array(query):
    '''
    This function takes comma seperated skills as a string input and convert those into a numpy array
    of size equal to the length of skill set, representing which skills are present in the input
    '''
    query_array = np.zeros(len(skill_set))
    input_skills = [i.strip() for i in query.lower().split(',')]
    input_skill_ids = [skill_to_id[i] for i in input_skills if i in skill_to_id]
    query_array[input_skill_ids] = 1
    return query_array



def get_top_n_job_ids(query, n):
    '''
    Getting index of top "n" jobs that best match with our skills
    '''
    query_array = get_query_array(query)
    dot = -skill_job_matrix.dot(query_array)
    return [i for i in (dot).argsort()[:n] if dot[i]!=0]


def get_job_data(ids):
    '''
    based on the indices, returning job data from the csv file
    '''
    df = all_data.iloc[ids]
    #print(all_data.columns)
    df = df.where(pd.notnull(df), None)
    df.to_csv('download/data.csv', index=False )
    data = []
    print(df.columns)
    for i in range(len(df)):
        dict_record = {}
        for c in df.columns:
            dict_record[c] = df.iloc[i][c]
        data.append(dict_record)
    return data

def get_download_data():
    '''
    function to read the csv file and return it as a string
    '''
    f = open('download/data.csv')
    text = f.read()
    #text = ' \n '.join(text.split('\n'))
    return text




## Wordcloud related functions

def get_wordcloud_data(query):
    '''
    function to get data for thr wordcloud based on the skills entered
    '''
    query_array = get_query_array(query)
    dot_prod = -skill_job_matrix.dot(query_array)
    indices = (dot_prod).argsort()[:100].tolist()
    data = Counter()
    for i, val in zip(indices, -dot_prod[indices]):
        for j in range(int(val)):
            title = all_data.iloc[i]['title'].lower().split()
            bigrams = [title[i]+' '+title[i+1] for i in range(len(title)-1)]
            trigrams = [title[i]+' '+title[i+1]+' '+title[i+2] for i in range(len(title)-2)]
            #data_bi = [{'name':i, 'weight':val} for i in bigrams]
            #data_tri = [{'name':i, 'weight':val} for i in trigrams]
            #data.extend(data_bi)
            #data.extend(data_tri)
            data.update(bigrams)
            data.update(trigrams)
    data = [{'name':k, 'weight':v}for k,v in data.items()]
    return data


## Relevant skills for a job class
class_skills = {}
for class_ in annot['class_name'].unique():
    temp = annot[annot['class_name'] == class_]
    counter = Counter()
    for i in range(len(temp)):
        counter.update(temp.iloc[i]['skills'].lower().split(','))
    counter = {k:round(100*v/len(temp),2) for k,v in counter.items()}
    counter = dict(sorted(counter.items(), key = lambda x: -x[1] )[:10])
    class_skills[class_] = counter
class_skills

