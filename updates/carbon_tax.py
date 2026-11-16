from model.State import State, StateUpdate

class __IncreaseCarbonTax:
    def __init__(self, step: float):
        self.__step = step  

    def update(self, state: State):
        state.carbon_tax += self.__step

def linear_carbon_tax(start: float, end: float, duration: int) -> list[StateUpdate]:
    updater = __IncreaseCarbonTax((end - start) / duration)
    return [updater.update for _ in range(duration)]

    
