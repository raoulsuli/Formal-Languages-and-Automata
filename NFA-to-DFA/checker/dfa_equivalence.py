from dfa import DFA


def symmetric_difference(lhs, rhs):
    """Construct the symmetric difference of two automata.

    lhs and rhs are the two input automata and res is the result of this
    function:

    L(res) = (L(lhs) \ L(rhs)) u (L(rhs) \ L(lhs))

    res can be constructed by building the product of lhs and rhs and setting
    the final states as: (lhs.F x ~rhs.F) u (~lhs.F x rhs.F)

    """
    def new_state_name(ls, rs):
        return ls * len(rhs.states) + rs

    # the automatons should have the same alphabet!
    alphabet = lhs.alphabet
    states = set(range(len(lhs.states) * len(rhs.states)))

    final_states = set()
    for ls in lhs.states:
        for rs in rhs.states:
            ns = new_state_name(ls, rs)
            if (ls in lhs.final_states) and (rs not in rhs.final_states) or \
                    (ls not in lhs.final_states) and (rs in rhs.final_states):
                final_states.add(ns)

    start_state = new_state_name(lhs.start_state, rhs.start_state)

    delta = {}
    for ls in lhs.states:
        for rs in rhs.states:
            for ch in alphabet:
                ns = new_state_name(ls, rs)
                nns = new_state_name(lhs.delta[(ls, ch)], rhs.delta[(rs, ch)])
                delta[(ns, ch)] = nns

    return DFA(alphabet, states, start_state, final_states, delta)


def empty_language(a):
    """Checks whether the given DFA recognizes the empty language.

    Performs DFS to see if there any reachable final states.

    """
    visited = [False for state in a.states]

    def dfs_reach_final(state):
        visited[state] = True
        for ch in a.alphabet:
            nstate = a.delta[(state, ch)]
            if nstate in a.final_states:
                return True

            if not visited[nstate]:
                if dfs_reach_final(nstate):
                    return True

        return False

    return not dfs_reach_final(a.start_state)


def language_eq(lhs, rhs):
    """Checks whether two DFAs recognize the same language."""
    da = symmetric_difference(lhs, rhs)
    return empty_language(da)
