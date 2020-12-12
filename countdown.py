import random
import itertools
import msvcrt
import threading
import time
from os import system
import unittest

def select_characters():
    """Returns a string of selected characters from the lists of vowels
        and consonants depanding on the user input."""    
    #lists with probability weighting for each elements
    vowels = (['a'] * int((15/67)*100) + ['e'] * int((21/67)*100)
              + ['i'] * int((13/67)*100) + ['o'] * int((13/67)*100)
              + ['u'] * int((15/67)*100))

    consonants = (['b'] * int((15/67)*100) + ['c'] * int((15/67)*100)
                  + ['d'] * int((15/67)*100) + ['f'] * int((15/67)*100)
                  + ['g'] * int((15/67)*100) + ['h'] * int((15/67)*100)
                  + ['j'] * int((15/67)*100) + ['k'] * int((15/67)*100)
                  + ['l'] * int((15/67)*100) + ['m'] * int((15/67)*100)
                  + ['n'] * int((15/67)*100) + ['p'] * int((15/67)*100)
                  + ['q'] * int((15/67)*100) + ['r'] * int((15/67)*100)
                  + ['s'] * int((15/67)*100) + ['t'] * int((15/67)*100)
                  + ['v'] * int((15/67)*100) + ['w'] * int((15/67)*100)
                  + ['x'] * int((15/67)*100) + ['y'] * int((15/67)*100)
                  + ['z'] * int((15/67)*100))

    characters = ""
    for counter in range(9): #iterate 9 times
        #user input is converted to lower case
        user_input = (input("Enter 'v' for a vowel or 'c' for a "
                            + "consonant: ")).lower()
        #user input vaildation
        while (user_input != 'v' and user_input != 'c'):
            user_input = (input("Please enter 'v' for a vowel or 'c'"
                                + " for a consonant: ")).lower()
        #adding strings
        if (user_input == 'v'):
            characters += str(random.choice(vowels))
        else:
            characters += str(random.choice(consonants))
    return characters

def dictionary_reader(filename):
    """Returns a list strings.

    Parameters:
        filename (str):The name of the file, which is needed to be
                        read.

    Returns:
        dictionary (list):The list containing all the copied strings.

    """
    with open(filename, 'r') as dictionary_file:
        # initialize list
        dictionary_list = []
        # iterate over file contents
        for element in dictionary_file:
            # add element to list
            dictionary_list.append(element.strip().lower())
    return dictionary_list

def word_lookup(string):
    """Returns a list of longest words that exists in the dictionary.

    Parameters:
        string (str):The string of letters, where the words are
                        formed from.

    Returns:
        words (list):A list of all the longest words that exists in
                        the dictionary.
    
    """
    output_words = []
    word_length = len(string) #number of characters in the string
    #sortes the charaters in an alphabetical order
    temp_word = sorted(string)
    while (word_length > 0):
    #generating all possible combinations of words for every string size
        for word_combination in itertools.combinations(temp_word,
                                                       word_length):
            word = ''.join(word_combination)
            if word in DICTIONARY:
                output_words.append(word)
        word_length = word_length - 1
        if (len(output_words) != 0):
            #calling a different function to remove duplicates.
            output_words = remove_duplicates(output_words)
            return output_words

def remove_duplicates(array):
    """Returns a list without any duplicated elements.

    Parameter:
        array (list):A list with duplicated elements.

    Returns:
        final_array (list):A list without duplicated elements.

    """
    final_array = [] 
    for num in array: 
        if num not in final_array: 
            final_array.append(num) 
    return final_array

def get_score(user_input, characters):
    """Returns the Player's score.

    Parameter:
        user_input (str):A string storing Player's best guess.
        characters (str):A string of characters from the lists of
                            vowels and consonants.

    Returns:
        score (int):An integer value to represent player's score.
    """
    score = 0
    user_input_list = list(user_input)
    characters_list = list(characters)
    for index in user_input_list:
        if index not in characters_list: #cheaking if the charater exist
            print("Error: You have misspelled!")
            return score
        characters_list.remove(index)
    #cheacking if user_input exist in the DICTIONARY
    if user_input in DICTIONARY:
        score = len(user_input)
        return score
    print("Error: your word doesn't exist!")
    return score

MAX_TIME_LIMIT = 30
SHOW_TIMEOUT_SECOND = 1

USER_INPUT = ""

