from Applicant_Tracking_System.scripts.syntax_parser2 import *
from Applicant_Tracking_System.scripts.ml_classifier import *
from Applicant_Tracking_System.scripts.parsing_rules import *


### takes as input the output of Parser defind in syntax_parser
### function to find the label of the element
def Annalyser(dict):
    for element in dict:
        print('-->',element)
        for liste in dict[element]:

            ## we label each line of the resume
            ## we ll start by finds entites by a rule bases approche
            for element_list in liste:
                if len(extract_email(element_list[1])) != 0:
                    element_list[0] = 'email'
                    print(element_list)

                elif len(extract_phone_number(element_list[1])) != 0:
                    element_list[0] = 'phone number'
                    print(element_list)

                elif len(extract_url(element_list[1])) != 0:
                    element_list[0] = 'url'
                    print(element_list)

                else:
                    # if extract_duration(element_list[1]) != 0 :
                    element_list[0] = classifierFr([element_list[1]])[0]
                    print(element_list)
        print('\n\n')

def SkillsExtractor(dict):
    dict_skills = {}
    for element in dict:
        for liste in dict[element]:
            changing_range = len(liste)
            for indice_elem in range(changing_range):
                if indice_elem < len(liste) and len(liste[indice_elem][1])>0:
                    liste_skills = extract_skills(liste[indice_elem][1])
                    for ones in liste_skills :
                        if ones not in dict_skills.keys():
                            dict_skills[ones] = {'pro':0,'other':0}
                        if element == 'pro':
                            dict_skills[ones][element] +=1
                        else:
                            dict_skills[ones]['other'] +=1
    return(dict_skills)


