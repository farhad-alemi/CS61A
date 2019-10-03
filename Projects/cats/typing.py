"""Typing test implementation"""

from utils import *
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    # BEGIN PROBLEM 1
    if k >= len(paragraphs):
        return ''
    counter = 0
    for i in range(len(paragraphs)):
        if select(paragraphs[i]):
            if counter == k:
                return paragraphs[i]
            else:
                counter += 1
    return ''
    # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    def select(paragraph):
        list_paragraph = split(lower(remove_punctuation(paragraph)))
        for i in range(len(topic)):
            if topic[i] in list_paragraph:
                return True
        return False
    return select
    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    if len(typed_words) == 0:
        return 0.0
    
    correct_count = 0
    
    for i in range (min(len(typed_words), len(reference_words))):
        if typed_words[i] == reference_words[i]:
            correct_count += 1
    return correct_count / len(typed_words) * 100.0
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    return (len(typed) / 5) / (elapsed / 60)
    # END PROBLEM 4


def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than LIMIT.
    """
    # BEGIN PROBLEM 5
    if user_word in valid_words:
        return user_word
    else:
        min_diff = 100         # initialization to a higher value for min to function

        for i in range (len(valid_words)):
            temp = diff_function(user_word, valid_words[i], limit)
            if (temp < min_diff):
                min_diff = temp
                min_i = i

        if min_diff <= limit:
            return valid_words[min_i]
        else:
            return user_word
            
    # END PROBLEM 5


def swap_diff(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # BEGIN PROBLEM 6
    len_diff = abs(len(start) - len(goal))
    if len_diff > limit:
        return limit + 100
    
    def helper(index, num_corrections):
        if num_corrections > limit:
            return limit + 100
        elif index >= min(len(goal), len(start)):
            return num_corrections
        elif start[index] == goal[index]:
            return helper(index + 1, num_corrections)
        else:
            return helper(index + 1, num_corrections + 1)
        
    return helper (0, len_diff)
    # END PROBLEM 6

def edit_diff(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL."""
    """len_diff = abs(len(start) - len(goal))
    if len_diff > limit:
        return limit + 100"""
    if start == goal:
        return 0
    elif limit <= 0:
        return 100      # A large value to indicate the case is over-the-limit
    elif len(start) == 0 or len(goal) == 0:
        return abs(len(start) - len(goal))
    # The following case is not required but will make the code run faster
    elif start[0] == goal[0]:
        return edit_diff(start[1:], goal[1:], limit)
    else:
        add_diff = 1+ edit_diff(goal[0] + start, goal, limit - 1)
        remove_diff = 1 + edit_diff(start[1:], goal, limit - 1) 
        substitute_diff = 1 + edit_diff(goal[0] + start[1:], goal, limit - 1)

    return min(add_diff, remove_diff, substitute_diff)


def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function'




###########
# Phase 3 #
###########


def report_progress(typed, prompt, id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    count_correct = 0
    percent_correct = 0
    for i in range(min(len(typed), len(prompt))):
        if typed[i] != prompt[i]:
            break
        count_correct += 1

    percent_correct = count_correct / len(prompt)
    send({'id': id, 'progress': percent_correct})
    return percent_correct
    # END PROBLEM 8


def fastest_words_report(word_times):
    """Return a text description of the fastest words typed by each player."""
    fastest = fastest_words(word_times)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def fastest_words(word_times, margin=1e-5):
    """A list of which words each player typed fastest."""
    n_players = len(word_times)
    n_words = len(word_times[0]) - 1
    assert all(len(times) == n_words + 1 for times in word_times)
    assert margin > 0
    # BEGIN PROBLEM 9
    def time_spent_typing_word(lst, word_num):
        return elapsed_time(lst[word_num]) - elapsed_time(lst[word_num - 1])

    def fastest_time_for_word(i):
        min_time = 1000         # initialization to a higher value for min to work
        for n in range(n_players):
            temp = time_spent_typing_word(word_times[n], i)
            if (temp < min_time):
                min_time = temp
        return min_time

    processed = []
    for n in range(n_players):
        processed += [[]]
        
    for i in range(1, n_words + 1):
        for n in range(n_players):
            if (time_spent_typing_word(word_times[n], i) - fastest_time_for_word(i)) <= margin:
                processed[n] += [word(word_times[n][i])]
    return processed            
    # END PROBLEM 9


def word_time(word, elapsed_time):
    """A data abstrction for the elapsed time that a player finished a word."""
    return [word, elapsed_time]


def word(word_time):
    """An accessor function for the word of a word_time."""
    return word_time[0]


def elapsed_time(word_time):
    """An accessor function for the elapsed time of a word_time."""
    return word_time[1]


enable_multiplayer = True  # Change to True when you


##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)
