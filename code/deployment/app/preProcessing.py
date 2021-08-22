# import for Headline Cleaning
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import pandas as pd
import re
import spacy
from nltk.corpus import sentiwordnet as swn
from nltk.corpus import wordnet as wn
from sentistrength import PySentiStr
from sklearn.feature_extraction.text import TfidfVectorizer
### Workaround for nltk download in Docker
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('sentiwordnet')

# help Functions like in the Notebooks for PreProcessing the Headline
def tokenize_post(headline):
    hl_tokenz = word_tokenize(headline)
    hl_post = nltk.pos_tag(hl_tokenz)
    hl_post_result = []
    for word in hl_post:
        if word[1].startswith('NN'):
            hl_post_result.append([word[0], 'n'])
        elif word[1].startswith('JJ'):
            hl_post_result.append([word[0], 'a'])
        elif word[1].startswith('V'):
            hl_post_result.append([word[0], 'v'])
        elif word[1].startswith('R'):
            hl_post_result.append([word[0], 'r'])
        else:
            hl_post_result.append([word[0], ''])
    return hl_post_result

def remove_stopwords(hl_post_tok_lower):
    stop_words = set(stopwords.words('english')) 
    #custom Stopwords possible:
    # stop_words.add('')
    filtered_sentence = [word for word in hl_post_tok_lower if not word[0] in stop_words]
    return filtered_sentence

#this headline is pos-tagged, tokenzied, lower, and stopwords-removed
lemmatizer = WordNetLemmatizer()
def lemmatize(headline):
    lemmatized_output = []
    for word in headline:
        if word[1] == '':
            lemmatized_output.append((lemmatizer.lemmatize(word[0]), word[1]))
        else:
            lemmatized_output.append((lemmatizer.lemmatize(word[0], pos=word[1]), word[1]))

    lemmatized_output = [word for word in lemmatized_output if len(word[0]) > 2]
    lemmatized_output = [word for word in lemmatized_output if not word[0].isnumeric()]

    return lemmatized_output

def getSynset(headline):
    synset_output = []
    for word in headline:
        synsets = wn.synsets(word[0], pos=word[1])
        if len(synsets)>0:
            synset_output.append((synsets[0].name()))

    return synset_output

#calculate sentiment
def getSentiment(headline):
    senti_pos = 0
    senti_neg = 0
    for word in headline:
        swn_synset = swn.senti_synset(word)
        senti_pos += swn_synset.pos_score()
        senti_neg += swn_synset.neg_score()

    return senti_pos, senti_neg

# POS tagged and tokenzized Array to String
def tokenz_in_sentence(headline):
    word_list = [word[:-5] for word in headline]
    sentence = ' '.join(word_list)
    return sentence

def headline2tf_idf(headline, feature_list, tfidf_vectorizer):
    single_headline_tfidf = pd.DataFrame()
    for feature in feature_list:
        idf_value = tfidf_vectorizer.idf_[tfidf_vectorizer.vocabulary_[feature]]
        count_feature = headline.count(feature)
        single_headline_tfidf[feature] = [(count_feature / len(headline)) * idf_value]
    return single_headline_tfidf




# module Functions
def preProcessing(headlines, feature_list, vectorizer):
    headlines_processed = []
    for headline in headlines:
        headline = headline.lower()
        headline = tokenize_post(headline)
        headline = remove_stopwords(headline)
        headline = lemmatize(headline)
        headline = getSynset(headline)
        headline_senti_pos, headline_senti_neg = getSentiment(headline)
        headline = tokenz_in_sentence(headline) #For TF_IDF
        headline_tf_idf = headline2tf_idf(headline, feature_list, vectorizer)
        headlines_processed.append(headline_tf_idf)
        # headlines_processed.append([headline_senti_pos, headline_senti_neg])

    return headlines_processed

def binaryPrediction(pList):
    pResults = []
    for p in pList:
        if p >= 1: pResults.append(1)
        if p < 1: pResults.append(0)
    return pResults