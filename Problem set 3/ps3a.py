# 6.00 Problem Set 3A Solutions
#
# The 6.00 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#

import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

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
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print "  ", len(wordlist), "words loaded."
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

	The score for a word is the sum of the points for letters
	in the word multiplied by the length of the word, plus 50
	points if all n letters are used on the first go.

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string (lowercase letters)
    returns: int >= 0
    """
    # Temporary variables
    score = 0
    wlen = len(word)
    len_bonus = 50 * (wlen == n)
    
    # Iterate through word
    for letter in word:
        score += SCRABBLE_LETTER_VALUES.get(letter)
    
    return(score * wlen + len_bonus)
    
#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    for letter in hand.keys():
        for j in range(hand[letter]):
             print letter,              # print all on the same line
    print                               # print an empty line

#
# Make sure you understand how this function works and what it does!
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    At least n/3 the letters in the hand should be VOWELS.

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    hand={}
    num_vowels = n / 3
    
    for i in range(num_vowels):
        x = VOWELS[random.randrange(0,len(VOWELS))]
        hand[x] = hand.get(x, 0) + 1
        
    for i in range(num_vowels, n):    
        x = CONSONANTS[random.randrange(0,len(CONSONANTS))]
        hand[x] = hand.get(x, 0) + 1
        
    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Assumes that 'hand' has all the letters in word.
	In other words, this assumes that however many times
	a letter appears in 'word', 'hand' has at least as
	many of that letter in it. 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    # Copy hand
    newhand = hand.copy()
    
    # Iterate through the word
    for letter in word:
        # Updated letter count
        newcount = newhand.get(letter) - 1
        # Remove one copy of the current letter from hand
        newhand.update({letter: newcount})
    
    return(newhand)

#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
    
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    """
    # Check whether the word is in word_list
    in_list = word in word_list
    # Check whether the word can be constructed from the hand
    valid = True
    # Check whether there are enough letters for the word
    try:
        # Must not have decremented the letter count past 0
        valid = min(update_hand(hand, word).values()) >= 0 
    # Fallback for missing letters
    except TypeError:
        valid = False
    # Return True when both conditions are true
    return(in_list & valid)

def calculate_handlen(hand):
    handlen = 0
    for v in hand.values():
        handlen += v
    return handlen

#
# Problem #4: Playing a hand
#
def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    1) The hand is displayed.
    
    2) The user may input a word.

    3) An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    4) When a valid word is entered, it uses up letters from the hand.

    5) After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    6) The sum of the word scores is displayed when the hand finishes.

    7) The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing a single
      period (the string '.') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      
    """
    # Variables to store
    points = 0
    
    # Main loop
    while calculate_handlen(hand) > 0:
        # Take user input
        print('Current hand: ')
        display_hand(hand)
        attempt = raw_input('Enter word, or a "." to indicate that you are finished: ')
        # Check input
        if attempt == '.':
            print('Total score: ' + str(points))
            break
        elif is_valid_word(attempt, hand, word_list) == False:
            print('Invalid word, please try again.')
        else:
            # Update hand
            hand = update_hand(hand, attempt)
            # Score word
            value = get_word_score(attempt, n = HAND_SIZE)
            points += value
            # Output
            print('"' + attempt + '" earned ' + str(value) + " points. " + \
                  "Total: " + str(points) + ' points')
            print('')

#
# Problem #5: Playing a game
# Make sure you understand how this code works!
# 
def play_game(word_list):
    """
    Allow the user to play an arbitrary number of hands.

    1) Asks the user to input 'n' or 'r' or 'e'.

    * If the user inputs 'n', let the user play a new (random) hand.
      When done playing the hand, ask the 'n' or 'e' question again.

    * If the user inputs 'r', let the user play the last hand again.

    * If the user inputs 'e', exit the game.

    * If the user inputs anything else, ask them again.
    """
    # Initial hand is empty
    hand = None
    # Loop until exiting
    while True:
        # Ask for input
        user_select = ''
        while user_select not in ('n', 'r', 'e'):
            user_select = \
            raw_input('Please enter "n" to play a new hand, "r" to ' + \
                      'replay the last hand, or "e" to exit the game. ')
        # Parse input
        if user_select == 'e':
            print('Thanks for playing!')
            break
        elif user_select == 'n' or hand == None:
            print('Dealing a new hand...')
            hand = deal_hand(n = HAND_SIZE)
            play_hand(hand, word_list)
        elif user_select == 'r':
            print('Replaying previous hand...')
            play_hand(hand, word_list)

#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)