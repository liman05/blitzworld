import tensorflow as tf
import numpy as np
import pandas as pd
import json
import nltk
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.layers import Input, Embedding, LSTM, Dense, GlobalMaxPooling1D, Flatten
from tensorflow.keras.models import Model
import matplotlib.pyplot as plt

with open('intends.json') as intend:
    d1 = json.load(intend)

tags = []
inputs= []
responses  = {}
for intent in d1['intents']:
#     responses.append(intent['responses'])
    responses[intent['tag']]=intent['responses']
    for lines in intent['inputs']:
        inputs.append(lines)
        tags.append(intent['tag'])

data = pd.DataFrame({"inputs":inputs, "tags":tags})
data

from tensorflow.keras.preprocessing.text import Tokenizer
tokenizer = Tokenizer(num_words=2000)
tokenizer.fit_on_texts(data['inputs'])
train = tokenizer.texts_to_sequences(data['inputs'])

from tensorflow.keras.preprocessing.sequence import pad_sequences
x_train = pad_sequences(train)

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
y_train = le.fit_transform(data['tags'])
#tokenizing data, appling padding and encoding output

input_shape = x_train.shape[1]
print(input_shape)

vocabulary = len(tokenizer.word_index)
print("number of unique words: ",vocabulary)
output_length = le.classes_.shape[0]
print("output lenght: ",output_length)

i = Input(shape=(input_shape))
x = Embedding(vocabulary+1, 10)(i)
x= LSTM(10, return_sequences=True)(x)
x= Flatten()(x)
x = Dense(output_length, activation="softmax")(x)
model = Model(i,x)

model.compile(loss="sparse_categorical_crossentropy", optimizer='adam', metrics=['accuracy'])
train = model.fit(x_train, y_train, epochs=200)

plt.plot(train.history['accuracy'],label='training set accuracy')
plt.plot(train.history['loss'],label='training set loss')
plt.legend()

model.save('blitzbot_response')

# import random
# import string

# while True:
#     texts_p = []
#     prediction_input = input('you: ')
    
#     prediction_input = [letters.lower() for letters in prediction_input if letters not in string.punctuation]
#     prediction_input = ''.join(prediction_input)
#     texts_p.append(prediction_input)
#     #remove punctuatuion above oh
    
#     prediction_input = tokenizer.texts_to_sequences(texts_p)
#     prediction_input = np.array(prediction_input).reshape(-1)
#     prediction_input = pad_sequences([prediction_input], input_shape)
    
#     output= model.predict(prediction_input)
#     output = output.argmax()
#     #getting output from model
    
#     response_tag = le.inverse_transform([output])[0]
#     print("bot: ", random.choice(responses[response_tag]))
#     if response_tag == "goodbye":
#         break
    