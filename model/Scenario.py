from typing import ReadOnly

from updates import carbon_tax, fleet, nothing
from .State import State, StateUpdate

class _Combined:
    def __init__(self, *callables: StateUpdate):
        self.callables = callables

    def update(self, state: State):
        for x in self.callables:
            x(state)

class Scenario:
    years: ReadOnly[list[int]] = [2020 + i for i in range(0, 31)]
    n_years: ReadOnly[int] = len(years)

    def __init__(self, updates: list[StateUpdate]):
        if (len(updates) != len(self.years)):
            raise Exception(f"Need {self.years} update functions")

        self.state = State()
        self.updates = updates
        self.current_year_id = 0

    def finished(self): return self.current_year_id == self.n_years

    def update(self):
        if self.finished():
            print("Scenario is finished")
            return

        self.updates[self.current_year_id](self.state)
        self.current_year_id += 1

    @classmethod
    def static(cls, update: StateUpdate):
        return Scenario([update for _ in range(cls.n_years)])

    def combine(self, other: Scenario):
        combined = [_Combined(x, y) for (x, y) in zip(self.updates, other.updates)]
        updates = [x.update for x in combined]

        return Scenario(updates)

NothingHappens = Scenario.static(nothing.nothing_happens)
ProgressiveElectricalFleet = Scenario.static(fleet.progressive_e_fleet)

n = int(Scenario.n_years / 3)
_progressive_carbon_tax = \
    carbon_tax.linear_carbon_tax(0, 100, n) + \
    carbon_tax.linear_carbon_tax(100, 250, n)
_progressive_carbon_tax += carbon_tax.linear_carbon_tax(250, 300, Scenario.n_years - len(_progressive_carbon_tax))

ProgressiveCarbonTax = Scenario(_progressive_carbon_tax)
ProgressiveCarbonTaxWithElectrifiedFleet = ProgressiveCarbonTax.combine(ProgressiveElectricalFleet)