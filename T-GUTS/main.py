import nltk
from nltk.util import ngrams
from random import choice, randint
from gtts import gTTS

import re
import string
import numpy as np

tokens = []
bigrams = []
markov_dict = {}

generated_text = ""
current_word = ''
sentences = 0
next_word = ''
current_word = ''

user_prompt = " "
user_data = " "

language = 'en'


punctuations = ['.', ':', ';', '!', '?']

def loadup():
    user_data_file = input("File to use as database: ")

    global texts
    global user_data
    # Starting sample text to generate from
    texts = ["Welcome to T-GUTS, a text-generator currently under testing stage. We hope to provide you with useful information and support throughout your experience. Feel free to ask us any questions you may have.",
             "T-GUTS is a text-generator that is still in the testing stage, but we are dedicated to providing you with the best information and support possible. We welcome any feedback you may have to help us improve our service.",
             "T-GUTS is a text-generator that is here to assist you with any information or support you may need. We understand that we are still in the testing stage and appreciate any feedback you can provide to help us improve and provide you with the best service possible."]
    
    with open(user_data_file, 'r', errors='ignore') as user_data_file:
        user_data = user_data_file.read()

    user_data = user_data.replace('â€™', '\'')
    user_data = user_data.replace('Ã¥', 'å')
    user_data = user_data.replace('Ã…', 'Å')
    user_data = user_data.replace('Ã¤', 'ä')
    user_data = user_data.replace('ðŸ˜ ” Ã „ ', 'Ä')
    user_data = user_data.replace('Ã¶', 'ö')

    texts[randint(0, len(texts) - 1)] += user_data

def process_current_text():
    # Tokenize the text
    text_random_index = randint(0, len(texts) - 1)
    text = texts[text_random_index]
    
    tokens = nltk.word_tokenize(text)
    
    # Create a list of bigrams
    bigrams = list(ngrams(tokens, 2))

    # Create a dictionary of bigrams and the frequency of the word that follows them
    for bigram in bigrams:
        if bigram[0] in markov_dict:
            if bigram[1] in markov_dict[bigram[0]]:
                markov_dict[bigram[0]][bigram[1]] += 1
            else:
                markov_dict[bigram[0]][bigram[1]] = 1
        else:
            markov_dict[bigram[0]] = {bigram[1]: 1}

def generate_new_text():
    # Generate a new text
    generated_text = []
    current_word = choice(list(markov_dict.keys()))
    generated_text.append(current_word)

    # Generate a new word based on the previous word
    sentences = 0
    while sentences < randint(1, 10):
        if current_word in markov_dict:
            total = sum(markov_dict[current_word].values())
            probs = [markov_dict[current_word][key]/total for key in markov_dict[current_word].keys()]
            next_word = np.random.choice(list(markov_dict[current_word].keys()), p=probs)
            if next_word in ['.', '!', '?']:
                sentences += 1
            generated_text.append(next_word)
            current_word = next_word
        else:
            current_word = choice(list(markov_dict.keys()))

    # Remove the spaces before punctuations
    generated_text = " ".join(generated_text)
    generated_text = re.sub(r"\s([?.!,;:])", r"\1", generated_text)

    speech = gTTS(text=generated_text, lang=language, slow=False, tld='com.us')
    speech.save('message.mp3')
    print("\nT-GUTS: " + generated_text)

def user_input():
    global texts
    global user_data

    user_prompt = input("\nUser: ")

    if user_prompt.startswith('/'):
        commands(user_prompt)
    else:
        # Saves the user's prompt to the texts
        text_random_index = randint(0, len(texts) - 1)
        texts[text_random_index] += ". " + user_prompt

        # Saves the user's prompt to the user data string
        if user_data[-1] not in punctuations:
            user_data += punctuations[randint(0, len(punctuations) - 1)] + ' ' + user_prompt
        else:
            user_data += ' ' + user_prompt

def commands(input_string):
    if input_string == "/help":
        print("""\nCommands:
                   /help      - Shows a list of all commands
                   /saveuser  - Saves only the user's data
                   /saveall   - Saves all data (including starting prompts)""")

    if input_string == "/saveuser":
        # Saves the current text data to a .txt file
            with open("user.txt", 'w') as file:
                data_to_write = user_data
                file.write(str(data_to_write))
            print("\nSuccessfully saved your database to: user.txt")
    
    if input_string == "/saveall":
        # Saves the current text data to a .txt file
            with open("all.txt", 'w') as file:
                data_to_write = texts
                file.write(str(data_to_write))
            print("\nSuccessfully saved your full database to: all.txt")




def loop():
    process_current_text()
    generate_new_text()
    user_input()

if __name__ == '__main__':
    loadup()
    while True:
        loop()