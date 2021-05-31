import sys

class finite_automata:
    def __init__(self, no_states, final_states, transitions):
        self.no_states = no_states
        self.final_states = final_states
        self.transitions = transitions
        symbols = list() # stores all the symbols in the finite automata
        for t_key in transitions.keys():
            if t_key[1] not in symbols and t_key[1] != 'eps':
                symbols.append(t_key[1])
        self.symbols = symbols
    
    def possible_states(self, state): # returns a dictionary with possible states
        possible_states = dict()      # from each state on each symbol -> {<symbol> : <list_of_states>} 
        for symbol in self.symbols:
            for s in state:
                if (s, symbol) in list(self.transitions.keys()):  # if the transition is defined
                    if isinstance(self.transitions[(s, symbol)], list):
                        for s_1 in self.transitions[(s, symbol)]: # for each transition in the list
                            if symbol not in possible_states.keys(): # if the dict entry was not set
                                possible_states[symbol] = list()
                                possible_states[symbol].append(s_1)
                            elif s_1 not in possible_states[symbol]: # just append another one
                                possible_states[symbol].append(s_1)
                    else:
                        if symbol not in possible_states.keys():
                            possible_states[symbol] = list()
                            possible_states[symbol].append(self.transitions[(s, symbol)])
                        elif self.transitions[(s, symbol)] not in possible_states[symbol]:
                            possible_states[symbol].append(self.transitions[(s, symbol)])
        return possible_states

    def epsilon(self, state): # epsilonN function
        queue = list()        # returns every possible epsilon transition from a state
        for s in state:
            queue.append(s) # append each existing state into a queue for later use
        while len(queue) > 0:
            current = queue.pop(0) # for each existing state
            if (current, 'eps') in list(self.transitions.keys()):
                for t_key, t_val in self.transitions.items():
                    if (current, 'eps') == t_key: # if an epsilon transition exists
                        if isinstance(t_val, list):
                            for t in t_val:
                                if t not in state:
                                    state.append(t) # extend the current state with it
                                    queue.append(t)
                        else:
                            if t_val not in state:
                                state.append(t_val)
                                queue.append(t_val)
        return sorted(state)
    
def nfa_to_dfa(nfa): # main function
    final_states = []
    transitions = dict()
    states = dict() # dictionary to save dfa state with a list of nfa states -> {<dfa_state> : [<nfa_states>]}
    queue = [] # queue for later use

    start_state = nfa.epsilon([0]) # extend the initial state with epsilon
    states[0] = start_state
    queue.append(start_state) # append first state
    no_states = 1 # keep the number of states

    while len(queue) > 0:
        current = queue.pop(0)
        possible_states = nfa.possible_states(current) # states that are possible with each transition
        for s_key, s_val in possible_states.items():
            s_val = nfa.epsilon(s_val)                      # extend each one with epsilon
            if s_val not in states.values():
                states[no_states] = s_val                   # map states
                queue.append(s_val)                         # save another one
                key_list = list(states.keys())
                val_list = list(states.values())
                transitions[(key_list[val_list.index(current)], s_key)] = key_list[val_list.index(s_val)]
                no_states += 1                              # add the transitions
            elif s_val in states.values() and (current, s_key) not in list(transitions.keys()): 
                key_list = list(states.keys())              # if the state exists but the transition doesn't
                val_list = list(states.values())
                transitions[(key_list[val_list.index(current)], s_key)] = key_list[val_list.index(s_val)]
     
    states[no_states] = []              # add sink state for every missing transition
    for state in list(states.keys()):
        for symbol in nfa.symbols:
            if (state, symbol) not in list(transitions.keys()):
                transitions[(state, symbol)] = no_states
    no_states += 1

    for s_key, s_val in states.items():     # save final states
        for s in s_val:
            if isinstance(nfa.final_states, list):
                if s in nfa.final_states:
                    final_states.append(s_key)
            else:
                if s == nfa.final_states:
                    final_states.append(s_key)
    return finite_automata(no_states, final_states, transitions)

def main():
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    f = open(input_file, 'r')

    no_states = int(f.readline().strip())
    final_states = list(map(int, f.readline().strip().split(' ')))
    transitions = dict()

    for line in f:
        row = line.strip().split(' ')
        transitions[(int(row[0]), row[1])] = list(map(int, row[2:])) # {(<state>, <symbol>) : <next_state>}
    f.close()

    nfa = finite_automata(no_states, final_states, transitions) # object initialization
    dfa = nfa_to_dfa(nfa) # main function

    f = open(output_file, 'w')
    f.write(str(dfa.no_states) + '\n')
    for i in dfa.final_states:
        f.write(str(i) + ' ')
    f.write('\n')
    for t_key, t_value in dfa.transitions.items():
        f.write(str(t_key[0]) + ' ')
        f.write(t_key[1] + ' ')
        f.write(str(t_value) + '\n')
    f.close()

if __name__=="__main__":
    main()