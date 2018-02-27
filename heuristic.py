from registry import register
import numpy as np
import math as math


@register('dumb')
def dumb(state):
    return 0

# Counts the run length of each run and adds it to that players value. Return player - enemy values as heuristic
@register('threat-space')
def threat_space(state):
    Player_Run_Val = 0
    Enemy_Run_Val = 0
    for section in state.sections:
        runs = np.split(section, np.where(np.diff(section) != 0)[0] + 1)
        run_sizes = [(run[0], run.size) for run in runs if run[0] != 0 and run.size >= 2]
        for size in run_sizes:
            if(size[0] == state.next_player):
                Player_Run_Val += size[1]
            elif(size[0] == (-1 * state.next_player)):
                Enemy_Run_Val += size[1]
    return Player_Run_Val - Enemy_Run_Val


def rolling_window(a, window):
    if a.size == window:
        return np.array([a])
    shape = a.shape[:-1] + (a.shape[-1] - window, window)
    strides = a.strides + (a.strides[-1],)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)




# https://web.stanford.edu/class/cs221/2017/restricted/p-final/xiaotihu/final.pdf
@register('winning-windows')
def winning_windows(state):
    r = state.run    
    v = np.zeros(r - 1)
    ve = np.zeros(r - 1)
    #print(r, v, ve)
    for section in state.sections:
        #print(section)
        if section.size < r:
            continue
        windows = rolling_window(section, r)
        
        for window in windows:
            #print(window)
            unique, _ = np.unique(window, return_counts=True)
            if set(unique) == set([0, 1]):
                window_count = window.sum()
                v[window_count - 1] += 1
            elif set(unique) == set([0, -1]):
                window_count = window.sum() * -1
                ve[window_count - 1] += 1
    return np.multiply(np.arange(1, 5)**2, v).sum() 


@register('aggressive-stupid')
def aggressive_stupid(state):
    num_open2 = open_2(state)
    num_open3 = open_3(state)
    num_open4 = open_4(state)
    num_open5 = win_5(state)

    sum_offense = (num_open2 * 2) + (num_open3 * 3) + (num_open4 * 4) + (num_open5 * 10)
    #if(sum_offense > 0):
     #   print('2','3','4','5', 'sum', num_open2, num_open3, num_open4, num_open5, sum_offense)

    #if(sum_offense > 0):
        #print(state.grid)
    return sum_offense


@register('aggressive')
def aggressive(state):
    weight_open2 = sigmoid(open_2(state))
    weight_open3 = sigmoid(open_3(state))
    weight_open4 = sigmoid(open_4(state))
    weight_win5 = sigmoid(win_5(state))

    sum_offense = (weight_open2 * 2) + (weight_open3 * 5) + (weight_open4 * 25) + (weight_win5 * 100)

    weight_abs_def = sigmoid(abs_def(state))
    weight_must_def = sigmoid(must_def(state))

    sum_defense = (weight_abs_def * 40) + (weight_must_def * 60)

    final_sum = sum_offense + sum_defense
    
    return final_sum



#returns the sigmoid activation function of a given x
def sigmoid(x_value):
    sig = 1 / (1 + math.exp(-x_value))
    return sig


# Return # of open 3 in a row * points attached
def open_3(state):
    row_3 = np.array([0, 1, 1, 1, 0])

    r = state.run
    num3 = 0

    for section in state.sections:
        if section.size < r:
            continue
        windows = rolling_window(section, r)

        for window in windows:
            if((window==row_3).all()):
                #print('c1', 'c2', counter1, counter2)
                num3 += 1

    return num3


# Return # of open 3 in a row * points attached
def open_2(state):
    row_2 = np.array([0, 1, 1, 0, 0])
    row_2_1 = np.array([0, 0, 1, 1, 0])
    r = state.run
    num2 = 0

    for section in state.sections:
        if section.size < r:
            continue
        windows = rolling_window(section, r)

        for window in windows:
            if((window==row_2).all() or (window==row_2_1).all()):
                #print('w', 'r', window)
                num2 += 1

    return num2


# Return # of open 3 in a row * points attached
def open_4(state):
    row_4 = np.array([0, 1, 1, 1, 1, 0])
    r = state.run + 1
    num4 = 0

    for section in state.sections:
        if section.size < r:
            continue
        windows = rolling_window(section, r)

        for window in windows:
            if((window==row_4).all()):
                #print('w', 'r', window)
                num4 += 1


    return num4

# Return # of open 3 in a row * points attached
def win_5(state):
    row_5 = np.array([1, 1, 1, 1, 1])
    r = state.run
    num5 = 0

    for section in state.sections:
        if section.size < r:
            continue
        windows = rolling_window(section, r)

        for window in windows:
            if((window==row_5).all()):
                #print('w', 'r', window)
                num5 += 1
    return num5



# Return # of ABSOLUTE defensive windows
# ABSOLUTE Defensive window is one where if we don't defend, we lose in <2 moves (of opponent)
def abs_def(state):
    def_window = np.array([1, -1, -1, -1, 0])
    def_window_2 = np.array([0, -1, -1, -1, 1])
    r = state.run
    num_abs_def = 0

    for section in state.sections:
        if section.size < r:
            continue
        windows = rolling_window(section, r)

        for window in windows:
            if((window==def_window).all() or (window==def_window_2).all()):
                #print('w', 'r', window)
                num_abs_def += 1

    #if(num_abs_def > 0):
    #    print(num_abs_def)
    #    print(state.grid)
    return num_abs_def


# Return # of MUST defensive windows
# MUST Defensive window is one where if we don't defend, we lose in <1 moves (of opponent)
def must_def(state):
    must_def = np.array([1, -1, -1, -1, -1, 1])
    r = state.run + 1
    num_must_def = 0

    for section in state.sections:
        if section.size < r:
            continue
        windows = rolling_window(section, r)

        for window in windows:
            if((window==must_def).all()):
                #print('w', 'r', window)
                num_must_def += 1

    #if(num_must_def > 0):
    #    print('must def', num_must_def)
    #    print(state.grid)
    return num_must_def 