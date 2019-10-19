from Applicant_Tracking_System.scripts import semantic_annalyser
from Applicant_Tracking_System.scripts.syntax_parser2 import *
from Applicant_Tracking_System.scripts.ml_classifier import *
from Applicant_Tracking_System.scripts.parsing_rules import *
from Applicant_Tracking_System.scripts.semantic_annalyser import *


class Condidat(object):
    
    def __init__(self):
        self.email = []
        self.name = []
        self.mobile = []
        self.url = []
        self.designation = []
        self.education = None
        self.pro = None
        self.skills = {}
    
    def Extractor(self,raw_text):
        blocks =  ParserFileNew(raw_text)
        print(blocks)
        self.skills = semantic_annalyser.SkillsExtractor(blocks)
        print(self.skills)
        
        blocEtude = ''
        if 'etude' in blocks.keys() :
            for element in blocks['etude']:
                for element_inside in element:
                    sentence =' '.join(element_inside)
                    blocEtude+=sentence+'\n'
            self.education = blocEtude
        else:
            self.education = 'not found'
        
        blocPro = ''
        if 'pro' in blocks.keys():
            for element in blocks['pro']:
                for element_inside in element:
                    sentence =' '.join(element_inside)
                    blocPro+=sentence+'\n'
            self.pro = blocPro
        else:
            self.pro = 'not found'
        
        for element in blocks:
            for block in blocks[element]:
                for ligne in block:
                    if(ligne[0] == 'email'):
                        self.email.append(ligne[1])
                    elif(ligne[0] == 'name'):
                        self.name.append(ligne[1])
                    elif(ligne[0] == 'phone number'):
                        self.mobile.append(ligne[1])
                    elif(ligne[0] == 'url'):
                        self.url.append(ligne[1])
                    elif(ligne[0] == 'designation'):
                        self.designation.append(ligne[1])



