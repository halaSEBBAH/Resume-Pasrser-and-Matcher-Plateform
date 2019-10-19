import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
# french lemmatizer  ### reference : https://github.com/ClaudeCoulombe/FrenchLefffLemmatizer
from french_lefff_lemmatizer.french_lefff_lemmatizer import FrenchLefffLemmatizer
import unidecode
import tokenizer

from Applicant_Tracking_System.scripts.ml_classifier import classifierFr
from Applicant_Tracking_System.scripts.parsing_rules import extract_email, extract_phone_number, extract_url, extract_name

stop_words = set(stopwords.words('french'))

mots_education = ['académique', 'education', 'publications', 'formation', 'formations', 'etude', 'cursus',
                  'scolaire''etudes', 'certification''certifications', 'pfe', "projet de fin d'étude", 'stage',
                  'connaissance', 'competences']
mots_professionnel = ['accomplissement', 'experience', 'professionnel', 'travail', 'projet', 'mission', 'client']
NOT_ALPHA_NUMERIC = r'[^a-zA-Z\d]'

# regex for detecting titles
r_pro = re.compile(r'professionnel|experience|travail|experiences|mission|professionnelles')
r_etude = re.compile(r'formation|etude|education|cursus|scolaire|etudes|stage|connaissance|competences|éducation|étude')
r_langue = re.compile(r'langue')


# def remove_non_alphanum():


def remove_stop_words_and_lemmatize(txt):
    lemmatizer = FrenchLefffLemmatizer()
    # word_tokens = word_tokenize(txt)
    word_tokens = list(element.txt for element in tokenizer.tokenize(txt))
    word_tokens = [x for x in word_tokens if x != None]
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    filtered_sentence = []
    for w in word_tokens:
        w = lemmatizer.lemmatize(w)
        if w not in stop_words:
            filtered_sentence.append(w)
    return (' '.join(filtered_sentence))


def findBreakers(element):
    element = element.lower()
    element = unidecode.unidecode(element)
    # return keyword etude
    if len(r_etude.findall(element)) > 0 and len(element.split(' ')) < 3:
        # print("element etude :   ",element,"   ",r_etude.findall(element))
        return 'etude'

    # return keyword professionnel
    if len(r_pro.findall(element)) > 0 and len(element.split(' ')) < 3:
        if (not (len(r_etude.findall(element)) > 0)):
            # print("element professionnel :   " , element ,"   ", r_pro.findall(element))
            return 'pro'

    if len(r_langue.findall(element)) > 0 and len(element.split(' ')) < 3:
        # print("element langue :   " , element ,"   ", r_langue.findall(element))
        return 'langue'

    # return back to line
    if (element == ''):
        # print("element retour :   ")
        return 'retour'
    else:
        return


def transform(dict):
    for element in dict:
        for liste in dict[element]:
            for indice in range(len(liste)):
                label = ''
                if len(extract_email(liste[indice])) != 0:
                    label = 'email'
                elif len(extract_phone_number(liste[indice])) != 0:
                    label = 'phone number'
                elif len(extract_url(liste[indice])) != 0:
                    label = 'url'
                elif len(extract_name(liste[indice])) != 0:
                    label = 'name'
                else:
                    label = classifierFr([liste[indice]])[0]
                str = [label, liste[indice]]
                liste[indice] = str
    return (dict)


def ParserFileNew(txt):
    # preprocess tex
    list = txt.split('\n')
    ind = 0
    for ind in range(len(list)):
        list[ind] = remove_stop_words_and_lemmatize(list[ind])

    # define titles and blocks
    Blocs = []
    dictBlock = []
    i = 0
    breakerToKeep = 'start'
    while i < len(list):
        flag = 0
        temporaryBloc = []
        while (i < len(list) and findBreakers(list[i]) == None):  # means element is not a breaker
            flag = 1
            temporaryBloc.append(list[i])
            i += 1
        Blocs.append(temporaryBloc)

        if not len(temporaryBloc) == 0:
            dictBlock.append(['Bloc', temporaryBloc])

        if i < len(list):
            breakerToKeep = findBreakers(list[i])
        if not (breakerToKeep == None) and not (breakerToKeep == 'retour'):
            dictBlock.append(['Titre', [breakerToKeep]])
        i += 1
    finalList = []
    # regroup blocks to corresponding title
    ActualTitle = 'start'
    indice = 0
    for indice in range(len(dictBlock)):
        if dictBlock[indice][0] == 'Titre':
            ActualTitle = dictBlock[indice][1][0]
        else:
            finalList.append([ActualTitle, dictBlock[indice][1]])
    Finaldic = {}
    for element in finalList:
        Finaldic.setdefault(element[0], []).append(element[1])
    Finaldic = transform(Finaldic)
    return (Finaldic)

