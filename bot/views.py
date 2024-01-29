from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
import openai
from django.contrib import auth
from django.contrib.auth.models import User
from .models import *
from chatroom.models import Room
from django.http import JsonResponse
from tensorflow.keras.preprocessing.sequence import pad_sequences
import tensorflow as tf
import numpy as np
        from openai import OpenAI
import pandas as pd
import json
import nltk
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.layers import Input, Embedding, LSTM, Dense, GlobalMaxPooling1D, Flatten
from tensorflow.keras.models import Model
import matplotlib.pyplot as plt

# with open('intend.json') as intend:
#         d1 = json.load(intend)

# tags = []
# inputs= []
# responses  = {}
# for intent in d1['intents']:
# #     responses.append(intent['responses'])
#     responses[intent['tag']]=intent['responses']
#     for lines in intent['inputs']:
#         inputs.append(lines)
#         tags.append(intent['tag'])

# data = pd.DataFrame({"inputs":inputs, "tags":tags})
# data

# from tensorflow.keras.preprocessing.text import Tokenizer
# tokenizer = Tokenizer(num_words=2000)
# tokenizer.fit_on_texts(data['inputs'])
# train = tokenizer.texts_to_sequences(data['inputs'])

# from tensorflow.keras.preprocessing.sequence import pad_sequences
# x_train = pad_sequences(train)

# from sklearn.preprocessing import LabelEncoder
# le = LabelEncoder()
# y_train = le.fit_transform(data['tags'])
#tokenizing data, appling padding and encoding output

# input_shape = x_train.shape[1]
# print(input_shape)

# vocabulary = len(tokenizer.word_index)
# print("number of unique words: ",vocabulary)
# output_length = le.classes_.shape[0]
# print("output lenght: ",output_length)

# i = Input(shape=(input_shape))
# x = Embedding(vocabulary+1, 10)(i)
# x= LSTM(10, return_sequences=True)(x)
# x= Flatten()(x)
# x = Dense(output_length, activation="softmax")(x)
# model = Model(i,x)

# model.compile(loss="sparse_categorical_crossentropy", optimizer='adam', metrics=['accuracy'])
# train = model.fit(x_train, y_train, epochs=200)

# plt.plot(train.history['accuracy'],label='training set accuracy')
# plt.plot(train.history['loss'],label='training set loss')
# plt.legend()




# import random
# import string

# def preprocess_inputdata(texts, tokenizer, input_shape):
#     texts_p = []
#     for message in texts:
#         message = [letters.lower() for letters in message if letters not in string.punctuation]
#         message = ''.join(message)
#         texts_p.append(message)

#     prediction_input = tokenizer.texts_to_sequences(texts_p)
#     prediction_input = pad_sequences(prediction_input, maxlen=input_shape)
#     return prediction_input


# def bot(request):
    
#     if request.method == 'POST':
#         message = request.POST.get('message')
#         texts_p = [message]
        
#         prediction_input = preprocess_inputdata(texts_p, tokenizer, input_shape)
#         output = model.predict(prediction_input)
#         output = output.argmax()
#         response_tag = le.inverse_transform([output])[0]
#         response = random.choice(responses[response_tag])
        
#         if response_tag == "goodbye":
#             return JsonResponse({'message': message, 'response': response})


 
        

#     return render(request, 'bot.html')
  

  

# def generate_response(conversation_context, user_input):
    # Preprocess user input
    # user_input = [letters.lower() for letters in user_input if letters.isalnum() or letters.isspace()]
    # user_input = ' '.join(user_input)

    # Append user input to the conversation context
    # conversation_context.append(user_input)

    # Tokenize and pad the entire conversation
    # tokenized_input = tokenizer.texts_to_sequences(conversation_context)
    # padded_input = pad_sequences(tokenized_input, maxlen=max_sequence_length, padding='post')

    # Make a prediction using the loaded model
    # predictions = model.predict(padded_input)

    # Decode the predicted response
    # predicted_response = tokenizer.sequences_to_texts([np.argmax(predictions)])[0]

    # return predicted_response, conversation_context

conversation_context = []


openai_api_key ='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'
openai.api_key = openai_api_key

def ask_openai(message):
    response = openai.Completion.create(
        engine = "text-davinci-003",
        prompt = message,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
  
    answer = response.choices[0].text.strip()
    return answer

def bot(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        # response = generate_response(conversation_context, message)
        response = ask_openai(message)
        # response = 'hello friend,actually openai was suppose to help me give you all answers but, they say my creator must pay for subcription so, till my creator creates my own api am sorry i cant answer any of your questions.openai just started this thing ish . i used chatterbot but its booring and gives wrong vague answers so till i learn tensorflow,panda,npl,small machine lerning, pytorch ...this bot is disfunctional, ok bye'
        
        return JsonResponse({'message':message, 'response':response})


    

    return render(request, 'bot.html')
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                return redirect('home')
            except:
                error_message = 'Error creating account'
                return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = 'Password dont match'
            return render(request, 'register.html', {'error_message': error_message})
    return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

def home(request):
    
    return render(request , 'home.html')
def ask(request):
    
    return render(request , 'ask.html')

def setting(request):
    rooms = Room.objects.all()
    chats= Chat.objects.all()
    return render(request , 'setting.html', {'chats':chats, 'rooms':rooms})
    

def profile(request):
    chats= Chat.objects.all()
    rooms = Room.objects.all()
    return render(request , 'profile.html', {'chats':chats, 'rooms':rooms})

def text_to_speech(request):
     client = OpenAI()
     message = request.POST.get('message')

     v_response = client.audio.speech.create(
     model="tts-1",
     voice="echo",
     input=message,
    )
     

     return render(request, 'bot.html', {'voice_res': v_response})






