Prototype for rorschIA 03-04.

The current functionalities are the following: the script parses the text, it organizes it and translates it. Then it splits the sentence based on punctuation and it runs each sentence through two SVM-tfidf models, one for contents and another one for determinants. Finally, it prints a little report in English for each figure and response. 

* The developemnt python notebook is included in case there`s anyone interested in having a deeper look under the hood. 

How to use the prototype:

- For convenience. copy-paste the protocol you want to evaluate into a .txt file in this folder. 

- Go to the terminal and navigate to this folder.

- Once you are in this folder, write the following command in the terminal: "py .\working_prototype_03-04.py". This will start the script.

- Next, you will be asked to write the path of the file. Since you will have copy-pasted the file to the current folder, you just have to write the name of the file, for example, "my_file.txt", and press enter. After a few seconds, you should get a mini-report in the terminal.


Some considerations:

- The script relies on certain regular expressions we are using to parse the text. We took those markers from the first brute protocol we were sent (I will include it in within the Dev Notebook folder). Please make sure the protocols have the roman numeral numbers + / before the responses for each figure. 
		For example: 

	"I/ @ ^ Une sorte de coléoptère avec des (...) 
	II/ V Deux personnages en train d’établir un contact ou un combat parce qu’il y a du sang ou une jambe qui a été coupée. (...)" and so on.

- Since the app uses DEEPL to translate the text, you will have to create a free API key and copy and paste it in the file called DEEPL_API_KEY. You will find all the info on how to create the key here: https://www.deepl.com/es/pro-api?cta=header-pro-api.

- For this prototype the final results are shown in English but we can reverse the sentences to French, as they were originally.

- As of now, the app computes Determinants and Contents. The contents model has an Accuracy of around 59 % and the determinants model around 30 %.
