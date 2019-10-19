####################################################################################################################
# réalisation d'un linear regression classifier
####################################################################################################################

import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm import LinearSVC
import numpy as np
from nltk.corpus import stopwords

# stopFR is a list fresh stop words
stopFR = stopwords.words('french')


## preparer les listes de données pour classifiers anglais et francais

####################################################################################################################
# ####################################       PROCESSING DATA     ####################################################
####################################################################################################################

def preprocessEng():
    path = "C:/Users/hala/Documents/Ma formation/Stage 2A/Spacy/traindata.json"
    dataList = []
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            data = json.loads(line)
            for element in data:
                for element2 in data['annotation']:
                    # print(element2['label'][0])
                    for element3 in element2['points']:
                        # print(element3['text'])
                        if len(element2['label']) > 0:
                            # print(element2['label'][0])
                            # if(element2['label'][0] != 'Name' ):
                            if element2['label'][0] == 'Graduation Year':
                                dataList.append(['Graduation', element3['text']])
                            else:
                                dataList.append([element2['label'][0], element3['text']])

    return (dataList)


def preprocessFR():
    dataList = []

    path = "C:/Users/hala/Documents/Ma formation/Stage 2A/ML ATM classification/DataSet/collegeFR.txt"
    with open(path, "r", encoding='utf-8') as f:
        lignes = f.readlines()
        for element in lignes:
            dataList.append(['college', element])

    path = "C:/Users/hala/Documents/Ma formation/Stage 2A/ML ATM classification/DataSet/companiesFR.txt"
    with open(path, "r", encoding='utf-8') as f:
        lignes = f.readlines()
        for element in lignes:
            dataList.append(['companies', element])

    path = "C:/Users/hala/Documents/Ma formation/Stage 2A/ML ATM classification/DataSet/degreeFR.txt"
    with open(path, "r", encoding='utf-8') as f:
        lignes = f.readlines()
        for element in lignes:
            dataList.append(['degree', element])

    path = "C:/Users/hala/Documents/Ma formation/Stage 2A/ML ATM classification/DataSet/designationFR.txt"
    with open(path, "r", encoding='utf-8') as f:
        lignes = f.readlines()
        for element in lignes:
            dataList.append(['designation', element])

    path = "C:/Users/hala/Documents/Ma formation/Stage 2A/ML ATM classification/DataSet/locationFR.txt"
    with open(path, "r", encoding='utf-8') as f:
        lignes = f.readlines()
        locations = []
        for element in lignes:
            locations.append(element)
        locations = np.random.choice(locations, 300, replace=False)
        for element in locations:
            dataList.append(['location', element])

    path = "C:/Users/hala/Documents/Ma formation/Stage 2A/ML ATM classification/DataSet/name.txt"
    with open(path, "r", encoding='utf-8') as f:
        lignes = f.readlines()
        names = []
        for element in lignes:
            names.append(element)
        names = np.random.choice(names, 300, replace=False)
        for element in names:
            dataList.append(['name', element])

    path = "C:/Users/hala/Documents/Ma formation/Stage 2A/ML ATM classification/DataSet/skills.txt"
    with open(path, "r", encoding='utf-8') as f:
        lignes = f.readlines()
        for element in lignes:
            dataList.append(['skills', element])

    return (dataList)


####################################################################################################################
#####################################       TRAIN MODEL :LINEAR REGRETION        ###################################
####################################################################################################################

# on transforme la dataset à une pandas dataframe
def classifierEng(txt):
    dataList = preprocessEng()
    df = pd.DataFrame(dataList, columns=['Category', 'Text'])
    df = df[pd.notnull(df['Text'])]
    df = df.drop_duplicates()
    df['category_id'] = df['Category'].factorize()[0]
    cat_id_df = df[["Category", "category_id"]].drop_duplicates().sort_values('category_id')
    cat_to_id = dict(cat_id_df.values)
    id_to_cat = dict(cat_id_df[['category_id', 'Category']].values)
    # dataList.append([element2['label'][0],element3['text']])

    tfidf = TfidfVectorizer(sublinear_tf=True,  # use a logarithmic form for frequency
                            min_df=5,  # minimum numbers of documents a word must be present in to be kept
                            norm='l2',  # ensure all our feature vectors have a euclidian norm of 1
                            ngram_range=(1, 2),  # to indicate that we want to consider both unigrams and bigrams.
                            stop_words='english')  # to remove all common pronouns to reduce the number of noisy features

    features = tfidf.fit_transform(df.Text).toarray()
    labels = df.category_id
    X_train, X_test, y_train, y_test = train_test_split(df['Text'], df['Category'], random_state=0)

    count_vect = CountVectorizer()

    X_train_counts = count_vect.fit_transform(X_train)
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
    clf = LinearSVC().fit(X_train_tfidf, y_train)
    return (clf.predict(count_vect.transform(txt)))


def classifierFr(txt):
    dataList = preprocessFR()
    df = pd.DataFrame(dataList, columns=['Category', 'Text'])
    df = df[pd.notnull(df['Text'])]
    df = df.drop_duplicates()
    df['category_id'] = df['Category'].factorize()[0]
    cat_id_df = df[["Category", "category_id"]].drop_duplicates().sort_values('category_id')
    cat_to_id = dict(cat_id_df.values)
    id_to_cat = dict(cat_id_df[['category_id', 'Category']].values)
    # dataList.append([element2['label'][0],element3['text']])

    tfidf = TfidfVectorizer(sublinear_tf=True,  # use a logarithmic form for frequency
                            min_df=5,  # minimum numbers of documents a word must be present in to be kept
                            norm='l2',  # ensure all our feature vectors have a euclidian norm of 1
                            ngram_range=(1, 2),  # to indicate that we want to consider both bigrams and unigramms.
                            stop_words=stopFR,
                            )  # to remove all common pronouns to reduce the number of noisy features

    features = tfidf.fit_transform(df.Text).toarray()
    labels = df.category_id
    X_train, X_test, y_train, y_test = train_test_split(df['Text'], df['Category'], random_state=0)

    count_vect = CountVectorizer()

    X_train_counts = count_vect.fit_transform(X_train)
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
    clf = LinearSVC().fit(X_train_tfidf, y_train)
    return clf.predict(count_vect.transform(txt))
