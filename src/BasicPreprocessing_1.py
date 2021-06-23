import numpy as np
from nltk.corpus import stopwords
import nltk
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import os
import xml.etree.ElementTree as ET
import json


nltk.download("wordnet")
nltk.download('stopwords')

class PreProcessing1:

    def __init__(self, source_dir, dest_dir):
        self.source_dir = source_dir
        self.dest_dir = dest_dir
        self.documentData = []
        self.corpus = []
        self.commonWords = []
        self.stopWords_list = ["disease", "diseases", "disorder", "symptom", "symptoms", "drug", "drugs", "problems",
                               "problem", "prob", "probs","med", "meds", "pill", "pills", "medicine", "medicines",
                               "medication", "medications","treatment", "treatments", "caps", "capsules",
                               "capsule", "tablet", "tablets", "tabs", "doctor", "dr", "dr.", "doc", "physician",
                               "physicians", "test", "tests", "testing", "specialist","specialists", "side-effect",
                               "side-effects", "pharmaceutical", "pharmaceuticals",
                               "pharma", "diagnosis", "diagnose", "diagnosed", "exam","challenge",
                               "device", "condition", "conditions", "suffer", "suffering", "suffered",
                               "feel", "feeling", "prescription", "prescribe",
                               "prescribed", "over-the-counter", "otc", "a", "about", "above", "after", "again",
                               "against", "all", "am", "an", "and", "any", "are",
                               "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between",
                               "both", "but", "by", "can", "can't", "cannot",
                               "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down",
                               "during", "each", "few", "for", "from",
                               "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd",
                               "he'll", "he's", "her", "here",
                               "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll",
                               "i'm", "i've", "if", "in", "into",
                               "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't",
                               "my", "myself", "no", "nor", "not", "of",
                               "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out",
                               "over", "own", "same", "shan't", "she", "she'd",
                               "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's",
                               "the", "their", "theirs", "them", "themselves",
                               "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've",
                               "this", "those", "through", "to", "too", "under",
                               "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were",
                               "weren't", "what", "what's", "when", "will", "when's", "where", "where's", "which",
                               "while","who", "who's", "whom", "why", "why's", "with", "won't", "would", "wouldn't",
                               "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves",
                               "n't", "'re", "'ve", "'d", "'s", "'ll", "'m",',', '.', ':', ';', '?', '(', ')', '[', ']',
                               '&', '!', '*', '@', '#', '$', '%']
        self.getRootJsonObjectForCorpus()

    '''
            It removes all spaces
    '''

    def remove_spaces(self, text_value):
        new_text_value = ""
        print("Bhanu")
        new = text_value.strip()
        print(new)
        for text in text_value:
            print(len(text))
            print(type(text))
            print(text == '')
            new_text_value += text.replace(" ", "")
        print(new_text_value)
        return  new_text_value

    '''
        It converts string to lower case
    '''
    def convert_lower_case(self, text_value):
        return np.char.lower(text_value)

    '''
        Removes Punctuation from string
    '''

    def remove_punctuation(self, text_value):
        punc_symbols = "!\"#$%&()*+-.,/:;<=>?@[\]^_`{|}~\n"
        for symbol in punc_symbols:
            text_value = np.char.replace(text_value, symbol, ' ')
        return text_value

    '''
        It removes apostrophe from the string
    '''
    def remove_apostrophe(self, text_value):
        return np.char.replace(text_value, "'", "")

    '''
        It removes the single character from the text
    '''
    def remove_single_characters(self, text_value):
        new_text = ""
        text_value_list = text_value.tolist()
        for w in text_value_list.split():
            if len(w) > 1:
                new_text = new_text + " " + w
        return new_text

    '''
        It removes the stopwords from the list
    '''
    def remove_stopwords(self, text_value):
        all_stopwords = stopwords.words('english')
        self.stopWords_list.append(all_stopwords)
        return " ".join(x for x in text_value.split() if x not in self.stopWords_list)


    '''
        Perform the Lemmitaization
    '''
    def perform_lemmatization(self, text_value_list):
        wordnet_lemmatizer = WordNetLemmatizer()
        result = list()
        for text_vale in text_value_list[0]:
            lem_text_value = ""
            for word in text_vale.split():
                lem_word = wordnet_lemmatizer.lemmatize(word)
                if lem_text_value is "":
                    lem_text_value += lem_word
                else:
                    lem_text_value = lem_text_value + " " + lem_word
            result.append(lem_text_value)
        return result

    '''
        Perform Stemming 
    '''
    def perform_stemming(self, text_value_list):
        st = PorterStemmer()
        result = list()
        for text_value in text_value_list:
            stem_text_value = ""
            for word in text_value.split():
                stem = st.stem(word)
                if stem_text_value is "":
                    stem_text_value += stem
                else:
                    stem_text_value = stem_text_value + " " + stem
                result.append(stem_text_value)
        return result

    '''
        It returns list of words from the documentData.
    '''

    def tokenization(self):
        singleWordList = [
            [word for word in document.split() if word not in self.stopWords_list]
            for document in self.corpus
        ]
        return singleWordList

    def valueTokenization(self):
        singleWordList = [
            [word for word in document.split() if word not in self.stopWords_list]
            for document in self.documentData
        ]
        return singleWordList

    '''
        It returns list of list words, whose count of frequency of words is grater than 1.
    '''

    def getCorpusList(self):
        singleWordList = self.tokenization()
        word_count_dict = {}
        for text in singleWordList:
            for token in text:
                word_count = word_count_dict.get(token, 0) + 1
                word_count_dict[token] = word_count
        texts = [[token for token in text if word_count_dict[token] > 1]
                 for text in singleWordList]
        return texts

    '''
        It returns the Most commonly used words from the corpus.
    '''

    def getCommonWords(self):
        frequ = self.getCommonfrequencyWords()
        ret_list = []
        most_list = frequ.most_common(400)
        for value in most_list:
            ret_list.append(value[0])
        return ret_list

    '''
        It returns the Most commonly used words from the corpus, with their frquency.
    '''

    def getCommonfrequencyWords(self):
        commonwordList = self.tokenization()
        joined_list = list()
        for wordsList in commonwordList:
            for words in wordsList:
                joined_list.append(words)
        freq = nltk.FreqDist(joined_list)
        return freq

    '''
        1. Get commonWords from corpus.
        2. Sort the values based on the frequency and return the sorted list.
    '''

    def getTopFrequencyItems(self, number):
        commoList = self.getCommonfrequencyWords()
        sortedItems = sorted(commoList.items(), key=lambda x: x[1], reverse=True)
        ret_list = []
        for value in sortedItems:
            ret_list.append(value[0])
        return ret_list[0:number]

    '''
        Get the commonWords and add them to stop_word list.
    '''

    def addCommonWordsToStopList(self):
        top_freq_list = self.getTopFrequencyItems(1000)
        common_stop_word_list = self.stopWords_list + top_freq_list
        return common_stop_word_list

    '''
        It converts List to string and returns string value

    '''

    def listToString(self, data_list):
        convertList = ''.join(map(str, data_list))
        return convertList

    '''
        1. It converts provided text to lowercase.
        2. It removes the punctuation.
        3. It removes the stopWords from the text.

    '''

    def preProcessingText(self, text_value):
        if text_value is None:
            return ""
        print(len(text_value))
        print(text_value)
        text_value = self.remove_spaces(text_value)
        text_value = self.convert_lower_case(text_value)
        text_value = self.remove_punctuation(text_value)
        text_value = self.remove_apostrophe(text_value)
        text_value = self.remove_single_characters(text_value)
        text_value = self.remove_stopwords(text_value)
        return text_value

    '''
        1. Get commonWords from corpus and add them to stopWordsList.
        2. Preprocess the text_value.
        3. Apply lemmatization for Tokenized words in the List.
    '''

    def valuePreprocessing(self, text_value):
        if text_value == None:
            return ""
        self.documentData.clear()
        pre_proceed_text_value = self.preProcessingText(text_value)
        self.documentData.append(pre_proceed_text_value)
        tokens_list = self.valueTokenization()
        lem_out_put = self.perform_lemmatization(tokens_list)
        stem_out_put = self.perform_stemming(lem_out_put)
        data = self.remove_punctuation(stem_out_put)
        for output in data:
            return ' '.join(map(str, output))

    '''
        1. List out all sub-directories
        2. Enumearte all folders and retrieve all xml files.
        3. Using ET, parse the root object from XML file.
    '''

    def getRootJsonObject(self):
        sub_dirs = os.listdir(self.source_dir)
        self.stopWords_list = self.addCommonWordsToStopList()
        for folder in sub_dirs:
            sub_folders = os.listdir(self.source_dir + '/' + folder)
            for sub_folder in sub_folders:
                trec_dir = self.dest_dir + '/' + folder + '/' + sub_folder

                if not os.path.exists(trec_dir):
                    os.makedirs(trec_dir)

                xml_files = os.listdir(self.source_dir + '/' + folder + '/' + sub_folder)

                for file in xml_files:
                    tree = ET.parse(self.source_dir + '/' + folder + '/' + sub_folder + '/' + file)
                    root = tree.getroot()
                    base = os.path.split(file)
                    fileName = os.path.splitext(base[1])
                    output_file_path = self.dest_dir + '/' + folder + '/' + sub_folder + '/' + fileName[0]
                    self.prepareJsonObject(root, output_file_path)

    '''
        1. List out all sub-directories
        2. Enumearte all folders and retrieve all xml files.
        3. Using ET, parse the root object from XML file.
    '''

    def getRootJsonObjectForCorpus(self):
        sub_dirs = os.listdir(self.source_dir)
        for folder in sub_dirs:
            sub_folders = os.listdir(self.source_dir + '/' + folder)
            for sub_folder in sub_folders:
                trec_dir = self.dest_dir + '/' + folder + '/' + sub_folder
                if not os.path.exists(trec_dir):
                    os.makedirs(trec_dir)
                xml_files = os.listdir(self.source_dir + '/' + folder + '/' + sub_folder)
                for file in xml_files:
                    tree = ET.parse(self.source_dir + '/' + folder + '/' + sub_folder + '/' + file)
                    root = tree.getroot()
                    self.corpusPrepration(root)

    def isDirectoy(self, path):
        return os.path.isdir(path)

    def isFile(self, path):
        return os.path.isfile(path)

    '''
        1. It appends the key value pairs in to data dict.
        2. Prepares a JSON_Object
        3. Write the JSON object in to output file.

    '''

    def prepareJsonObject(self, root, output_file_path):
        data = {}
        for subRootElement in root:
            data[subRootElement.tag] = []
            if len(subRootElement) == 0:
                if subRootElement.tag != "brief_title" or "article-title" or "abstract" or "introduction" or "conclusion":
                    data[subRootElement.tag] = subRootElement.text
                else:
                    data[subRootElement.tag] = self.valuePreprocessing(subRootElement.text)
            for j in subRootElement:
                j_value = j.text
                if j.tag == "textblock" or "article-title" or "abstract" or "introduction" or "conclusion":
                    j_value = self.valuePreprocessing(j_value)
                data[subRootElement.tag].append({
                    j.tag: j_value
                })
        json_object = json.dumps(data, indent=1)
        with open(output_file_path + '.json', 'w') as outfile:
            outfile.write(json_object)

    '''
        1. It appends the key value pairs in to data dict.
        2. Prepares a JSON_Object
        3. Prepares corpus(documentData) with all files data.

    '''

    def corpusPrepration(self, root):
        data = {}
        for index, subRootElement in enumerate(root):
            data[subRootElement.tag] = []
            if len(subRootElement) == 0:
                data[subRootElement.tag] = self.preProcessingText(subRootElement.text)

            for j in subRootElement:
                data[subRootElement.tag].append({
                    j.tag: self.preProcessingText(j.text)
                })
        json_object = json.dumps(data, indent=1)
        json_object = json.loads(json_object)
        fileData = list()
        for key, value in json_object.items():
            if isinstance(value, list):
                for element in value:
                    if isinstance(element, dict):
                        for _, value in element.items():
                            fileData.append(str(value))
                    else:
                        fileData.append(str(value))
        self.corpus.append(self.listToString(fileData))


#basic_preprocessing = PreProcessing1('./Data/TREC_2019_input_data', './Data/TREC_2019_Output_data')
basic_preprocessing = PreProcessing1('/home/junhua/trec/Trec2021/Data/SampleinputData', '/home/junhua/trec/Trec2021/Data/Sampleoutputdata')
basic_preprocessing.getRootJsonObject()







