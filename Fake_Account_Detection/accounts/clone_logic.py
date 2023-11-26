import pandas as pd
from rapidfuzz.distance import Levenshtein
import math
# import csv
users_info = pd.read_csv("statics/accounts_info.csv")
no_of_records = len(users_info.index)
clone_similarity = []


def remove_spaces(acc_list):
    for index in range(len(acc_list)):
        acc_list[index] = acc_list[index].replace(" ","")
    return acc_list

def restore_spaces(acc_list):
    for index in range(len(acc_list)):
        for i in range(2,len(acc_list[index])):
            if(acc_list[index][i].isupper()):
                word1 = acc_list[index][0:i]
                word2 = acc_list[index][i:len(acc_list[index])]
                acc_list[index] = f"{word1} {word2}"
                break
    return acc_list
                


def find_similarity(list1,list2):
    similarity = 0
    for i in range(len(list1)):
        s = float(Levenshtein.normalized_similarity(list1[i],list2[i]))
        similarity = similarity + s
    return float(similarity/len(list1))

def get_profiles(input_from_user):
    print(input_from_user)
    my_dictionary = {}
    index = 1
    for i in range(0,no_of_records):
        details = users_info.loc[i, :].tolist()
        details = remove_spaces(details)
        input_from_user = remove_spaces(input_from_user)
        similarity = find_similarity(details,input_from_user)
        input_from_user = restore_spaces(input_from_user)
        my_dictionary["input_from_user"] = input_from_user
        details = restore_spaces(details)
        if similarity >= 0.7 and similarity != 1.0:
            clone_similarity.append(similarity)
            details.append(math.floor(similarity*100))
            my_dictionary["p"+str(index)] = details
            index = index + 1
    return my_dictionary


def get_profile_values(param_dict):
    parameters = []
    for i in param_dict:
        if i == "csrfmiddlewaretoken":
            pass
        else:
            parameters.append(param_dict[i])
    return parameters







