import numpy as np

# Default variables
default_num_tries = 10
default_bankroll = 10
default_win_prob = 0.55
default_win_odds = 1.5
default_fraction = 0.5 
default_seed = 42
default_prior_wins = 1
default_prior_losses = 1
default_estimated_win_prob = 0.5

def too_big(bankroll): # Checks if a bankroll value exceeds an upper bound that may cause numerical overflow.
    return bankroll > (1.7e250)

def full_kelly( # mathematically optimal, bad in practice
        num_tries = default_num_tries, 
        bankroll = default_bankroll, 
        win_prob = default_win_prob, 
        win_odds = default_win_odds, 
        seed = default_seed): 
    """
    Simulates bets using the full Kelly Criterion strategy over a fixed number of trials.

    Inputs:
        num_tries: Integer, total number of bets to simulate
        bankroll: Float, starting bankroll
        win_prob: Float between 0 and 1, true win probability of a single bet
        win_odds: Float, payout multiplier on a winning bet
        seed: Integer, seed for NumPy's random number generator to ensure reproducibility

    Output:
        values: numpy array of bankroll values after each bet, length equal to num_tries
        If bankroll exceeds too_big() limit, simulation halts and remaining values repeat the last valid value
        This is done to prevent issues when calculating mean bankroll in Calculations.py
    """
    np.random.seed(seed)

    values = []
    total_money_lost = 0
    val_too_big = 0
    kelly_frac = (((win_odds * win_prob) - (1 - win_prob)) / win_odds) # Kelly Criterion
    rand = np.random.random(num_tries) # simulate random numbers from 0 to 1 - used for betting results
    rand_index = 0

    for x in range(num_tries):
        if bankroll > 0:
            amount_to_bet = kelly_frac * bankroll
            if too_big(bankroll):
                print(f'Number too big: {bankroll}. Stopping bets')
                val_too_big = values[len(values) - 1]
                break
            if amount_to_bet > 0:
                if rand[rand_index] < win_prob:
                    bankroll += amount_to_bet
                else:
                    bankroll -= amount_to_bet
                    total_money_lost += amount_to_bet
                values.append(bankroll)
                rand_index += 1
            else:
                print('No edge. Will not bet.')
                break
        else:
            print(f'Bankrupt after {x} rounds')
            break
    while len(values) < num_tries:
        values.append(val_too_big)
    values = np.asarray(values)
    return values

def fractional_kelly( # used as benchmark due to superior survivability and growth consistency
        num_tries = default_num_tries, 
        bankroll = default_bankroll, 
        win_prob = default_win_prob, 
        win_odds = default_win_odds, 
        fraction = default_fraction, 
        seed = default_seed): 
    """
    Simulates betting using a fractional Kelly Criterion strategy, which mitigates volatility at the cost of slower growth.

    Inputs:
        num_tries: Integer, total number of bets to simulate
        bankroll: Float, starting bankroll
        win_prob: Float between 0 and 1, true win probability of a single bet
        win_odds: Float, payout multiplier on a winning bet
        fraction: Float between 0 and 1, fraction of the full Kelly bet to bet each round
        seed: Integer, seed for NumPy's random number generator to ensure reproducibility

    Output:
        values: numpy array of bankroll values after each bet, length equal to num_tries
        If bankroll exceeds too_big() limit, simulation halts and remaining values repeat the last valid value
        This is done to prevent issues when calculating mean bankroll in Calculations.py
    """
    np.random.seed(seed)

    values = []
    total_money_lost = 0
    val_too_big = 0
    kelly_frac = (((win_odds * win_prob) - (1 - win_prob)) / win_odds) * fraction
    rand = np.random.random(num_tries)
    rand_index = 0

    for x in range(num_tries):
        if bankroll > 0:
            amount_to_bet = kelly_frac * bankroll
            if too_big(bankroll):
                # print(f'Number too big: {bankroll}. Stopping bets')
                val_too_big = values[len(values) - 1]
                break
            if amount_to_bet > 0:
                if rand[rand_index] < win_prob:
                    bankroll += amount_to_bet
                else:
                    bankroll -= amount_to_bet
                    total_money_lost += amount_to_bet
                values.append(bankroll)
                rand_index += 1
            else:
                print('No edge. Will not bet.')
                break
        else:
            print(f'Bankrupt after {x} rounds')
            break
    while len(values) < num_tries:
        values.append(val_too_big)
    values = np.asarray(values)
    return values