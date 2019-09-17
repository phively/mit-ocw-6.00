# 6.00 Problem Set 4
#
# Caesar Cipher Skeleton
#
import string
import random

WORDLIST_FILENAME = "words.txt"

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)
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
    wordlist = line.split()
    print "  ", len(wordlist), "words loaded."
    return wordlist

wordlist = load_words()

def is_word(wordlist, word):
    """
    Determines if word is a valid word.

    wordlist: list of words in the dictionary.
    word: a possible word.
    returns True if word is in wordlist.

    Example:
    >>> is_word(wordlist, 'bat') returns
    True
    >>> is_word(wordlist, 'asdf') returns
    False
    """
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in wordlist

def random_word(wordlist):
    """
    Returns a random word.

    wordlist: list of words  
    returns: a word from wordlist at random
    """
    return random.choice(wordlist)

def random_string(wordlist, n):
    """
    Returns a string containing n random words from wordlist

    wordlist: list of words
    returns: a string of random words separated by spaces.
    """
    return " ".join([random_word(wordlist) for _ in range(n)])

def random_scrambled(wordlist, n):
    """
    Generates a test string by generating an n-word random string
    and encrypting it with a sequence of random shifts.

    wordlist: list of words
    n: number of random words to generate and scamble
    returns: a scrambled string of n random words


    NOTE:
    This function will ONLY work once you have completed your
    implementation of apply_shifts!
    """
    s = random_string(wordlist, n) + " "
    shifts = [(i, random.randint(0, 26)) for i in range(len(s)) if s[i-1] == ' ']
    return apply_shifts(s, shifts)[:-1]

def get_fable_string():
    """
    Returns a fable in encrypted text.
    """
    f = open("fable.txt", "r")
    fable = str(f.read())
    f.close()
    return fable


# (end of helper code)
# -----------------------------------

#
# Problem 1: Encryption
#
    
def shift_checker(shift, lower = -27, upper = 27, debug = False):
    """
    Ensures shift is in the valid range -27 < shift < 27.
    If not, set to 0.
    """
    if not isinstance(shift, int) or shift <= lower or shift >= upper:
        if debug:
            print('Invalid shift = ' + str(shift) + '; using 0 ')
        shift = 0
    return(shift)

def build_coder(shift):
    """
    Returns a dict that can apply a Caesar cipher to a letter.
    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation and numbers.

    shift: -27 < int < 27
    returns: dict

    Example:
    >>> build_coder(3)
    {' ': 'c', 'A': 'D', 'C': 'F', 'B': 'E', 'E': 'H', 'D': 'G', 'G': 'J',
    'F': 'I', 'I': 'L', 'H': 'K', 'K': 'N', 'J': 'M', 'M': 'P', 'L': 'O',
    'O': 'R', 'N': 'Q', 'Q': 'T', 'P': 'S', 'S': 'V', 'R': 'U', 'U': 'X',
    'T': 'W', 'W': 'Z', 'V': 'Y', 'Y': 'A', 'X': ' ', 'Z': 'B', 'a': 'd',
    'c': 'f', 'b': 'e', 'e': 'h', 'd': 'g', 'g': 'j', 'f': 'i', 'i': 'l',
    'h': 'k', 'k': 'n', 'j': 'm', 'm': 'p', 'l': 'o', 'o': 'r', 'n': 'q',
    'q': 't', 'p': 's', 's': 'v', 'r': 'u', 'u': 'x', 't': 'w', 'w': 'z',
    'v': 'y', 'y': 'a', 'x': ' ', 'z': 'b'}
    (The order of the key-value pairs may be different.)
    """
    shift = shift_checker(shift)
    # Make sure upper/lower case is preserved
    lower_keys = string.ascii_lowercase + ' '
    upper_keys = string.ascii_uppercase + ' '
    # Construct a dictionary
    coder = {}
    for i, letters in enumerate(upper_keys):
        # Add the keys in order, but the value is shifted
        coder.update({letters : (upper_keys + upper_keys)[i + shift]})
    for i, letters in enumerate(lower_keys):
        # Add the keys in order, but the value is shifted
        coder.update({letters : (lower_keys + lower_keys)[i + shift]})
    # Return result
    return(coder)
    
