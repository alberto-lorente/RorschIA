#IMPORTING THE DEPENDENCIES

import re
import deepl
import json
import pickle
import pandas
from sklearn.feature_extraction.text import TfidfVectorizer

def get_responses(raw_text):
  
  """This function takes plain text, parses the in-text markers to extract the text corresponding to each Rorschach figure,
  runs the responses through the Deepl API to translate them and returns a dictionary with the responses for each figure properly organized.
  """

  dict_numbers = {"I": 1, "II": 2,
                  "III": 3, "IV": 4,
                  "V": 5, "VI": 6,
                  "VII": 7, "VIII": 8,
                  "IX": 9, "X": 10}

  regex_response_number = '[A-Z]+/'                                # since the responses alway start with the number + \

  list_number_figure = re.findall(regex_response_number, raw_text)  # finds the regex for the number of responses

  text_i = re.split(regex_response_number, raw_text)

  # regex_choix_pos = r'Choix +(.*?)Choix -'

  # regex_choix_neg = r'Choix -(.*?)Rq :'

  # regex_rq = r'Rq :(.*?)\n'
  try: 
      
    text_choix_pos = re.findall(r'Choix \+ :(.*?)\nCh.?', raw_text)[0].strip()

    text_choix_neg = re.findall(r'Choix \- :(.*?)\n', raw_text)[0].strip()

    text_rq = re.findall(r'Rq :(.*?)\n', raw_text)[0].strip()

    additional_info = {"Choix_pos": text_choix_pos, "Choix_neg": text_choix_neg, "Rq": text_rq}
    
  except:
      
      additional_info = {"Choix_pos": "nada", "Choix_neg": "nada", "Rq": "nada"}
      
      print("Additional info not found")

  list_responses = []

  for i in range(len(list_number_figure)):

    if list_number_figure[i] not in text_i[i]:

      j = i + 1 # there is a \n\n string at index 0 so the text actually starts at index 1
      # print("not found")

    else:

      j = i

    dict_responses = {}

    n_response = list_number_figure[i][:-1]

    number = dict_numbers[n_response]

    text_i = re.split(regex_response_number, raw_text)

    full_text = text_i[j].strip()

    regex_line_break = '\n++'

    list_sentences_raw = text_i[j].split(".")

    text_i[j] = re.sub(regex_line_break, " ", text_i[j]) \
                  .replace("@", "") \
                  .replace("^", "") \
                  .replace("V", "") \
                  .replace(">", "") \
                  .replace("  ", " ") \
                  .strip() \

    # DEEPL API TRANSLATION

    with open(r"DEEPL_KEY\DEEPL_API_KEY.txt", "r") as f:
      API_KEY = f.read()

    translator = deepl.Translator(API_KEY)
    result = translator.translate_text(text_i[j], target_lang="EN-US", preserve_formatting=True)

    text_i[j] = result.text

    dict_responses["figure_number"] = number

    dict_responses["raw_response"] = full_text

    dict_responses["clean_response"] = text_i[j]

    list_sentences_clean = text_i[j].split(".")

    clean_sentences = []

    i = 0

    special_markers_list = ["@", "^", "V ", "<", ">",]

    # structuring the sentences inside the while loop

    while i < len(list_sentences_clean):

      if "Choix" in list_sentences_clean[i]:  # if we reach choix, there are no more actual responses by the patient, those are just comments by the psychologist
        break

      elif "Choice" in list_sentences_clean[i]:  # if we reach choix, there are no more actual responses by the patient, those are just comments by the psychologist
        break

      j = i + 1

      # cleaning the sentences and adding the . back at the end of the sentence

      dict_sentence_info = {}

      # use the full_text of the text here to parse, the text[j is clean
      item = list_sentences_clean[i].strip()

      item_2 = list_sentences_raw[i].strip()

      if item != "":                      # split leaves an empty string at the end of the list and by adding a . , we get a "." item at the end of the list
        item = item + "."
        dict_sentence_info["response_{}".format(j)] = item
        clean_sentences.append(dict_sentence_info)


        for marker in special_markers_list:
          if marker in item_2:
            dict_sentence_info["special_marker"] = marker

      j = j + 1

      i = i + 1

    dict_responses["sentences"] = clean_sentences
        # in case we need to double-check

    list_responses.append(dict_responses)

  list_responses.append(additional_info)



  return list_responses

