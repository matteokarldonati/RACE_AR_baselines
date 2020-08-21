import json
import nltk
import os
from nltk import sent_tokenize, word_tokenize

from perturbations import get_names_groups, get_adv_names, replace_names, get_entities, get_adv_entities, \
    replace_entities

nltk.download('punkt')


def tokenize(st):
    # TODO: The tokenizer's performance is suboptimal
    ans = []
    for sent in sent_tokenize(st):
        ans += word_tokenize(sent)
    return " ".join(ans).lower()


if __name__ == "__main__":
    difficulty_set = ["middle", "high"]
    data = "../data/data"
    raw_data = "../../drive/My Drive/Colab Notebooks/noahlab/RACE"
    cnt = 0
    avg_article_length = 0
    avg_question_length = 0
    avg_option_length = 0
    num_que = 0

    perturbation_num = 25
    perturbation_type = 'names'

    for data_set in ["test"]:
        p1 = os.path.join(data, data_set)
        if not os.path.exists(p1):
            os.mkdir(p1)
        for d in difficulty_set:
            new_data_path = os.path.join(data, data_set, d)
            if not os.path.exists(new_data_path):
                os.mkdir(new_data_path)
            new_raw_data_path = os.path.join(raw_data, data_set, d)
            for inf in os.listdir(new_raw_data_path):
                cnt += 1

                obj = json.load(open(os.path.join(new_raw_data_path, inf), "r"))

                article = obj["article"]

                if perturbation_type == 'names':
                    names = get_names_groups(article)

                if perturbation_type in ['ORG', 'GPE', 'LOC', 'NORP']:
                    entities = get_entities(article, perturbation_type)

                for _ in range(perturbation_num):

                    if perturbation_type == 'names':
                        adv_names = get_adv_names(len(names), None)
                        obj["article"] = replace_names(article, names, adv_names)
                    if perturbation_type in ['ORG', 'GPE', 'LOC', 'NORP']:
                        adv_entities = get_adv_entities(len(entities), perturbation_type)
                        obj["article"] = replace_entities(article, entities, adv_entities)

                    obj["article"] = obj["article"].replace("\\newline", "\n")
                    obj["article"] = tokenize(obj["article"])
                    avg_article_length += obj["article"].count(" ")
                    for i in range(len(obj["questions"])):
                        num_que += 1

                        if perturbation_type == 'names':
                            obj["questions"][i] = replace_names(obj["questions"][i], names, adv_names)

                        if perturbation_type in ['ORG', 'GPE', 'LOC', 'NORP']:
                            obj["questions"][i] = replace_entities(data_raw["questions"][i], entities, adv_entities)

                        obj["questions"][i] = tokenize(obj["questions"][i])
                        avg_question_length += obj["questions"][i].count(" ")
                        for k in range(4):

                            if perturbation_type == 'names':
                                obj["options"][i][k] = replace_names(obj["options"][i][k], names, adv_names)

                            if perturbation_type in ['ORG', 'GPE', 'LOC', 'NORP']:
                                obj["options"][i][k] = replace_entities(obj["options"][i][k], entities, adv_entities)

                            obj["options"][i][k] = tokenize(obj["options"][i][k])
                            avg_option_length += obj["options"][i][k].count(" ")
                    json.dump(obj, open(os.path.join(new_data_path, inf), "w"), indent=4)
    '''print "avg article length", avg_article_length * 1. / cnt
    print "avg question length", avg_question_length * 1. / num_que
    print "avg option length", avg_option_length * 1. / (num_que * 4)'''
