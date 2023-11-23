import json

def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data #dictionary
    except FileNotFoundError:
        print("File not found.")
        return None
    except json.JSONDecodeError:
        print("There was an error")
        return None
    
def mergeString(data):
    #한 인물의 모든 정보를 json에서 하나의 XML 태깅이 완료된 string로 합치는 output이 나오는 코드
    #그리고 각 인물의 xml에 어떤 태그가 있는지 태그의 리스트로 output이 나와야 함
    print("어쩌고")


import spacy
nlp = spacy.load("en_core_web_trf")

def tag_nouns(text):
    spacy_document = predictor._spacy(text)
    clusters = predictor.predict(text).get("clusters")

    resolved = list(tok.text_with_ws for tok in spacy_document)

    # The main mention is the first item in the cluster
    for person_index, cluster in enumerate(clusters):
        mention_start, mention_end = cluster[0][0], cluster[0][1] + 1
        mention_span = spacy_document[mention_start:mention_end]
        replace_tag = f"[{person_index}]"

        for coref in cluster:   # The coreferences are all items following the first in the cluster
            final_token = spacy_document[coref[1]]
            # In both of the following cases, the first token in the coreference
            # is replaced with the main mention, while all subsequent tokens
            # are masked out with "", so that they can be eliminated from
            # the returned document during "".join(resolved).
            # The first case attempts to correctly handle possessive coreferences
            # by inserting "'s" between the mention and the final whitespace
            # These include my, his, her, their, our, etc.
            # Disclaimer: Grammar errors can occur when the main mention is plural,
            # e.g. "zebras" becomes "zebras's" because this case isn't
            # being explictly checked and handled.
            if final_token.tag_ in ["PRP$", "POS"]:
                resolved[coref[0]] = replace_tag + "'s" + final_token.whitespace_
            else: # If not possessive, then replace first token with main mention directly
                resolved[coref[0]] = replace_tag + final_token.whitespace_
            for i in range(coref[0] + 1, coref[1] + 1): # Mask out remaining tokens
                resolved[i] = ""

    result = "".join(resolved)
    return result

from spacy.symbols import ORTH

def select_subject(num_tag_text: str, person_id = 0) -> [str]:
    ############################################################################################################################################
    # select_subject(): A function that selects sentences that have the designated person as the subject (active or passive) of the sentence.  #
    #                                                                                       #
    # num_tag_text: text that has replaced the people to number tags
    # person_id: the tag number of the person of interest                                                                           #
    ############################################################################################################################################

    # Add special tokens for people
    for i in range(200):
        nlp.tokenizer.add_special_case(f"[{i}]", [{ORTH: f"[{i}]"}])

    doc = nlp(num_tag_text) #The text that has all people replaced with numbered tags is now processed through spacy
    assert doc.has_annotation("SENT_START")
    selected_sentences = [] #Store all sentences with the main person's tag as the subject inside this list
    for sent in doc.sents: # Go through all the sentences
        sentence_doc = nlp(sent.text) # Run the sentence through spacy again, so that we can look through token by token.
        sentence_added = False 
        for token in sentence_doc: # Go through all the tokens
            if((token.dep_ == "nsubj" or token.dep_ == "nsubjpass") and # If the token is an active or passive subject
               token.text == f"[{person_id}]" and # If the token is referring to the person we're interested in
               not sentence_added):# If we haven't added this sentence to selected_sentences before
                selected_sentences.append(sent) # Then, we can add the sentence to the list
                sentence_added = True
    return selected_sentences


def main():
    file_path = r'C:\Users\inny9\Documents\GitHub\wiki_people\wiki_crawling\txt_dict_2.json'
    
    dictData = read_json_file(file_path)

    #XML로 합친 method, assume that the output is a list of string elements and each element represents each figure
    #output = peopleList
    peopleList = mergeString(dictData)

    allPeople = []

    for person in peopleList:
        taggedString = tag_nouns(person)
        allPeople.append(taggedString)

    



    

#if __name__ == "__main__":
#    main()