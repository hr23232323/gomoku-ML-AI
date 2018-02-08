from inspect import isclass


REGISTERED_PLAYERS = {}
REGISTERED_HEURISTICS = {}

def register(name):
    def decorator(obj):
        if isclass(obj):
            REGISTERED_PLAYERS[name] = obj
        else:
            REGISTERED_HEURISTICS[name] = obj
        return obj
    return decorator