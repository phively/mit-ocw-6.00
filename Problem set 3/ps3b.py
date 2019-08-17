from ps3a import *
import time
from perm import *


#
#
# Problem #6A: Computer chooses a word
#
#
def comp_choose_word(hand, word_list, start_size = HAND_SIZE, debug = False):
    """
	Given a hand and a word_dict, find the word that gives the maximum value score, and return it.
   	This word should be calculated by considering all possible permutations of lengths 1 to HAND_SIZE.

    hand: dictionary (string -> int)
    word_list: list (string)
    start_size: starting hand length to try
    debug: if True, print debug output
    """
    # Variables for use
    len_to_try = min(calculate_handlen(hand), start_size)
    best_word = '.' # Fallback is to stop looking for words
    found_word = False
    
    # Loop till a valid word is discovered
    while found_word == False and len_to_try > 0:
        
        # debug output
        if debug:
            print('  DEBUG: best word so far is ' + best_word)
            print('  DEBUG: current length is ' + str(len_to_try))
        
        # Populate guesses
        guesses = get_perms(hand, len_to_try)
        
        # Check for word
        for guess in guesses:
            found_word = is_valid_word(guess, hand, word_list)
            
            # debug output
            if debug:
                print('  DEBUG: current guess is ' + guess)
            # Break if a valid word was discovered
            if found_word == True:
                best_word = guess
                break
        if found_word == True:
            break
        # Otherwise try again with a shorter hand length
        len_to_try = len_to_try - 1
    
    # Return the found word
    return(best_word)


#
# Problem #6B: Computer plays a hand
#
def comp_play_hand(hand, word_list):
    """
     Allows the computer to play the given hand, as follows:

     * The hand is displayed.

     * The computer chooses a word using comp_choose_words(hand, word_dict).

     * After every valid word: the score for that word is displayed, 
       the remaining letters in the hand are displayed, and the computer 
       chooses another word.

     * The sum of the word scores is displayed when the hand finishes.

     * The hand finishes when the computer has exhausted its possible choices (i.e. comp_play_hand returns None).

     hand: dictionary (string -> int)
     word_list: list (string)
    """
    # Variables
    points = 0
    last_len = HAND_SIZE # For efficiency I want to keep track of the length of
      # the previously found word as there's no point looking again for a longer one
    
    # Main loop
    while calculate_handlen(hand) > 0:
        # Take computer input
        print('Current hand: ')
        display_hand(hand)
        print('')
        print('Enter word, or a "." to indicate that you are finished: ')
        # Return computer attempt
        attempt = comp_choose_word(hand, word_list, start_size = last_len)
        print(attempt)
        # Check input
        if attempt == '.':
            print('Total score: ' + str(points))
            break
        elif is_valid_word(attempt, hand, word_list) == False:
            print('Invalid word, please try again.')
        else:
            # Update hand
            hand = update_hand(hand, attempt)
            last_len = len(attempt)
            # Score word
            value = get_word_score(attempt, n = HAND_SIZE)
            points += value
            # Output
            print('"' + attempt + '" earned ' + str(value) + " points. " + \
                  "Total: " + str(points) + ' points')
            print('')
    
#
# Problem #6C: Playing a game
#
#
def play_game(word_list):
    """Allow the user to play an arbitrary number of hands.

    1) Asks the user to input 'n' or 'r' or 'e'.
    * If the user inputs 'n', play a new (random) hand.
    * If the user inputs 'r', play the last hand again.
    * If the user inputs 'e', exit the game.
    * If the user inputs anything else, ask them again.

    2) Ask the user to input a 'u' or a 'c'.
    * If the user inputs 'u', let the user play the game as before using play_hand.
    * If the user inputs 'c', let the computer play the game using comp_play_hand (created above).
    * If the user inputs anything else, ask them again.

    3) After the computer or user has played the hand, repeat from step 1

    word_list: list (string)
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
        else:
            if user_select == 'n' or hand == None:
                print('Dealing a new hand...')
                hand = deal_hand(n = HAND_SIZE)
            elif user_select == 'r':
                print('Replaying previous hand...')
            player_type = ''
            while player_type not in ('c', 'u'):
                player_type = \
                raw_input('Please enter "u" to play as yourself, or "c" ' + \
                          'to let the computer play the round. ')
            # Start game
            if player_type == 'u':
                print('Good luck!')
                print('')
                play_hand(hand, word_list)            
            else:
                print('Okay, wish me luck!')
                print('')
                comp_play_hand(hand, word_list)
        
#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)

    
