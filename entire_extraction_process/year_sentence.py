import pandas as pd
import numpy as np
import re

#######################################################################################
#                                                                                     
#   Input: 문장 list                                                                  
#                                                                                      
#   Output: year가 포함된 문장 list
#
#######################################################################################


def year_extraction(sentence_list):
    year_sentence_list = []
    
    for x in sentence_list:
        if re.search(r'\b\d{4}\b', x):
            year_sentence_list += [x]
            
    return year_sentence_list


# err_lst = []

# for k1, v1 in txt1_dup.items():
#     for k2, v2 in v1.items():
#         if type(v2)==str:
#             v1[k2] = year_extraction(sent_tokenize(v2))
#         else:
#             for k3, v3 in v2.items():
#                 try:
#                     v2[k3] = year_extraction(sent_tokenize(v3))
#                 except:
#                     err_lst += [k1, k2, k3, v3]