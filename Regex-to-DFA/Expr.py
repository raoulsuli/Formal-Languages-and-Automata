class Expr:
    def printTree(self, tabs: int):
        return ""

    def buildNFA(self, nfa):
        return None
        


class Append(Expr):
    def __init__(self, left: Expr, right: Expr):
        self.left: Expr = left
        self.right: Expr = right

    def printTree(self, tabs: int):
        print("\t" * tabs + "")
        self.left.printTree(tabs + 1)
        self.right.printTree(tabs + 1)

    def buildNFA(self, nfa):
        transitions = {}
        last_state = nfa.finalState
        states = [last_state + 1, last_state + 2]
        finalState = last_state + 2

        transitions[last_state, self.left.buildNFA(nfa)] = last_state + 1
        transitions[last_state + 1, self.right.buildNFA(nfa)] = last_state + 2

        nfa.merge(states, finalState, transitions)

class Par(Expr):
    def __init__(self, expr: Expr):
        self.expr: Expr = expr

    def printTree(self, tabs: int):
        print("\t" * tabs + "(")
        self.expr.printTree(tabs + 1)
        print("\t" * tabs + ")")

    def buildNFA(self, nfa):
        if isinstance(self.expr, Expr):
            return self.expr.buildNFA(nfa)
        

class Union(Expr):
    def __init__(self, left: Expr, right: Expr):
        self.left: Expr = left
        self.right: Expr = right

    def printTree(self, tabs: int):
        print("\t" * tabs + "|")
        self.left.printTree(tabs + 1)
        self.right.printTree(tabs + 1)

    def buildNFA(self, nfa):
        transitions = {}
        last_state = nfa.finalState
        states = [last_state + 1, last_state + 2, last_state + 3, last_state + 4, last_state + 5]
        finalState = last_state + 5

        transitions[last_state, 'eps'] = [last_state + 1, last_state + 3]
        transitions[last_state + 1, self.left.buildNFA(nfa)] = last_state + 2
        transitions[last_state + 2, 'eps'] = last_state + 5
        transitions[last_state + 3, self.right.buildNFA(nfa) if isinstance(self.right, Expr) else self.right] = last_state + 4
        transitions[last_state + 4, 'eps'] = last_state + 5
        nfa.merge(states, finalState, transitions)

class Star(Expr):
    def __init__(self, expr: Expr):
        self.expr: Expr = expr

    def printTree(self, tabs: int):
        print("\t" * tabs + "*")
        self.expr.printTree(tabs + 1)

    def buildNFA(self, nfa):
        transitions = {}
        last_state = nfa.finalState
        states = [last_state + 1]
        finalState = last_state + 1

        transitions[last_state, 'eps'] = last_state + 1
        transitions[last_state, self.expr.buildNFA(nfa)] = last_state + 1
        transitions[last_state + 1, 'eps'] = last_state
        nfa.merge(states, finalState, transitions)
        

class Letter(Expr):
    def __init__(self, letter: str):
        self.letter = letter

    def printTree(self, tabs: int):
        print("\t" * tabs + self.letter)

    def buildNFA(self, nfa):
        transitions = {}
        last_state = nfa.finalState
        states = [last_state + 1]
        finalState = last_state + 1

        transitions[last_state, self.letter] = last_state + 1
        nfa.merge(states, finalState, transitions)
