import numpy as np

def find_mean_bankroll_histories_for_prob(top_fracs, probabilities) :
    # mean = sum(x) / n
    prob_bankrolls = { # create empty dictionary containing spaces for bankroll histories
        prob: np.zeros(len(top_fracs[0][0]['bankroll history'])) 
        for prob in probabilities
    }
    counts = {prob: 0 for prob in probabilities} # total number of elements
    
    for value in top_fracs:
        for dict in value: # add all values to prob_bankrolls
            prob = dict['probability']
            prob_bankrolls[prob] += dict['bankroll history']
            counts[prob] += 1
    for prob in probabilities:
        prob_bankrolls[prob] /= counts[prob]
    return prob_bankrolls

def find_mean_bankroll_histories_for_frac(top_fracs, fractions) :
    # mean = sum(x) / n
    frac_bankrolls = { # create empty dictionary containing spaces for bankroll histories
        frac: np.zeros(len(top_fracs[0][0]['bankroll history'])) 
        for frac in fractions
    }
    counts = {frac: 0 for frac in fractions}
    counts

    for value in top_fracs:
            for dict in value: # add all values to prob_bankrolls
                frac = dict['fraction']
                frac_bankrolls[frac] += dict['bankroll history']
                counts[frac] += 1
    for frac in fractions:
        frac_bankrolls[frac] /= counts[frac]
    return frac_bankrolls

def find_max_within_range_for_prob(start, stop, prob_bankrolls, probabilities):
    # finds the highest value of the bankroll history within a certain range
    max_bankroll = 0
    for prob in probabilities:
        curr_max = max(prob_bankrolls[prob][start:int(stop)])
        if(curr_max > max_bankroll):
            max_bankroll = curr_max
    return max_bankroll

def find_max_within_range_for_frac(start, stop, frac_bankrolls, fractions):
    # finds the highest value of the bankroll history within a certain range
    max_bankroll = 0
    for frac in fractions:
        curr_max = max(frac_bankrolls[frac][start:int(stop)])
        if(curr_max > max_bankroll):
            max_bankroll = curr_max
    return max_bankroll

def get_frequency_stats(top_fracs):
    """
    Calculates mean, number of bins, and values from a dict containing frequencies
    
    Inputs: 
        top_fracs: dict with simulation results for one seed

    Outputs: List with 3 indexes
        [0] mean: average frequency of observations from dict, calculated by sum(x) / n
        [1] n: total number of bins in the dictionary
        [2] counts: list of values from top_fracs - useful for subscripting as dict.values() is not subscriptable
    """
    total = 0
    counts = []
    top_fracs_freq = top_fracs.values()
    n = len(top_fracs_freq)
    for count in top_fracs_freq:
        total += count
        counts.append(count)
    mean = total / n
    return mean, n, counts

def chi_squared_test(observed, predicted):
    chi_squared = 0
    for i in range(len(observed)):
        obs = observed[i]
        pred = predicted[i]
        curr_var = ((obs - pred) ** 2) / pred
        chi_squared += curr_var
    return chi_squared