def get_list_figure_responses(og_dict):

    # if you look at the depth of the sentences in the original dictionary,
    # the responses are a list of dictionaries of structure [{response: blablabla, special_marker: blablabla}, {response_2: blablabla, special_marker: blablabla}]
    # to be able to extract the sentences to process them and do the computations that we need to do,
    # i thought it would be nicer to have them without all the fluff of the other dictionary keys, etc.
    # I am just going to make this function to get the 10 figures into 10 dataframes with its responses and drop all the other stuff we dont need
    
    

    responses_list = []

    for figure in og_dict[:-1]:

        figure_sents = figure["sentences"]

        for item in figure_sents:

            item.pop("special_marker", None)
        responses_list.append(figure_sents)

    return responses_list

def clean_dict(responses_fig_list):

    '''merges the dictionary for each the responses of a figure into one response
    to go from a list of dicts [{response: blablabla},  {response: blablabla}, {response: blablabla}]
    to just one dict{response_1: , response_2: , response_3: }

    '''

    new_dict = {}
    for dictionary in responses_fig_list:
            for k , v in dictionary.items():
                # print(k,v)
                new_dict[k]= v
    return new_dict

def transform_dictionary_to_figure_dataframes(og_dictionary):
    '''this function transforms the first dictionary
    into individual response dictionaries for each figure and returns it in list form.
    '''

    responses_list = get_list_figure_responses(og_dictionary)

    clean_fig_1 = clean_dict(responses_list[0])
    clean_fig_2 = clean_dict(responses_list[1])
    clean_fig_3 = clean_dict(responses_list[2])
    clean_fig_4 = clean_dict(responses_list[3])
    clean_fig_5 = clean_dict(responses_list[4])
    clean_fig_6 = clean_dict(responses_list[5])
    clean_fig_7 = clean_dict(responses_list[6])
    clean_fig_8 = clean_dict(responses_list[7])
    clean_fig_9 = clean_dict(responses_list[8])
    clean_fig_10 = clean_dict(responses_list[9])

    list_dicts = [clean_fig_1, clean_fig_2, clean_fig_3, clean_fig_4, clean_fig_5, clean_fig_6, clean_fig_7, clean_fig_8, clean_fig_9, clean_fig_10]

    return list_dicts

def classify_contents(text, model_contents=r"Models\Contents\svm_contents_V1-03-04.sav"):
    
    clf = pickle.load(open(model_contents, "rb"))
    
    prediction = clf.predict([text])[0]
    
    return prediction


def classify_determinants(text, model_determinants=r"Models\Determinants\svm_determinants_V1-03-04.sav"):
    
    clf_determinants = pickle.load(open(model_determinants, "rb"))
    
    prediction = clf_determinants.predict([text])[0]
    
    return prediction


def eval(list_dicts):
    """This function runs the evaluation with our first two models. 
    It takes as input the list of dictionary responses, prints the evaluation 
    and returns the content and determinant labels for each response in dictionary form.   
    """
    evaluation = []
    i = 1
    for dictionary in list_dicts:
        
        figure_number = "Figure_{}".format(i)
        
        dict_evaluation_per_figure = {}
        
        print(figure_number, "\n") 
        
        list_evaluation_figure = []
        
        j = 1
        
        for response in dictionary:
            
            sentence = dictionary[response]
            # print(dictionary[response]) #works until here
            
            content = classify_contents(dictionary[response])
            
            # print(response, content)
            
            determinant = classify_determinants(dictionary[response])
            
            # print(response, content, determinant)
            
            dict_eval = {}
            dict_eval["response"] = sentence
            dict_eval["content"] = content
            dict_eval["determinant"] = determinant
            list_evaluation_figure.append(dict_eval)
            
            print("Response {}: ".format(j), sentence, "\nContent:", content , "\nDeterminant:", determinant, "\n")
            
            j = 1 + j
            
        dict_evaluation_per_figure[figure_number] = list_evaluation_figure
        
        evaluation.append(dict_evaluation_per_figure)
        
        i = i +1
        
    return evaluation

def raw_text_response_eval(raw_text):
    
    responses = get_responses(raw_text)

    list_dicts = transform_dictionary_to_figure_dataframes(responses)

    evaluation = eval(list_dicts)
    
    return evaluation

def translated_dict_response_eval(dictionary): 
    """Use this one if you are working with the demo dictionaries already done to save deepl credits"""
    
    responses = dictionary

    list_dicts = transform_dictionary_to_figure_dataframes(responses)

    evaluation = eval(list_dicts)
    
    return evaluation