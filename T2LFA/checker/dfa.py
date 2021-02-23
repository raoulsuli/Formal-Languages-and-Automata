class DFA(object):
    """Model a Nondeterministic Finite Automaton

    The automaton contains the following:

        - "alphabet": a set of symbols
        - "states": set of non-negative integers
        - "start_state": a member of "states"
        - "final_states": a subset of "states"
        - "delta": a dictionary from configurations to states
                {(state, symbol): state}
                where "state" is a member of "states" and "symbol" is a member
                of "alphabet"

    """

    def __init__(self, alphabet, states, start_state, final_states, delta):
        """See class docstring"""
        assert start_state in states
        assert final_states.issubset(states)
        for symbol in "()*|":
            assert symbol not in alphabet

        self.alphabet = alphabet
        self.states = states
        self.start_state = start_state
        self.final_states = final_states
        self.delta = delta
        self.sink_state = None

    def get_sink_state(self):
        """Get the sink state if any

        If the DFA does not have a sink state, None will be returned.
        The sink state is computed the first time this function is called.

        Note that this is only meaningful for minimized DFAs!

        """
        if self.sink_state is not None:
            return self.sink_state

        for state in self.states:
            if state in self.final_states:
                continue

            is_sink = True
            for symbol in self.alphabet:
                if self.delta[(state, symbol)] != state:
                    is_sink = False

            if is_sink:
                self.sink_state = state
                return self.sink_state

        return None

    def accept(self, string):
        """Check if a string is in the DFA's language"""
        current_state = self.start_state
        sink_state = self.get_sink_state()
        for symbol in string:
            current_state = self.delta.get((current_state, symbol), sink_state)
            if current_state == sink_state:  # early bailout
                return False

        return current_state in self.final_states


def parse_dfa(text):
    """Ad-hoc parsing of an dFA.

    text must have the following format:

    <number of states>
    <final state 1> <final state 2> ... <final state n>
    <current state> <simbol> <next state>
    <current state> <simbol> <next state>
    ...
    <current state> <simbol> <next state>

    """
    def build_delta(transitions):
        delta = {}
        alphabet = set()
        for transition in transitions:
            elems = transition.split()
            delta[(int(elems[0]), elems[1])] = int(elems[2])
            alphabet.add(elems[1])

        return delta, alphabet

    lines = text.splitlines()
    final_states = set(int(s) for s in lines[1].split())
    delta, alphabet = build_delta(lines[2:])
    states = set(range(0, int(lines[0])))

    return DFA(alphabet, states, 0, final_states, delta)
