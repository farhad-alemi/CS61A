"""
Only this file will be submitted. Make sure to include any helper functions
from `hog.py` that you'll need here! For example, if you have a function to
calculate Free Bacon points, you should make sure it's added to this file
as well.

Don't forget: your strategy must be deterministic and pure.
"""

PLAYER_NAME = 'ERROR'

import functools

@functools.lru_cache(maxsize=None)
def is_swap(player_score, opponent_score):
    """
    Return whether the two scores should be swapped
    """
    def left_digit(score):            
        while score:
            if score // 10 == 0:
                return score
            else:
                score //= 10
        return score

    return (((player_score % 10) * left_digit(player_score))
            == ((opponent_score % 10) * left_digit(opponent_score)))
#@memoize
def free_bacon(score):
    """Return the points scored from rolling 0 dice (Free Bacon).

    score:  The opponent's current score.
    """
    assert score < 100, 'The game should be over.'
    if score < 10:
        return 10
    return (10 - min(score % 10, score // 10))

#@memoize
def bacon_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice if that gives at least MARGIN points, and
    rolls NUM_ROLLS otherwise.
    """
    if free_bacon(opponent_score) >= margin:
        return 0
    else:
        return num_rolls

#@memoize
def swap_strategy(score, opponent_score, margin=8, num_rolls=-1):
    """This strategy rolls 0 dice when it triggers a beneficial swap. It also
    rolls 0 dice if it gives at least MARGIN points and does not trigger a
    non-beneficial swap. Otherwise, it rolls NUM_ROLLS.
    """
    possible_gain = free_bacon(opponent_score)
    prospective_score = score + possible_gain
    can_swap = is_swap(prospective_score, opponent_score)
    
    if can_swap and prospective_score < opponent_score:
        return 0
    elif possible_gain >= margin:
        if can_swap and prospective_score > opponent_score:
            return num_rolls
        else:
            return 0
    else:
        return num_rolls

def six_sided(outcome):
    if 1 <= outcome <= 6:
        return 1/6
    else:
        return 0

dice = six_sided

#@memoize
def roll_a_one(n):
    """The probability of rolling a 1 from N dice.

    >>> [round(roll_a_one(n), 3) for n in range(1, 10)]
    [0.167, 0.306, 0.421, 0.518, 0.598, 0.665, 0.721, 0.767, 0.806]
    """
    if n == 0:
        return 0
    return dice(1) + (1 - dice(1)) * roll_a_one(n-1)

#@memoize
def roll_no_ones(total, n):
    """The probability of scoring total from N dice, assuming no ones.
    
    >>> [round(roll_no_ones(t, 2), 3) for t in range(1, 13)]
    [0.0, 0.0, 0.0, 0.028, 0.056, 0.083, 0.111, 0.139, 0.111, 0.083, 0.056, 0.028]
    """
    if total == 0 and n == 0:
        return 1
    elif n == 0:
        return 0
    else:
        chance, outcome = 0, 2
        while outcome <= 6:
            chance += dice(outcome) * roll_no_ones(total-outcome, n-1)
            outcome += 1
        return chance

#@memoize
def roll_dice(total, n):
    """The probability of scoring total from N dice, observing pig out.

    >>> [round(roll_dice(t, 2), 3) for t in range(1, 13)]
    [0.306, 0.0, 0.0, 0.028, 0.056, 0.083, 0.111, 0.139, 0.111, 0.083, 0.056, 0.028]
    """
    if total == 1:
        return roll_a_one(n)
    else:
        return roll_no_ones(total, n)
    
#@memoize
def roll_at_least(k, n):
    """Return the chance of scoring at least K points by rolling N dice
    without rolling a 1.

    >>> round((5/6) ** 4, 10)
    0.4822530864
    >>> round(roll_at_least(8, 4), 10)
    0.4822530864
    >>> round(roll_at_least(4, 4), 10)
    0.4822530864
    >>> round(roll_at_least(20, 4), 10)
    0.0540123457
    >>> round(roll_at_least(20, 6), 10)
    0.3017189643
    >>> round(roll_at_least(8, 2), 10)
    0.4166666667
    """
    total, chance = k, 0
    while total <= 6 * n:
        chance += roll_dice(total, n)
        total += 1
    return chance

#@memoize
def final_strategy(score, opponent_score):
    num_rolls = swap_strategy(score, opponent_score, 100 - score)

    """if num_rolls == -1:"""
        
    return num_rolls
