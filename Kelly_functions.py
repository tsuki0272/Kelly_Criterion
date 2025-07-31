import numpy as np
import math

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

def too_big(bankroll):
    return bankroll > (1.7e250)

def full_kelly( # mathematically optimal, bad in practice
        num_tries = default_num_tries, 
        bankroll = default_bankroll, 
        win_prob = default_win_prob, 
        win_odds = default_win_odds, 
        seed = default_seed): 
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