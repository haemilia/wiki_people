import json
import spacy
import config
import coref_tag_v2
import category_tagger


def divide_sections_no_summary(people_dict: dict,real_flatten = category_tagger.real_flatten) -> dict:
    divided_dict = {}
    for name, content in people_dict.items():
        flat = real_flatten(content)
        del flat['summary']
        sections_dict = {}
        for topic, flat_content in flat.items():
            sections_dict[topic] = f"{name}. " + flat_content
        divided_dict[name] = sections_dict
    return divided_dict

def save_json(filename:str, json_content: dict, path = MAIN_PATH / "coref_output"):
    # Just helper function
    with open(path / filename, "w") as json_file:
        json.dump(json_content, json_file)

def coref_divided(divided_dict: dict, save_json = save_json):
    for name, content in divided_dict.items():
        for id, (topic, t_content) in enumerate(list(content.items())):
            coref_result = coref_tag_v2.coreference_tag(t_content)
            json_content = {topic: coref_result}
            print(f"completed: {topic} of {name}")
            save_json(f"{name}_{id}_coref.json",json_content, MAIN_PATH / "all_coref_output")

def main():
    ## 내가 실제로 진행했던 흐름:

    # MAIN_PATH = Path(r"C:\Users\lhi30\Haein\2023\YBIGTA\2023-2\DA\Wiki_People\Share")
    # our_path1 = MAIN_PATH / 'wiki_crawling/txt_dict_2_new.json'
    # our_path2 = MAIN_PATH / 'wiki_crawling/name_list_2_new.json'

    # with open(our_path1, 'r') as file:
    #     our_txt = json.load(file)

    # with open(our_path2, 'r') as file:
    #     our_name = json.load(file)

    # haein_name_list = our_name[0:44]
    # haein_text = {}
    # for name in haein_name_list:
    #     haein_text[name] = our_txt[name]

    # divided = divide_sections_no_summary(haein_text)
