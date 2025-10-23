from .state import State


def Node_1(state: State) -> State:
    return {"count": [state["count"][-1] + 1]}


def Node_2(state: State) -> State:
    return {"count": [state["count"][-1] + 1]}


def Node_3(state: State) -> State:
    return {"count": [state["count"][-1] + 1]}


def Node_4(state: State) -> State:
    return {"count": [state["count"][-1] + 1]}
