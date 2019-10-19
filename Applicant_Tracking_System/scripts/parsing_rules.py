#################################################################################x##################################
# regles et heuristiques qu'on a définit
####################################################################################################################


import re
import nltk
from nltk.corpus import stopwords
import spacy
import csv
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from datetime import datetime
from dateutil import relativedelta

stop = stopwords.words('english')


##############################################################################################
##############################################################################################

################## extraxting email : regex  ###################
# xxx@yyy.zzz
# accurate
def extract_email(string):
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    return r.findall(string)


##############################################################################################
##############################################################################################

################## extraxting linked in or perso blog : regex  ###################
# http ou https need the other one
# accurate
def extract_url(string):
    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)
    return url


##############################################################################################
##############################################################################################

################## extraxting morrocan phone number  ###################
def extract_phone_number(string):
    r_phone = re.compile('[212|0]\d{1,2}.\d{2,3}.\d{2,3}.\d{0,2}.\d{0,2}')
    return r_phone.findall(string)


##############################################################################################
##############################################################################################

############# Extracting name : part of speech tagging with nltk (natural language processing library)   ##############
# critic : it considers something like Almonds Green as a name too --> to be changed with a names model
# input string of the cv
# output a list of names it contains

def ie_preprocess(document):
    document = ' '.join([i for i in document.split() if i not in stop])
    sentences = nltk.sent_tokenize(document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    return sentences


def extract_name(document):
    names = []
    sentences = ie_preprocess(document)
    for tagged_sentence in sentences:
        for chunk in nltk.ne_chunk(tagged_sentence):
            # if chunk[1] == 'NNP' :
            #    print(chunk)
            # print(chunk[1])
            if type(chunk) == nltk.tree.Tree:
                if chunk.label() == 'PERSON':
                    names.append(' '.join([c[0] for c in chunk]))
    return names


##############################################################################################
##############################################################################################

############ skills extraction nlp model + matching to the list of skills ###################
# input string of the cv
# output a list of skills it contains

def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
    csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
    for row in csv_reader:
        yield [cell.encode('utf-8') for cell in row]
    return csv_reader


def skills_list(filename):
    new_list = []
    reader = unicode_csv_reader(open(filename))
    for field1 in reader:
        new_list.append(field1[0].decode("utf-8").lower())
    return new_list


nlp = spacy.load('fr_core_news_sm')
# noun_chunks = nlp.noun_chunks
vectorizer_bi = CountVectorizer(analyzer='word', ngram_range=(2, 2))


vectorizer_tri = CountVectorizer(analyzer='word',ngram_range=(3, 3))


def extract_skills(resume_text):

    nlp_text = nlp(resume_text)
    corps = resume_text.split('\n')

    if (len(corps) >= 2):
        vectorizer_bi.fit_transform(corps)
    if (len(corps) >= 3):
        vectorizer_tri.fit_transform(corps)

    # removing stop words and implementing word tokenization
    tokens = [token.text for token in nlp_text if not token.is_stop]

    # reading the skills dataset
    path = "C:/Users/hala/Documents/Ma formation/Stage 2A/skills.csv"
    data = pd.read_csv(path)
    # extract values
    skills = data.columns.values.tolist()

    # readning fammille de competences of smart system
    path2 = "C:/Users/hala/Documents/Ma formation/Stage 2A/familles_competences.csv"
    skills2 = skills_list(path)

    skillset = []

    # check for one-grams (example: python)
    for token in tokens:
        if token.lower() in skills:
            skillset.append(token)
        if token.lower() in skills2:
            skillset.append(token)

    # check for bi-grams and tri-grams
    if (len(corps) >= 2):
        noun_chunks_bi = vectorizer_bi.get_feature_names()
        for token in noun_chunks_bi:
            token = token.lower().strip()
            if token in skills:
                skillset.append(token)
            if token in skills2:
                skillset.append(token)

    if (len(corps) >= 3):
        noun_chunks_tri = vectorizer_tri.get_feature_names()
        for token in noun_chunks_tri:
            token = token.lower().strip()
            if token in skills:
                skillset.append(token)
            if token in skills2:
                skillset.append(token)

    return [i.capitalize() for i in set([i.lower() for i in skillset])]


##############################################################################################
##############################################################################################

# extraire les durées de temps dans une phrase

MONTHS_SHORT = r'(jan)|(feb)|(mar)|(apr)|(may)|(jun)|(jul)|(aug)|(sep)|(oct)|(nov)|(dec)'
MONTHS_LONG = r'(january)|(february)|(march)|(april)|(may)|(june)|(july)|(august)|(september)|(october)|(november)|(december)'
MONTH = r'(' + MONTHS_SHORT + r'|' + MONTHS_LONG + r')'
YEAR = r'(((20|19)(\d{2})))'


def get_number_of_months_from_dates(date1, date2):
    if date2.lower() == 'present':
        date2 = datetime.now().strftime('%b %Y')
    try:
        if len(date1.split()[0]) > 3:
            date1 = date1.split()
            date1 = date1[0][:3] + ' ' + date1[1]
        if len(date2.split()[0]) > 3:
            date2 = date2.split()
            date2 = date2[0][:3] + ' ' + date2[1]
    except IndexError:
        return 0
    try:
        date1 = datetime.strptime(str(date1), '%b %Y')
        date2 = datetime.strptime(str(date2), '%b %Y')
        months_of_experience = relativedelta.relativedelta(date2, date1)
        months_of_experience = months_of_experience.years * 12 + months_of_experience.months
    except ValueError:
        return 0
    return months_of_experience


def extract_duration(line):
    exp_ = []
    experience = re.search("(?P<fmonth>\w+.\d+)\s*(\D|to|à|jusqu'à|jusque|jusqu'a||)\s*(?P<smonth>\w+.\d+|present)",
                           line, re.I)
    print(type(experience))
    if experience:
        exp_.append(experience.groups())
    print(exp_)
    for i in exp_:
        print(i)
        return (get_number_of_months_from_dates(i[0], i[2]))


########################################################################################################
########################################################################################################

############ function to remove nonsense sentences ############

NOT_ALPHA_NUMERIC = r'[^a-zA-Z\d]'
SPECIAL_CHAR = r'[@\+.-_]'


# returns true for nonsens element
def find_nonsence(txt):
    initial = len(txt)

    pageCount = re.compile(PAGE_COUNT)
    not_alpha_num = re.compile(NOT_ALPHA_NUMERIC)

    list = not_alpha_num.findall(txt)
    lenList = 0
    if (len(list) > 0):
        for element in list:
            lenList += len(element)
        if (lenList == initial):
            return True
        else:
            return False
    if (len(pageCount.findall(txt)) > 0):
        return True
    else:
        return False

########################################################################################################
########################################################################################################