def show_screen(message, input_word, duration):
    """Displays a user message, inputting characters and remaining time.

    Parameter:
        message (str):a message to inform the user.
        input_word (str):currently typed letters.
        duration (float):remaining time.
    """
    system('cls')
    print("Remaining time: ", MAX_TIME_LIMIT - duration)
    print(message, input_word)

def user_input_data(user_message):
    """Gets user inputs and reacts depending on which key they enter.

    Parameter:
        user_message (str):a message to inform the user.
    """
    global USER_INPUT

    system('cls')
    show_screen(user_message, USER_INPUT, 0)
    start_time = time.time()
    count = 1
    duration = 0

    while True:
        time.sleep(0.05)
    #user input is being limited as only some characters are recognized.
        if msvcrt.kbhit():
            key = ord(msvcrt.getch())
            if key == 13: #enter key
                break
            elif key == 8:
                USER_INPUT = USER_INPUT[:-1] #backspace key
            elif 97 <= key <= 122 or 65 <= key <= 90:  #a-z or A-Z keys
                USER_INPUT = USER_INPUT + chr(key)
                show_screen(user_message, USER_INPUT, duration)

        duration = round(time.time() - start_time, 0)
        if duration >= MAX_TIME_LIMIT:
            return ""
        elif duration >= count * SHOW_TIMEOUT_SECOND:
            count += 1
            show_screen(user_message, USER_INPUT, duration)

def run_timer():
    msg = "Randomly Generated letters are: " + CHARACTERS + "."
    msg += " Enter your best guess at the longest word: "
    thread = threading.Thread(target=user_input_data(msg))
    thread.setDaemon(True)
    thread.start()
    thread.join()

    if not USER_INPUT.strip():
        print("Sorry, Times up!!! or You haven’t entered anything.")
        return ""
    else:
        return USER_INPUT

    #Call your function here by passing 'USER_INPUT'
    USER_INPUT

class TestFunctions(unittest.TestCase):

    def test_select_characters(self): #testing select_characters() function
        self.assertEqual(len(CHARACTERS), 9)
        self.assertTrue(CHARACTERS.isalpha()) #is the string only alpha values
        self.assertTrue(CHARACTERS.lower()) #is the string lower case

    def test_dictionary_reader(self):
        self.assertEqual(len(DICTIONARY), len(open("words.txt")
                                              .readlines())) #is size equal
        
    def test_word_lookup(self):
        for element in LONGEST_WORDS:
            #does the LONGEST_WORDS exists in the DICTIONARY
            self.assertIn(element, DICTIONARY)
            element_list = list(element)
            characters_list = list(CHARACTERS)
            for index in element_list:
                #does the LONGEST_WORDS exists in the CHARACTERS
                self.assertIn(index, characters_list)


if __name__ == "__main__":
    print('''
################################################################################
        888       888          888                                         
        888   o   888          888                                         
        888  d8b  888          888                                         
        888 d888b 888  .d88b.  888  .d8888b .d88b.  88888b.d88b.   .d88b.  
        888d88888b888 d8P  Y8b 888 d88P"   d88""88b 888 "888 "88b d8P  Y8b 
        88888P Y88888 88888888 888 888     888  888 888  888  888 88888888 
        8888P   Y8888 Y8b.     888 Y88b.   Y88..88P 888  888  888 Y8b.     
        888P     Y888  "Y8888  888  "Y8888P "Y88P"  888  888  888  "Y8888  

                                      _   _  
                                     / \ / \ 
                                    ( t | o )
                                     \_/ \_/ 
                                      
             _____                   _      _                     
            /  __ \                 | |    | |                    
            | /  \/ ___  _   _ _ __ | |_ __| | _____      ___ __  
            | |    / _ \| | | | '_ \| __/ _` |/ _ \ \ /\ / / '_ \ 
            | \__/\ (_) | |_| | | | | || (_| | (_) \ V  V /| | | |
             \____/\___/ \__,_|_| |_|\__\__,_|\___/ \_/\_/ |_| |_|                                                                                                             
################################################################################
''') #Ascii Art

    CHARACTERS = select_characters()
    INPUT_WORD = run_timer().lower()
    DICTIONARY = dictionary_reader("words.txt")
    SCORE = get_score(INPUT_WORD, CHARACTERS)
    LONGEST_WORDS = word_lookup(CHARACTERS)
    print("The longest possible words are: ", LONGEST_WORDS)
    print("You have scored ", SCORE, " point(s)!!!")
    print()
    unittest.main()
