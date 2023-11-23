import pandas as pd
import numpy as np
import re


def year_extraction(sentence_list):
    #######################################################################################
    #                                                                                     
    #   Input: 문장 list                                                                  
    #                                                                                      
    #   Output: year가 포함된 문장 list
    #
    #######################################################################################
    year_sentence_list = []
    
    for x in sentence_list:
        if re.search(r'\b\d{4}\b', x):
            year_sentence_list += [x]
            
    return year_sentence_list


def only_year_extraction(year_sentence):
    #######################################################################################
    #                                                                                     
    #   Input: 한 문장                                                                  
    #                                                                                      
    #   Output: year 네 글자
    #
    #######################################################################################
    match = re.search(r'\b\d{4}\b', year_sentence)
    year = match.group(0)
    
    return year


def construct_year_df(year_json):
    #######################################################################################
    #                                                                                     
    #   Input: 전체 json 파일                                                                 
    #                                                                                      
    #   Output: 전체 인물의 인물별 dataframe 모음
    #
    #######################################################################################
    people_dict = {}
    for person, person_content in year_json.items():
        person_list = []
        for big_topic, big_content in person_content.items():
            if isinstance(big_content, list):
                for sentence in big_content:
                    year = only_year_extraction(sentence)
                    row = pd.Series([year, sentence, big_topic, mid_topic])
                    person_list.append(row)
            else:
                for mid_topic, mid_content in big_content.items():
                    if isinstance(mid_content, list):
                        for sentence in mid_content:
                            year = only_year_extraction(sentence)
                            row = pd.Series([year, sentence, big_topic, mid_topic])
                            person_list.append(row)
                    if not mid_topic:
                        if not mid_content:
                            continue
                        else:
                            for sentence in mid_content:
                                year = only_year_extraction(sentence)
                                row = pd.Series([year, sentence, big_topic, mid_topic])
                                person_list.append(row)
                    else:
                        for sentence in mid_content:
                            year = only_year_extraction(sentence)
                            row = pd.Series([year, sentence, big_topic, mid_topic])
                            person_list.append(row)
        people_dict[person] = pd.DataFrame(person_list)
        
    return people_dict