def build_encoder(shift):
    """
    Returns a dict that can be used to encode a plain text. For example, you
    could encrypt the plain text by calling the following commands
    >>>encoder = build_encoder(shift)
    >>>encrypted_text = apply_coder(plain_text, encoder)
    
    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation and numbers.

    shift: 0 <= int < 27
    returns: dict

    Example:
    >>> build_encoder(3)
    {' ': 'c', 'A': 'D', 'C': 'F', 'B': 'E', 'E': 'H', 'D': 'G', 'G': 'J',
    'F': 'I', 'I': 'L', 'H': 'K', 'K': 'N', 'J': 'M', 'M': 'P', 'L': 'O',
    'O': 'R', 'N': 'Q', 'Q': 'T', 'P': 'S', 'S': 'V', 'R': 'U', 'U': 'X',
    'T': 'W', 'W': 'Z', 'V': 'Y', 'Y': 'A', 'X': ' ', 'Z': 'B', 'a': 'd',
    'c': 'f', 'b': 'e', 'e': 'h', 'd': 'g', 'g': 'j', 'f': 'i', 'i': 'l',
    'h': 'k', 'k': 'n', 'j': 'm', 'm': 'p', 'l': 'o', 'o': 'r', 'n': 'q',
    'q': 't', 'p': 's', 's': 'v', 'r': 'u', 'u': 'x', 't': 'w', 'w': 'z',
    'v': 'y', 'y': 'a', 'x': ' ', 'z': 'b'}
    (The order of the key-value pairs may be different.)

    HINT : Use build_coder.
    """
    shift = shift_checker(shift, lower = 0)
    # Create the coder dictionary
    return(build_coder(shift))

def build_decoder(shift):
    """
    Returns a dict that can be used to decode an encrypted text. For example, you
    could decrypt an encrypted text by calling the following commands
    >>>encoder = build_encoder(shift)
    >>>encrypted_text = apply_coder(plain_text, encoder)
    >>>decrypted_text = apply_coder(plain_text, decoder)
    
    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation and numbers.

    shift: 0 <= int < 27
    returns: dict

    Example:
    >>> build_decoder(3)
    {' ': 'x', 'A': 'Y', 'C': ' ', 'B': 'Z', 'E': 'B', 'D': 'A', 'G': 'D',
    'F': 'C', 'I': 'F', 'H': 'E', 'K': 'H', 'J': 'G', 'M': 'J', 'L': 'I',
    'O': 'L', 'N': 'K', 'Q': 'N', 'P': 'M', 'S': 'P', 'R': 'O', 'U': 'R',
    'T': 'Q', 'W': 'T', 'V': 'S', 'Y': 'V', 'X': 'U', 'Z': 'W', 'a': 'y',
    'c': ' ', 'b': 'z', 'e': 'b', 'd': 'a', 'g': 'd', 'f': 'c', 'i': 'f',
    'h': 'e', 'k': 'h', 'j': 'g', 'm': 'j', 'l': 'i', 'o': 'l', 'n': 'k',
    'q': 'n', 'p': 'm', 's': 'p', 'r': 'o', 'u': 'r', 't': 'q', 'w': 't',
    'v': 's', 'y': 'v', 'x': 'u', 'z': 'w'}
    (The order of the key-value pairs may be different.)

    HINT : Use build_coder.
    """
    shift = shift_checker(shift, lower = 0)
    # Create the coder dictionary
    return(build_coder(-1 * shift))
 

def apply_coder(text, coder, debug = False):
    """
    Applies the coder to the text. Returns the encoded text.

    text: string
    coder: dict with mappings of characters to shifted characters
    returns: text after mapping coder chars to original text

    Example:
    >>> apply_coder("Hello, world!", build_encoder(3))
    'Khoor,czruog!'
    >>> apply_coder("Khoor,czruog!", build_decoder(3))
    'Hello, world!'
    """
    # Create an empty output string
    output = ''
    # Iterate through the text
    for letters in text:
        # Figure out the replacement, if any
        replacement = coder.get(letters)
        if debug:
            print('Looking up: ' + letters + ' : ' + str(replacement))
        if replacement == None:
            replacement = letters
        if debug:
            print('Current replacement for ' + letters + ' = ' + replacement)
        # Append the translated text to output
        output += replacement
        if debug:
            print('Current text: ' + output)
    # Return result
    return(output)

# For debugging
# apply_coder('abc ABC 123!', coder, True)

