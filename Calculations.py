import numpy as np

def find_mean_bankroll_histories(top_fracs, strategy_keys, strategy_label) :
    """
    Computes the mean bankroll history for each strategy (e.g., probability or fraction).

    Inputs:
        top_fracs: List of lists of dicts, each containing 'bankroll history' and strategy info
        strategy_keys: List of strategy values (e.g., all probabilities or all fractions)
        strategy_label: String, either 'probability' or 'fraction', specifying which key to extract

    Output:
        bankrolls: Dict[strategy -> np.array], mapping each strategy value to the mean bankroll history
    """
    # mean = sum(x) / n
    bankrolls = { # create empty dictionary containing spaces for bankroll histories
        key: np.zeros(len(top_fracs[0][0]['bankroll history'])) 
        for key in strategy_keys
    }
    counts = {key: 0 for key in strategy_keys} # total number of elements
    
    for value in top_fracs:
        for dict in value: # add all values to prob_bankrolls
            key = dict[strategy_label]
            bankrolls[key] += dict['bankroll history']
            counts[key] += 1
    for key in strategy_keys:
        bankrolls[key] /= counts[key]
    return bankrolls

def find_max_within_range(start, stop, bankrolls, strategies):
    """
    Finds maximum bankroll value within a given index range across multiple strategies.

    Inputs:
        start: Integer, starting index (inclusive) of range
        stop: Integer, stopping index (exclusive) of range
        bankrolls: Dict[strategy -> list of bankroll values] by probability or fraction
        strategies: List of keys (floats or strings) corresponding to the strategies to consider

    Output:
        max_bankroll: Float, highest bankroll value observed within the specified range across all strategies
    """
    # finds the highest value of the bankroll history within a certain range
    max_bankroll = 0
    for strat in strategies:
        curr_max = max(bankrolls[strat][start:int(stop)])
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

def chi_squared_test(observed, predicted): # Computes the chi-squared test statistic comparing observed and expected frequencies.
    chi_squared = 0
    for i in range(len(observed)):
        obs = observed[i]
        pred = predicted[i]
        curr_var = ((obs - pred) ** 2) / pred
        chi_squared += curr_var
    return chi_squared