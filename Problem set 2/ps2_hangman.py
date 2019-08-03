# 6.00 Problem Set 3
# 
# Hangman
#
# Paul Hively
# Time spent: 15 mins on helper functions


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

# your code begins here!

# Helper function to print the not yet guessed letters
def get_remaining_letters(guessed_letters, debug = False):
    # Lower-case alphabet
    letters_out = string.ascii_lowercase
    # Delete any guessed letters using string.replace
    for letters in guessed_letters:
        letters_out = string.replace(letters_out, letters, '')
    # Debug output
    if debug:
        print "   (debug) guessed letters: " + str(guessed_letters)
        print "   (debug) remaining letters: " + letters_out
    return letters_out

# Helper function to display the word so far based on letters guessed
def display_word(remaining_letters, answer, debug = False):
    hint_out = answer
    # Replace each letter not yet guessed with " _"
    for letters in remaining_letters:
        hint_out = string.replace(hint_out, letters, " _")
    # Debug output
    if debug:
        print "   (debug) " + answer + " -> " + hint_out
    return hint_out

# Main function
def hangman(guesses = 2, debug = False):
    """
    Launches an interactive game of hangman.
    
    guesses (int): additional number of guesses (beyond the word length)
      allowed before the game ends
    debug (bool): when True, print debug output
    """
    ### Initialize the game's starting state
    # Load the wordlist
    wordlist = load_words()
    # Choose a random word from wordlist
    answer = choose_word(wordlist)
    if debug:
        print "  (debug) the answer is: " + answer
    # Create a tuple of guessed letters to keep track of
    guessed_letters = ( )
    remaining_letters = get_remaining_letters(guessed_letters, debug)
    # Create blank spaces for the word to be guessed
    hint = display_word(answer, guessed_letters, debug)
    
    # Welcome message
    
    # Main loop - while guesses remain, alternate between guess and check
        # Print # of guesses and available letters
        # Ask for a guess
        # Check if the word was revealed
        # Check if chose an already guessed letter
        # Check if guessed a new letter in the word
        # Else letter is not in the word
        
    # End of game
    # Congrats or you lost message
    