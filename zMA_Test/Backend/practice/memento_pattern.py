class Memento:
    def __init__(self, state):
        self.state = state

    def getState(self):
        return self.state


class Originator:
    def __init__(self):
        self.state = []

    def setState(self, state):
        self.state = state

    def save(self):
        print('Originator: saving to memento')
        return Memento(self.state)

    def restore(self, memento):
        self.state = memento.getState()
        print('State after restoring from memento: ', self.state)
        return self.state


class Caretaker:
    mementos = []

    def addMemento(self, memento):
        self.mementos.append(memento)

    def getMemento(self, position):
        return self.mementos[position]
