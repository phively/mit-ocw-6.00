# 6.00 Problem Set 3
# 
# Hangman
#
# Paul Hively
# Time spent: call it two hours? About 30 minutes creating and reworking the
#   helper functions plus something like 1:15 programming the rest and playing
#   with the results.

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)
import random
import string

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = string.split(line)
    print "  ", len(wordlist), "words loaded."
    return wordlist

def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code
# -----------------------------------

# Load the wordlist
wordlist = load_words()
    
# your code begins here!

# Helper variables
debug_print = "   (debug) "

# Helper function to print the not yet guessed letters
def get_remaining_letters(guessed_letters, debug = False):
    # Lower-case alphabet
    letters_out = string.ascii_lowercase
    # Delete any guessed letters using string.replace
    for letters in guessed_letters:
        letters_out = string.replace(letters_out, letters, '')
    # Debug output
    if debug:
        print debug_print + "guessed letters: " + str(guessed_letters)
        print debug_print + "remaining letters: " + letters_out
    return letters_out

# Helper function to display the word so far based on letters guessed
def display_word(answer, remaining_letters, debug = False):
    hint_out = answer
    # Replace each letter not yet guessed with " _"
    for letters in remaining_letters:
        if debug:
            print "Letter " + letters + " ; " + str(type(letters))
        hint_out = string.replace(hint_out, letters, " _")
    # Debug output
    if debug:
        print debug_print + answer + " -> " + hint_out
    return hint_out

# Main function
def hangman(max_guesses = 8, debug = False):
    """
    Launches an interactive game of hangman.
    
    guesses (int): minimum number of guesses allowed before the game ends
    debug (bool): when True, print debug output
    """
    # Helper variables
    separator = "-------------------------------------------------"

    ### Initialize the game's starting state
    
    # Choose a random word from wordlist
    answer = choose_word(wordlist)
    guesses = max_guesses
    if debug:
        print debug_print + "the answer is: " + answer
        print debug_print + str(guesses) + " guesses allowed"
    # Create a string of guessed letters to keep track of
    guessed_letters = ""
    remaining_letters = get_remaining_letters(guessed_letters, debug)
    # Create blank spaces for the word to be guessed
    hint = display_word(answer, remaining_letters, debug)
    
    # Welcome message
    print separator
    print "Welcome to Hangman!"
    print ("I'm thinking of a word that is " + 
           str(len(answer)) + " letters long.")
    
    ### Main loop - while guesses remain, alternate between guess and check
    while guesses > 0:
        # Print # of guesses and available letters
        print separator
        print "My word: " + hint
        print "You have " + str(guesses) + " guesses left."
        print "Available letters: " + remaining_letters
        
        # Ask for a guess
        guess = string.lower(raw_input("Please guess a letter: "))
        
        if debug:
            print debug_print + "current guess = " + guess
            print debug_print + "previously guessed = " + guessed_letters
        
        ### Error checking
        # Check that input is valid
        if string.find(string.lowercase, guess) == -1:
            print guess + " is not a valid letter! Please try again."
            continue
        # Check if chose an already guessed letter
        elif string.find(guessed_letters, guess) != -1:
            print guess + " was already guessed! Please try again."
            continue
        
        ### Update variables
        guessed_letters += guess
        remaining_letters = get_remaining_letters(guessed_letters, debug)
        hint = display_word(answer, remaining_letters, debug) 
        
        ### Guess checking
        # Break if the word was revealed
        if string.find(hint, "_") == -1:
            print separator
            print "Congratulations! My word was: " + answer
            print "You won using " + str(max_guesses - guesses) + " guesses."
            break
        
        # Check if guessed a new letter in the word
        if string.find(answer, guess) != -1:
            print "Good guess!"
            # Don't decrement remaining guesses if you found a letter
        # Else letter is not in the word
        else:
            guesses -= 1 # Decrement remaining guesses
            print "Oops, " + guess + " is not in the word."
            # Out of guesses: you lose!
            if guesses == 0:
                print "Out of guesses! My word was: " + answer
                print "Let's play again soon."
