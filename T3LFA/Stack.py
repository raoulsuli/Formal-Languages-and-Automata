class Stack:
    def __init__(self):
        self.stack = []

    def push(self, el):
        self.stack.append(el)

    def peek(self, pos):
        if pos < len(self.stack):
            return self.stack[-(pos + 1)]

        return None

    def pop(self):
        el = self.peek(0)
        self.stack.pop()
        return el

    def empty(self):
        return self.stack == []

    def size(self):
        return len(self.stack)
    
    def remove(self, elem):
        self.stack.remove(elem)
     
    def insert_elem(self, pos, elem):
        self.stack.insert(self.size() - pos, elem)