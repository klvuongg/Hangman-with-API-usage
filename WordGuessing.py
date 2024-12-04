import random
import requests

# Fetch words from an API
def fetch_words(api_url):
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            return [word["word"] for word in response.json()]  # Assuming the API returns a JSON list of words
        else:
            print(f"Error fetching words: {response.status_code}")
            return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Word bank and game setup
word_bank = []
api_url = "https://api.datamuse.com/words?ml=word"  

word_bank.extend(fetch_words(api_url))
if not word_bank:
    print("No words available from the API. Exiting...")
    exit()
    

word = random.choice(word_bank)
guessedWord = [' ' if char == ' ' else '-' if char == '-' else '_' for char in word]
attempts = 8
guessedLetters = set()
hang = ["_______",
    "|",
    "|",
    "|",
    "|",
    "|",
    "|",
    "___"]
man = ["     |",
       "   (O.O)", # Happy face
       "     |",
       "     /",
       "|",
       "\\",
       "     /",
       " \\"]

def update_hangman(hang, man, wrong_attempts):
    index = len(man) - wrong_attempts 
    if index < len(man):
        if index == 0:  # Rope
            hang[1] = "| " + man[index]
        elif index == 1:  # Head
            hang[2] = "| " + man[index]
        elif index == 2:  # Upper body
            hang[3] = "| " + man[index]
        elif index == 3:  # Left hand
            hang[4] += man[index]
        elif index == 4:  # Lower body
            hang[4] += man[index]
        elif index == 5:  # Right hand
            hang[4] += man[index]
        elif index == 6:  # Left leg
            hang[5] += man[index]
        elif index == 7: # Right leg
            hang[5] += man[index]

while attempts > 0:
    print('\nCurrent word: ' + ' '. join(guessedWord))
    guess = input('Guess a letter or the whole word: ')

    if not guess.isalpha():
        print('Invalid input! Please guess an alphabetic character.')
        continue

    if guess in guessedLetters:
        print(f'You have already guessed "{guess}". Try a different letter/word!')
        continue
    guessedLetters.add(guess)
    print(f'You have tried {guessedLetters}')

    if guess in word:
        if len(guess) > 1:
          for i in range(len(word)):
             if word[i] == guess[i]:
               guessedWord[i] = guess[i]
        elif len(guess) == 1:
            for i in range(len(word)):
             if word[i] == guess:
               guessedWord[i] = guess
        print('Great guess!')
    else:
        update_hangman(hang, man, attempts)
        attempts -= 1
        print('Wrong guess! You have ' + str(attempts) + ' attempts left!')
        

    if '_' not in guessedWord:
        print('\nCongratulations! You guessed the word: ' + word)
        if len(guessedLetters) == 1:
            print('\nYou guessed correctly in: 1 guess!')
        elif len(guessedLetters) > 1:
            print('\nYou guessed correctly in: ' + str(len(guessedLetters)) + ' guesses!')
        break
    elif attempts == 0:
        man[1] = "   (X.X)"  # Update face to dead
        hang[2] = "| " + man[1]  # Reflect change in hang structure
        print('\nYou\'ve run out of attempts! The word was: ' + word)
    print("\n".join(hang))