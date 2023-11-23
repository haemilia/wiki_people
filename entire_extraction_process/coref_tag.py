# Assuming Allen-NLP, spacy and all related packages and models are installed.
import config
import spacy
from allennlp.predictors.predictor import Predictor

def coreference_tag(input_text: str) -> str:
    predictor = Predictor.from_path(config.MODEL_URL)

    spacy_document = predictor._spacy(input_text)
    clusters = predictor.predict(input_text).get("clusters")
    dict_clusters = dict(enumerate(clusters))
    #cLusters에 순번 매겨서 dictionary에 넣기. 처음으로 나오는 인물이 우리가 관심 있는 인물이라는 가정.
    dict_clusters_sorted = sorted(dict_clusters.values(), key=lambda x: x[0][1]-x[0][0])
    #각 인물을 나타내는 coreference clusters list의 첫번쨰 요소를 기준으로 그 길이가 짧은 것부터 긴 순서로 배열.
    #긴 것을 후순위로 보냄으로써 짧은 인물을 덮어쓰게 하기 위함임.

    resolved = list(tok.text_with_ws for tok in spacy_document)

    for cluster in dict_clusters_sorted:
    # The main mention is the first item in the cluster
        mention_start, mention_end = cluster[0][0], cluster[0][1] + 1
        mention_span = spacy_document[mention_start:mention_end]

        replace_tag = [key for key, val in dict_clusters.items() if val == cluster]
        #각 cluster list와 일치하는 value를 갖는 키를 요소로 갖는 replace_tag라는 list에 넣어줌
        replace_tag = f"[{replace_tag[0]}]"

        if replace_tag == '[0]':
        #우리가 관심 있는 인물의 key는 0일 것이고 0인 것들만 숫자로 tagging하겠다는 것.

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
                    #[0]로 바꿔주는 작업
                else:
                    # If not possessive, then replace first token with main mention directly
                    resolved[coref[0]] = replace_tag + final_token.whitespace_
                # Mask out remaining tokens
                for i in range(coref[0] + 1, coref[1] + 1):
                    resolved[i] = ""
        #우리가 관심 있는 인물 이외의 인물들은 숫자로 tagging하지 않고 각 cluster list 첫 요소를 가지고 대체하겠다는 것.
        # replace_tag -> mention_span.textf로 바뀐 거 빼고는 위와 같음.
        else:
            # The coreferences are all items following the first in the cluster
            for coref in cluster:
                final_token = spacy_document[coref[1]]

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