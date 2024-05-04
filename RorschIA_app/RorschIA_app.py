import streamlit as st
import pandas as pd
import deepl
from langdetect import detect

from functions import raw_text_response_eval
from functions import get_np
from functions import evaluate_one_vs_rest_transformer

st.title("RorschIA")

text_entered = st.text_input("Paste the text of your protocol :)")



process_button = st.button("Process")

if process_button == True:
    try:
        evaluation, list_dicts = raw_text_response_eval(text_entered)
        st.write("The protocol was parsed successfully!")
        
        report = st.write("REPORT")
        for figure_dict in list_dicts:
            
            # maybe hacer 3 boxes, 1 para qué figura es/imagen de la figura, otro para la columna y otra para el valor 
            
            # print(figure_dict)
            # print(type(figure_dict))
            for figure in figure_dict:
                response_dict = figure_dict[figure] # list of responses 
                # print(response_dict)
                for individual_response in response_dict:
                    
                    individual_response["Sentence"] = individual_response.pop("response")
                    individual_response["Response"] = individual_response.pop("noun_phrase")
                    individual_response["Determinant label"] = individual_response.pop("determinant")
                    individual_response["Content label"] = individual_response.pop("content")
                
                    for k, v in individual_response.items():
                        
                        if k !="figure":
                            text_report = st.write(k, ":", v)
                        
        # st.write("JSON Results")
        # st.write(list_dicts)
        
        csv = evaluation.to_csv()
        
        st.download_button(label='Download CSV', data=csv, file_name='RorschIA_results.csv', mime='text/csv')
        
    except:
        lang = detect(text_entered)
        if lang == "fr":
            with open("DEEPL_API_KEY.txt", "r") as f:
                API_KEY = f.read()
            translator = deepl.Translator(API_KEY)
            result = translator.translate_text(text_entered, target_lang="EN-US", preserve_formatting=True)
            response = result.text
            
            #GET NP WORKS WITH ENGLISH, no point of doing running get_np with french text
            
            content = evaluate_one_vs_rest_transformer("sentence_transformer_contents_V23-18-04.sav", response)
            determinant = evaluate_one_vs_rest_transformer("sentence_transformer_determinants_V23-18-04.sav", response)
            
            st.write("*Sentence*: {} ".format(text_entered))
            st.write("Response: {} ".format(response))
            st.write("Content: {} ".format(content))
            st.write("Determinant: {} ".format(determinant))
            
        else: # language will be english
            text = text_entered
            response_tuple = get_np(text) # noun phrase segmentation
            if response_tuple[1] == True: #    THERE IS COORDINATION!
                response = response_tuple[0]
                for np in response:
                    content = evaluate_one_vs_rest_transformer("sentence_transformer_contents_V23-18-04.sav", response)
                    determinant = evaluate_one_vs_rest_transformer("sentence_transformer_determinants_V23-18-04.sav", response)
                    
                    st.write("*Sentence*: {} ".format(text_entered))
                    st.write("Response: {} ".format(response))
                    st.write("Content: {} ".format(content))
                    st.write("Determinant: {} ".format(determinant))
            
            else: # No coordination
                response = response_tuple[0]
                content = evaluate_one_vs_rest_transformer("sentence_transformer_contents_V23-18-04.sav", response)
                determinant = evaluate_one_vs_rest_transformer("sentence_transformer_determinants_V23-18-04.sav", response)
                
                st.write("*Sentence*: {} ".format(text_entered))
                st.write("Response: {} ".format(response))
                st.write("Content: {} ".format(content))
                st.write("Determinant: {} ".format(determinant))



