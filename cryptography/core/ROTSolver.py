class ROTSolver:
    _state = None
    _text = None

    def __init__(self, text, state: State)-> None:
        _text = text
        self.transition_to(state)

    def setText(text):
        _text = text

    def transition_to(self, state: State):
        """
        Alows to change State object at runtime.
        """

        self._state = state
        self._state.rotSolver = self

class State:

    @property
    def rotSolver(self) -> ROTSolver:
        return self._rotSolver

    @context.setter
    def rotSolver(self, rotSolver: ROTSolver) -> None:
        self._rotSolver = rotSolver

    @abstractmethod
    def solve(self) -> None:
        pass

class ManualState(State):
    def solve():
        pass

class AutomaticState(State):
    def solve():
        pass