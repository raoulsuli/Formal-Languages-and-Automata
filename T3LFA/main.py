from typing import Dict, Tuple, Optional, List
from Stack import Stack
from Expr import *
from NFA2DFA import *
import string, sys

EPS = ""
UNION = "|"
OPEN = "("
CLOSE = ")"
STAR = "*"
alphabet = list(string.ascii_lowercase)

State = int
WORD = 0
POP = 1
PUSH = 2
Transition = (str, str, str)

class Parser:
    def __init__(self):
        self.states: List[State] = [0, 1]
        self.initialState: State = 0
        self.finalStates: List[State] = [1]

        self.transitions: Dict[Tuple[State, Transition], State] = {}

        self.transitions[0, (OPEN, EPS, OPEN)] = 0
        for c in alphabet:
            self.transitions[0, (c, EPS, c)] = 1
            self.transitions[1, (c, EPS, c)] = 1

        self.transitions[1, (CLOSE, EPS, CLOSE)] = 1
        self.transitions[1, (STAR, EPS, STAR)] = 1
        self.transitions[1, (UNION, EPS, UNION)] = 0
        self.transitions[1, (CLOSE, EPS, CLOSE)] = 1
        self.transitions[1, (OPEN, EPS, OPEN)] = 0

        self.stack: Stack = Stack()

    def nextState(self, currentState: State, word: str) -> Optional[State]:
        for (state, transition) in self.transitions.keys():
            if state == currentState:
                if word[0] == transition[WORD]:
                    if transition[PUSH] != EPS:
                        self.stack.push(transition[PUSH])

                    return self.transitions[(state, transition)]
        return None

    def reduceLetter(self):
        letter = self.stack.pop()
        self.stack.push(Letter(letter))
    
    def reducePar(self):
        if self.stack.peek(0) != CLOSE:
            return

        self.stack.pop()
        prevExpr = self.stack.pop()
        self.stack.pop()
        self.stack.push(Par(prevExpr))

    def reduceStar(self): 
        self.stack.pop()
        prevExpr = self.stack.pop()
        self.stack.push(Star(prevExpr))

    def reduceAppend(self, close):
        pos_open = 0
        if close == 1:
            while self.stack.peek(pos_open) != OPEN:
                pos_open += 1
        else:
            pos_open = self.stack.size() - 1
        
        for i in range(pos_open, 0, -1):
            if isinstance(self.stack.peek(i), Expr) and isinstance(self.stack.peek(i - 1), Expr):
                
                prevExpr = self.stack.peek(i)
                prevExpr2 = self.stack.peek(i - 1)
                
                self.stack.remove(prevExpr)
                self.stack.remove(prevExpr2)

                self.stack.insert_elem(i - 1, Append(prevExpr, prevExpr2))
                
                if close == 1:
                    while pos_open > self.stack.size() - 1 and self.stack.peek(pos_open) != OPEN:
                        pos_open -= 1
                i = pos_open
        
    def reduceUnion(self, close):
        pos_open = 0
        if close == 1:
            while self.stack.peek(pos_open) != OPEN:
                pos_open += 1
        else:
            pos_open = self.stack.size() - 1

        for i in range(pos_open, 0, -1):
            if isinstance(self.stack.peek(i), Expr) and self.stack.peek(i - 1) == UNION:

                prevExpr = self.stack.peek(i)
                prevExpr2 = self.stack.peek(i - 2)
                unionExpr = self.stack.peek(i - 1)

                self.stack.remove(prevExpr)
                self.stack.remove(prevExpr2)
                self.stack.remove(unionExpr)

                self.stack.insert_elem(i - 1, Union(prevExpr, prevExpr2))
                
                if close == 1:                
                    while pos_open > self.stack.size() - 1 and self.stack.peek(pos_open) != OPEN:
                        pos_open -= 1
                i = pos_open

    def reduce(self) -> bool:
        if self.stack.peek(0) in alphabet:
            self.reduceLetter()
            return True
        if self.stack.peek(0) == STAR and isinstance(self.stack.peek(1), Expr):
            self.reduceStar()
            return True
        if self.stack.peek(0) == CLOSE:
            self.reduceAppend(1)
            self.reduceUnion(1)
            self.reducePar()
            return True

        return False

    def parse(self, word: str) -> Optional[Expr]:
        currentState = self.initialState

        while word != EPS:
            currentState = self.nextState(currentState, word)
            if currentState is None:
                break
            
            word = word[1:]

            while self.reduce():
                continue
        
        if self.stack.size() != 1:
            self.reduceAppend(0)
            self.reduceUnion(0)
            self.reducePar()
        
        if word != EPS and self.stack.size() != 1:
            return None

        return self.stack.pop()