def apply_shift(text, shift):
    """
    Given a text, returns a new text Caesar shifted by the given shift
    offset. The empty space counts as the 27th letter of the alphabet,
    so spaces should be replaced by a lowercase letter as appropriate.
    Otherwise, lower case letters should remain lower case, upper case
    letters should remain upper case, and all other punctuation should
    stay as it is.
    
    text: string to apply the shift to
    shift: amount to shift the text
    returns: text after being shifted by specified amount.

    Example:
    >>> apply_shift('This is a test.', 8)
    'Apq hq hiham a.'
    """
    shift = shift_checker(shift)
    return(apply_coder(text, build_coder(shift)))
   
#
# Problem 2: Codebreaking.
#
def find_best_shift(wordlist, text, debug = False):
    """
    Decrypts the encoded text and returns the plaintext.

    text: string
    returns: 0 <= int 27

    Example:
    >>> s = apply_coder('Hello, world!', build_encoder(8))
    >>> s
    'Pmttw,hdwztl!'
    >>> find_best_shift(wordlist, s) returns
    8
    >>> apply_coder(s, build_decoder(8)) returns
    'Hello, world!'
    
    Pseudocode:
    For each shift_int from 0 to 27, inclusive:
        Shift the letters in the string by shift_int
        For each substring, from the beginning of the current string to the next space:
            Check for valid words, where a valid word is all characters from the start of current_string to the next space, or the last character
            Trim the current tested word from the front of this substring
        Save the count of valid words for this shift_int
    Return the integer shift_int producing the maximum count of valid words
    """
    # Store the results from our shifts
    shift_results = {}
    # Loop through the possible shifts (0 to 27)
    for shift in range(0, 27):
        # Decode the text with the current shift, and split it into words
        shift_text = apply_coder(text, build_decoder(int(shift)))
        candidate_words = string.split(shift_text,  sep = ' ', )
        # Count number of words and store result
        wordcount = 0
        for word in candidate_words:
            wordcount += is_word(wordlist, word)
        shift_results.update({shift : wordcount})
        # Debug output
        if debug:
            print('SHIFT = ' + str(shift))
            print('  Current text is: ' + shift_text)
            print('  There are ' + str(len(candidate_words)) + ' candidate words.')
            print('  There are ' + str(wordcount) + ' valid words.')
    # Debug output
    if debug:
        print('Final results: ')
        print(shift_results)
    # Return results
    return(max(shift_results, key = shift_results.get))
   
# find_best_shift(wordlist, 'hello there people who ArE reading This', debug = True)
# s = apply_coder('Hello, world!', build_encoder(8))
# find_best_shift(wordlist, s)
# apply_coder(s, build_decoder(8))
    
#
# Problem 3: Multi-level encryption.
#
def apply_shifts(text, shifts):
    """
    Applies a sequence of shifts to an input text.

    text: A string to apply the Ceasar shifts to 
    shifts: A list of tuples containing the location each shift should
    begin and the shift offset. Each tuple is of the form (location,
    shift) The shifts are layered: each one is applied from its
    starting position all the way through the end of the string.  
    returns: text after applying the shifts to the appropriate
    positions

    Example:
    >>> apply_shifts("Do Androids Dream of Electric Sheep?", [(0,6), (3, 18), (12, 16)])
    'JufYkaolfapxQdrnzmasmRyrpfdvpmEurrb?'
    """
    # Create a string to store the output
    # Its initial state is just the unencrypted text
    output = text
    # Iterate through the shifts
    for start, shift in shifts:
        # Keep up to start unchanged, then apply the shift to the piece after start
        output = output[:start] + apply_shift(output[start:], shift)
    # Return the final result
    return(output)

#
# Problem 4: Multi-level decryption.
#

def find_best_shifts(wordlist, text, debug = False):
    """
    Given a scrambled string, returns a shift key that will decode the text to
    words in wordlist, or None if there is no such key.

    Hint: Make use of the recursive function
    find_best_shifts_rec(wordlist, text, start)

    wordlist: list of words
    text: scambled text to try to find the words for
    returns: list of tuples.  each tuple is (position in text, amount of shift)
    
    Examples:
    >>> s = random_scrambled(wordlist, 3)
    >>> s
    'eqorqukvqtbmultiform wyy ion'
    >>> shifts = find_best_shifts(wordlist, s)
    >>> shifts
    [(0, 25), (11, 2), (21, 5)]
    >>> apply_shifts(s, shifts)
    'compositor multiform accents'
    >>> s = apply_shifts("Do Androids Dream of Electric Sheep?", [(0,6), (3, 18), (12, 16)])
    >>> s
    'JufYkaolfapxQdrnzmasmRyrpfdvpmEurrb?'
    >>> shifts = find_best_shifts(wordlist, s)
    >>> print apply_shifts(s, shifts)
    Do Androids Dream of Electric Sheep?
    """
    return(find_best_shifts_rec(wordlist, text, 0, debug))

