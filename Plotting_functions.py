from matplotlib import pyplot as plt
import numpy as np
import math

def create_bankroll_history_plot(title = '', prob = 0, rows = 1, columns = 1, plot_num = 1, line = None):
    """
    Sets up a single subplot for visualizing bankroll history in a multi-plot figure layout.

    Inputs:
        title: String, title of current subplot. If `prob` is provided and non-zero, 
            this will be overridden to include the probability value
        prob: Float (optional), if non-zero, sets a title indicating win probability
        rows, columns: Integer, # of rows and columns in plotting grid
        plot_num: Integer, current index of plot within plotting grid
        line: Float (optional), Y-axis value at which a line is drawn

    Output:
        None. Configures and formats the current subplot
    """
    plt.subplot(rows, columns, plot_num)
    plt.title(title)
    if(prob != 0):
        plt.title(f'Bankroll History (prob = {prob:.3f})')
    plt.xlabel('Num. of Bets')
    plt.ylabel('Bankroll Size')
    if line != None:
        plt.axhline(y = line, linestyle='--')
    plt.tight_layout()

def count_optimal_fractions(top_fracs, fractions, probabilities):
    """
    Counts how often each fraction yields the highest final bankroll, per probability and overall.
    
    Inputs:
        top_fracs: List of lists, each sublist contains dicts with simulation results for one seed
        fractions: List or array of fractions used in the simulation
        probabilities: List or array of probabilities used
    
    Outputs: List with 2 indexes
        [0] overall_counter: Dict of overall best fraction frequencies
        [1] per_prob_counter: Dict[float -> Dict[fraction -> count]]
    """

    overall_counter = {f: 0 for f in fractions}
    per_prob_counter = {p: {f: 0 for f in fractions} for p in probabilities}

    for values in top_fracs:
        finals = [entry['bankroll history'][-1] for entry in values] # find all final bankrolls for this seed
        finals = np.array(finals)
        prob = values[0]['probability'] # gets current probability
        best_frac = fractions[np.argmax(finals)] # finds which fraction returned the highest final bankroll

        overall_counter[best_frac] += 1
        matched_prob = next((prob for p in probabilities if math.isclose(p, prob)), None)
        if matched_prob is not None:
            per_prob_counter[matched_prob][best_frac] += 1
        else:
            raise ValueError(f"Unexpected probability value: {prob}")
    return overall_counter, per_prob_counter

def plot_optimal_fractions(rows = 1, columns = 1, plot_num = 1, max_counter = {}, title = '', line = None):
    """
    Creates a subplot of a barplot grid of optimal fractions for a given probability.

    Inputs:
        rows, columns: Integer, # of rows and columns in plotting grid
        plot_num: Integer, current index of plot within plotting grid
        max_counter: Dictionary, contains frequencies of top performing fractions for one probability
        title: String, title of current subplot
        line: Float (optional), Y-axis value at which a line is drawn
    
    Outputs:
        Barplot sublot at a certain position in a plotting grid showing distributions of top fractions
    """
    colors = ['orange', 'cornflowerblue', 'greenyellow', 'hotpink', 'violet', 'mediumseagreen']
    plt.subplot(rows, columns, plot_num)
    plt.bar([str(f'{max_val:.2}') for max_val in max_counter.keys()], list(max_counter.values()), color=colors[(plot_num - 1)% 6])
    plt.title(title)
    plt.xlabel('Fraction')
    plt.ylabel('Frequency')
    if line != None:
        plt.axhline(y = line, linestyle='--', c='black')
    plt.tight_layout()