import pandas as pd
import sqlite3
import re
import spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import AdaBoostClassifier
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from keras.preprocessing.text import Tokenizer
from keras.preprocessing import sequence 
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense

stopWords = set(stopwords.words('german'))
nlp = spacy.load('de_core_news_sm') 

REPLACE_NO_SPACE = re.compile("(\.)|(\;)|(\:)|(\!)|(\')|(\?)|(\,)|(\")|(\()|(\))|(\[)|(\])")
REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")

def text_normalizer(text):
    text = REPLACE_NO_SPACE.sub("", text.lower())
    text = REPLACE_WITH_SPACE.sub(" ", text)

    return text

def delete_stopwords(text):
    words = word_tokenize(text)
    words_filtered = [word for word in words if word not in stopWords ]
    text_filtered = " ".join(words_filtered)
    
    return text_filtered

def lemmatize_words(text):
    text_for_lemmatization = nlp(text)
    text_lemmatized = [token.lemma_ for token in text_for_lemmatization]
    text_end = " ".join(text_lemmatized)
    
    return text_end

conn = sqlite3.connect('corpus.sqlite3')
data = pd.read_sql_query('SELECT Posts.Headline, Posts.Body, Annotations_consolidated.Category, Annotations_consolidated.Value FROM Posts INNER JOIN Annotations_consolidated ON Posts.ID_Post = Annotations_consolidated.ID_Post',conn)

data = data[data['Category'].str.match("SentimentNegative|SentimentNeutral|SentimentPositive")]
data = data[data['Value'] == 1]
#neutral_data = data[data['Category'] == "SentimentNeutral"]
#positive_data = data[data['Category'] == "SentimentPositive"]
data.fillna(value='', inplace=True)

data['Text'] = data['Headline'] + data['Body']

data.replace("SentimentNegative", -1, inplace=True)
data.replace("SentimentNeutral", 0, inplace=True)
data.replace("SentimentPositive", 1, inplace=True)

data.drop(['Headline', 'Body', 'Value'], axis=1, inplace=True)

data['Text'] = data['Text'].map(text_normalizer)
data['Text'] = data['Text'].map(delete_stopwords)
#data['Text'] = data['Text'].map(lemmatize_words)

token = Tokenizer()
token.fit_on_texts(data['Text'])
X = token.text_to_sequences(data['Text'])
#cv = CountVectorizer()
#cv.fit(data['Text'])
#X = cv.transform(data['Text'])

print(X)

X_train, X_val, Y_train, Y_val = train_test_split(
    X, data['Category'], train_size = 0.8
) 

top_words = 5000
max_review_length = 500 
embedding_vector_length = 32

X_train = sequence.pad_sequences(X_train.toarray(), maxlen=max_review_length) 
X_val = sequence.pad_sequences(X_val.toarray(), maxlen=max_review_length) 

model = Sequential()
model.add(Embedding(top_words, embedding_vector_length, input_length=max_review_length))
model.add(LSTM(100)) 
model.add(Dense(1, activation='sigmoid')) 
model.compile(loss='binary_crossentropy',optimizer='adam', metrics=['accuracy']) 
print(model.summary())

model.fit(X_train, Y_train, validation_data=(X_val, Y_val), nb_epoch=5, batch_size=64) 