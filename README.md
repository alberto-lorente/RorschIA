# RorschIA

Data cleaning and GPT4ALL explanation

The notebook has two parts as of now: one for cleaning the raw protocols and another one to experiment with open source LLMs to use as classifiers

1. Cleaning the Data
   What I am trying to do here is take the raw protocol, organize it into a useable format and cleaning it a little bit.

   First, I am splitting the text into chunks with regular expressions. That way, we have the responses for each figure separated. I also saaw there was an extra Choix and Rq secion at the end so I am deviding that as well. As you see, the info for each fire is stored in dictionaries and I am saving the raw responses (because they have position markers that we'll use) and then I am cleaning, taking away the markers, the responses so that when we do NLP stuff with them we don't have random characters that will not be helpful.

   Then, for the responses of each figure I am separating the sentences and just labelling them as response_x in a dictionary. The idea behind it is that this way it is easier to access each individual response (since we will have to do stuff for each of them). Also, the if "choix" break is just a safeguard; since choix and rq are sections unrelated to the final response, they should not be included in the responses for the final card. Then I am doing a list of dictionaries for each response and I am saving it in the dictionary as the value for the key 'sentences'.

   The structure produced right now is   list[{dictionary for each figure}, {dictionary for the additional info}]

   and the structure of the dictionary for each figure is {figure_number: *the number of the figure*,
                                                           raw_response: *unprocessed response with all the markers*,
                                                           clean_response: *response with no markers*,
                                                           sentences: [*list of dictionaries for each clean sentences numbered*]}
   
   the structure for the dict for each response for now is just {response_number: *clean response*
                                                                 position: NOT DONE}

   I am breaking down each response into its own dictionary because that way we can access it directy and we can add more information like the position, the noun phrases present in the sentence to eventually get the determinants, syntactic dependencies, whether there are mentions of colors, check the similarity between sentences, etc., plus dictionaries are easily converted into pandas dataframes.

   What would be left to do for this part would be: 1. add a position key where I put it in the explanation above (each individual response can have one) 2. figure out the information we have to extract from each sentence to further preprocess the sentences and add said info to the individual sentence dictionary.


3. GPT4ALL experiment

   I saw this video: https://www.youtube.com/watch?v=h_GTxRFYETY&pp=ygUHdGh1IHZ1IA%3D%3D       where someone uses Ollama to run LLMs locally (so that there are no privacy concerns too) to classify their spendings in categories and thought maybe if we cannot make a model or don't have enough data, we could do smth similar with the categories we have to classify. My final idea would be having propmpts structure in a tree and just run through the tree according to yes or no answers kind of like the drawing i've made. It's pretty bad but it kinda gets the idea across hopefully.

   However, I could not use Ollama so I used GPT4ALL, which is much more primitive I think, instead. An alternative would be using LangChain, a framework to connect the python code with LLM Apis like OpenAI but for that we'd need to have a subscription to them (I tried with a API key I generated in a free account and it said I had exceeded the limit).
