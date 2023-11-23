# Assuming Allen-NLP, spacy and all related packages and models are installed.
import config
import spacy
from allennlp.predictors.predictor import Predictor

def coreference_tag(input_text: str) -> str:
    predictor = Predictor.from_path(config.MODEL_URL)

    spacy_document = predictor._spacy(input_text)
    clusters = predictor.predict(input_text).get("clusters")
    dict_clusters = dict(enumerate(clusters))
    dict_clusters_sorted = sorted(dict_clusters.values(), key=lambda x: x[0][1]-x[0][0])

    resolved = list(tok.text_with_ws for tok in spacy_document)

    for cluster in dict_clusters_sorted:
    # The main mention is the first item in the cluster
        mention_start, mention_end = cluster[0][0], cluster[0][1] + 1
        mention_span = spacy_document[mention_start:mention_end]

        replace_tag = [key for key, val in dict_clusters.items() if val == cluster]
        replace_tag = f"[{replace_tag[0]}]"

        if replace_tag == '[0]':

            # The coreferences are all items following the first in the cluster
            for coref in cluster:
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
                else:
                    # If not possessive, then replace first token with main mention directly
                    resolved[coref[0]] = replace_tag + final_token.whitespace_
                # Mask out remaining tokens
                for i in range(coref[0] + 1, coref[1] + 1):
                    resolved[i] = ""
        else:
            # The coreferences are all items following the first in the cluster
            for coref in cluster:
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
                    resolved[coref[0]] = mention_span.text + "'s" + final_token.whitespace_
                else:
                    # If not possessive, then replace first token with main mention directly
                    resolved[coref[0]] = mention_span.text + final_token.whitespace_
                # Mask out remaining tokens
                for i in range(coref[0] + 1, coref[1] + 1):
                    resolved[i] = ""

        result = "".join(resolved)
    return result