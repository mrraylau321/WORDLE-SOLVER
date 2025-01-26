import requests
import json
import time
import random
import numpy as np
from itertools import product

words_alpha = set(requests.get('https://raw.githubusercontent.com/dwyl/english-words/refs/heads/master/words_alpha.txt').text.split('\n'))  #dwyl/english-words Alpha only
words_alpha = [word.strip().lower() for word in words_alpha]                                #Lower case and remove space or \r                   

baseurl = 'https://wordle.votee.dev:8000/'                                                  #Base URL
endpoint = input('Enter the mode of the game (daily / random / manual): ').strip().lower()  #Enter game mode

if endpoint != 'manual':
    size = input("Enter the target word size (default: 5): ")                               #Manual input size
    try:
        size = int(size)                                                                    #Turn input to integer
    except:
        print("Using default size length: 5")   
        size = 5                                                                                                          
else:
    targetword = input("Enter your manual word: ")
    endpoint = f'word/{targetword}'                                                         #Format as described
    size = len(targetword)                                                                  #Manual mode not required size input, used to filter words list

words = [word for word in words_alpha if len(word)== size]                                  #Filter the words_list
seed = random.randint(0,int("FFFFFFFF",16)) if endpoint == 'random' else None               #Random seed for random game, else None
spare_arr = np.zeros(size*26).reshape(size, 26)                                             #Creating array for guessing not in the large word alpha list

def guess_func(endpoint, guess, size = 5, seed = None):
    #Main Guess Function
    global baseurl
    url = baseurl + endpoint
    para = {
        'guess': guess,
    }
    if seed != None: para['seed'] = seed
    if 'word/' not in endpoint: para['size'] = size

    result = requests.get(url, para)
    max_retries = 5
    retry = 0
    while result.status_code != 200:
        if retry <= max_retries:
            print('Connection failed, retry in 2 seconds')
            time.sleep(2)
            result = requests.get(url, params=para)
            retry +=1
        else:
            raise Exception(f"Maximum retries exceed. Status Code:{result.status_code}")
    return json.loads(result.text)

guess = random.choice(words)                                                                #Pick a random guess in the words list
corrected = False
guesscount = 1

while corrected != True:
    guess_result = guess_func(endpoint, guess = guess, size = size, seed=seed)              #Guess the result
    corrected = True                                                                        #Assume the guess is correct
    for i in range(size):                                                                   #Loop through the word size
        checkingchar = guess[i]                                                             #Get character
        res = guess_result[i]['result']                                                     #Get the result of each position
        if res == 'absent':                                                 
            corrected = False                                                               #Any wrong makes the guess is not correct
            words = [word for word in words if checkingchar not in word]                    #Filter the word list to ensure the character is absent
            spare_arr[:, ord(checkingchar)-97] = -1                                         #Update all position not contains the character
        elif res == 'correct':
            words = [word for word in words if word[i] == checkingchar]                     #Filter the word list to ensure the character in the exact poistion
            spare_arr[i,:] = -1                                                             #Excludes all other combinations
            spare_arr[i, ord(checkingchar)-97] = 1                                          #Leave only a specific character which is correct
        else:
            corrected = False                                                               #Any wrong makes the guess is not correct
            spare_arr[i, ord(checkingchar)-97] = -1                                         #Filter out the specific poistion contains the character
            for j in range(size):
                if spare_arr[i, j] == 0:                                                    #Make a mark that may include the character except the filtered one
                    spare_arr[i, j] = 0.5
            words = [word for word in words if (checkingchar in word and word[i] != checkingchar)]  #Update the words list                 
    
    if guess in words: words.remove(guess)                                                  #Ensure the guess not be repeated if not successful filtered

    if corrected:
        print(f"The program spent {guesscount} times to get the correct answer.")
        print(f'The word is {guess}')
        break
    else:
        print(f"The {guesscount} guess is {guess} but incorrect, generating next guess..")
        try:
            guess = random.choice(words)                                                    #Try to pick another guess from the words list
        except:                                                                             #If unable to choose words, the word must be out of the word alpha lists
            print("The word is not found in the large words list, retry with another method.")
            temp = []                                                                       #Creating an empty list
            for i in range(size):                                                           #Loop through the word length
                temp.append([])                                                             
                temp[i] = []                                                                #Creating array for each position
                for j in range(26):                                                         #Loop through all characters
                    if spare_arr[i,j] >= 0:                         
                        temp[i].append(chr(j+97))                                           #Update the temp list to leave all possible characters for each position
            combinations = list(product(*temp))                                             #Combine the temp list          
            words = [''.join(combo) for combo in combinations]                              #Update the words list accordingly
            for j in range(26):                                                             #Loop through all characters
                exist = np.sum(spare_arr[:,j])                                              #Check the existance of character that updated with 0.5 
                if exist > 0:
                    words = [word for word in words if chr(97+j) in word]                   #Filter out all words without the character confirmed existed
            guess = random.choice(words)                                                    #Pick a random guess from the new words list instead

        guesscount += 1                                                                     #Update the count of Guess