class NFA:
    def __init__(self):
        self.states = []
        self.initialState = 0
        self.finalState = 0
        self.transitions = {}

    def merge(self, states, finalState, transitions):
        for s in states:
            if s not in self.states:
                self.states.append(s)
        
        self.finalState = finalState
        
        for (k1, k2), val in transitions.items():
            if k2 != None:
                if len(list(self.transitions.keys())) > 1 and (k1, k2) in list(self.transitions.keys()):
                    if isinstance(self.transitions[k1, k2], list) and val not in self.transitions[k1, k2]:
                        if isinstance(val, list):
                            for s in val:
                                if s not in self.transitions[k1, k2]:
                                    self.transitions[k1, k2].append(s)
                        else:
                            if isinstance(val, list):
                                for s in val:
                                    if s not in self.transitions[k1, k2]:
                                        self.transitions[k1, k2].append(s)
                            else:
                                self.transitions[k1, k2].append(val)
                    elif not isinstance(self.transitions[k1, k2], list) and val != self.transitions[k1, k2]:
                        aux = []
                        aux.append(self.transitions[k1, k2])
                        if isinstance(val, list):
                            for s in val:
                                if isinstance(self.transitions[k1, k2], list):
                                    if s not in self.transitions[k1, k2]:
                                        aux.append(s)
                                else:
                                    if s != self.transitions[k1, k2]:
                                        aux.append(s)
                        else:
                            aux.append(val)
                        self.transitions[k1, k2] = aux
                else:
                    self.transitions[k1, k2] = val

inputFile = sys.argv[1]
nfaFile = sys.argv[2]
dfaFile = sys.argv[3]

f = open(inputFile, "r")
inputText = f.read()

f = open(nfaFile, "w+")
g = open(dfaFile, "w+")

parser = Parser()
expr = parser.parse(inputText)

if expr is not None:
    nfa = NFA()

    if isinstance(expr, Expr):
        expr.buildNFA(nfa)
    
        for i in range(len(nfa.states)):
            if i not in nfa.states:
                nfa.states.append(i)
        nfa.states = sorted(nfa.states)
        nfa.finalState = nfa.states[-1] if len(nfa.states) > 0 else 0

        f.write(str(len(nfa.states)) + "\n" + str(nfa.finalState) + "\n")
        for (k1, k2), val in nfa.transitions.items():
            f.write(str(k1) + " ")
            f.write(k2 + " ")
            if not isinstance(val, list):
                f.write(str(val) + " ")
            else:
                for s in val:
                    f.write(str(s) + " ")
            f.write("\n")


        dfa = nfa_to_dfa(finite_automata(len(nfa.states), nfa.finalState, nfa.transitions))
        g.write(str(dfa.no_states) + "\n")
        if isinstance(dfa.final_states, list):
            for s in dfa.final_states:
                g.write(str(s) + " ")
            g.write("\n")
        else:
            g.write(str(dfa.final_states) + "\n")
        for (p, s), val in dfa.transitions.items():
            g.write(str(p) + " " + str(s) + " " + str(val) + "\n")
    else:
        f.write("1\n0\n0 eps 0")
        g.write("1\n0\n0 b 0")

else:
    print("Nu am putut parsa cuvantul")