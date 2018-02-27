# Team HGo - Gomoku AI
# Harsh Rana

This program uses Python 3.6 and utilizes the following pip modules: 
    Fire, 
    Halo, 
    Numpy, 
    Pytest (if you want to run the test cases)

To make the AI play itself locally run 
`python start.py local --a1=[agent_from_list] --a2=[agent_from_list] --h1=[heuristic_from_list] --h2=[heuristic_from_list] start`
    For Example: `python start.py local --a1=ab --a2=ab --h1=aggressive --h2=winning-windows start`

To play a reffed game run:
`python start.py reffed --team_name=[name_string] --a=[agent_from_list] --h=[heuristic_from_list] start`
    For Example: `python start.py reffed --team_name=HGo --a=ab --h=aggressive start`

List of Heuristics:
    'aggressive' (USE)
    `winning-windows`
    `threat-space`

List of Agents:
    `ab` - Alpha-Beta Pruning w/ iterative deepening (USE)

To get rid of all the referee files run `./clean`