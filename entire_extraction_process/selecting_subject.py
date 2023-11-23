import spacy
from spacy.symbols import ORTH

nlp = spacy.load("en_core_web_trf") #Load spacy model


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

def tagged_stentences(peopleList):
    allPeople = {}
    for key, value in peopleList:
        taggedString = select_subject(value)
        allPeople[key] = taggedString