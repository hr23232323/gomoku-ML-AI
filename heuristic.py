from registry import register
import numpy as np


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



# Return # of open 3 in a row * points attached
@register('open3')
def open_3(state):
    row_3 = np.array([0, 1, 1, 1, 0])
    r = state.run
    friendly_windows = 0

    for section in state.sections:
        if section.size < r:
            continue
        windows = rolling_window(section, r)

        for window in windows:
            #print(window, row_3)
            if(np.array_equal(window, row_3)):
                print('w', 'r', window)
                friendly_windows += 1

    if(friendly_windows > 0):
        print(friendly_windows)
    #print('\n')


    return friendly_windows + winning_windows(state)