def find_best_shifts_rec(wordlist, text, start, debug = False):
    """
    Given a scrambled string and a starting position from which
    to decode, returns a shift key that will decode the text to
    words in wordlist, or None if there is no such key.

    Hint: You will find this function much easier to implement
    if you use recursion.

    wordlist: list of words
    text: scambled text to try to find the words for
    start: where to start looking at shifts
    returns: list of tuples.  each tuple is (position in text, amount of shift)
    """
    # Debug output
    if debug:
        print('Current full text is: ' + text)
        print('Current scrambled text is: ' + text[start:])
    # Iterate through the possible shifts
    for shift in range(0, 27):
        # Generate a test string, the currently decoded prefix plus a shifted suffix
        prefix = text[:start]
        suffix = apply_shift(text[start:], shift)
        # Debug output
        if debug:
            print('  shift = ' + str(shift) + '; text = ' + prefix + suffix)
        # Check for a new word boundary, i.e. a space
        next_space = string.find(suffix, ' ')
        # If a space was found
        if next_space >= 0:
            # String up to space is a word
            if is_word(wordlist, suffix[:next_space]):
                # Recursively run algorithm on the next substring
                # Debug output
                if debug:
                    print('  Word found using ' + str((start, shift)))
                    print('    Calling recursively on ' + suffix)
                new_call = find_best_shifts_rec(wordlist, prefix + suffix, start + next_space + 1, debug)
                # Debug output
                if debug:
                    print('  New call output is ' + str(new_call) + ' ' + str(type(new_call)))
                # If new_call is a list of tuples, then great! We succeeded
                if new_call != None:
                    # Only save the (start, shift) when shift is nonzero
                    current_call = [(start, shift)]
                    if debug:
                        print('Current call output is ' + str([(start, shift)]))
                    if shift == 0:
                        if debug:
                            print('Shift is 0; skipping word')
                            return(new_call)
                    return(current_call + new_call)
            # Don't need an else condition; the else is just to continue looping
        # BASE CASE: no spaces found
        if next_space == -1:
            # Success: the rest of the string is a word
            if is_word(wordlist, suffix[:]):
                # Debug output
                if debug:
                    print('  SUCCESS! Returning ' + str((start, shift)))
                if shift == 0:
                    if debug:
                        print('  Last word is in plaintext, skipping')
                        return([])
                return([(start, shift)])
            # Failure: the rest of the string is not a word
            # Keep looping and try again with a different shift
    # Fallback: no valid shifts were found so return None
    return(None)

# find_best_shifts_rec(wordlist, apply_shifts('good deal', [(0, 3), (5, 20)]), 0, debug = True)
# find_best_shifts_rec(wordlist, apply_shifts('good deals all day today', [(0, 3), (5, 20), (15, 11)]), 0, debug = True)


def decrypt_fable(debug = False):
    """
    Using the methods you created in this problem set,
    decrypt the fable given by the function get_fable_string().
    Once you decrypt the message, be sure to include as a comment
    at the end of this problem set how the fable relates to your
    education at MIT.

    returns: string - fable in plain text
    """
    decryptors = find_best_shifts(wordlist, get_fable_string(), debug)
    text = apply_shifts(get_fable_string(), decryptors)
    return(text)


# 'An Ingenious Man who had built a flying machine invited a great concourse of
# people to see it go up. at the appointed moment, everything being ready, he
# boarded the car and turned on the power. the machine immediately broke
# through the massive substructure upon which it was builded, and sank out of
# sight into the earth, the aeronaut springing out a rely in time to save
# himself. "well," said he, "i have done enough to demonstrate the correctness
# of my details. the defects," he added, with a add hat the ruined brick work,
# "are merely a sic and fundamental." upon this assurance the people came
# ox ward with subscriptions to build a second machine'

# What is the moral of the story?
# 
# Beware of all hat no cattle types, I suppose. More seriously, without sound
# knowledge of fundamentals, it's a thin line between disaster and glory.
# 
# Also, don't rely on a brute force decoder to produce poetry, or even to get
# every word right. I enjoy some of the creative grammatical results
# (e.g. shouldn't it be "merely BASIC and fundamental").

