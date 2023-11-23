import spacy
from spacy.matcher import Matcher
from spacy.util import filter_spans
from spacy.symbols import ORTH
import re

nlp = spacy.load("en_core_web_trf")


def summarize(sentence: str, original_main_subject: str,  main_subject_tag = "[0]") -> [str]:
   
    pattern = [
    {"LEMMA": main_subject_tag, "DEP": {"in": ["nsubj", "nsubjpass", "ROOT"]}, "OP": "+"},
    {"POS": {"in": ["VERB", "AUX", "ROOT"]}, "OP": "+"},
    {"OP": "*"},
    {"LEMMA": {"in":[".", "!", "?"]}, "OP": "!"},
    {"DEP": {"in": ["dobj", "attr", "prep"]}, "OP": "*"},
    ]

    nlp.tokenizer.add_special_case(main_subject_tag, [{ORTH: main_subject_tag}])
    doc = nlp(sentence)
    matcher = Matcher(nlp.vocab)
    matcher.add("FindAction", [pattern])

    matches = matcher(doc)

    spans = [doc[start+1:end] for _, start, end in matches]
    filtered =  filter_spans(spans)
    tag = re.compile(r'\[0\]')
    result_list = []
    for span in filtered:
        span_text = ""
        for tok in span:
            if tag.search(tok.text):
                span_text += original_main_subject
            else:
                span_text += tok.text_with_ws
        result_list.append(span_text)

    return result_list