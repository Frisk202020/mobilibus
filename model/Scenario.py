from typing import ReadOnly

from updates import carbon_tax, fleet, nothing
from .State import State, StateUpdate

"""
Define a scenario from 2020 to 2050

A scenario is defined by a list of state updaters (one for each year). Each year calls its updater in order, 
and the caller can retrieve current state's data at each step before calling `update` again (for plots).
"""
class Scenario:
    years: ReadOnly[list[int]] = [2020 + i for i in range(0, 31)] # from 2020 to 2050
    n_years: ReadOnly[int] = len(years)

    def __init__(self, updates: list[StateUpdate]):
        if (len(updates) != len(self.years)):
            raise Exception(f"Need {self.years} update functions")

        self.state = State()
        self.updates = updates
        self.current_year_id = 0

    def finished(self): return self.current_year_id == self.n_years

    def update(self):
        """
        Update state to next year
        """
        if self.finished():
            print("Scenario is finished")
            return

        self.updates[self.current_year_id](self.state)
        self.current_year_id += 1

    @classmethod
    def static(cls, update: StateUpdate):
        """
        Generate a scenario having the same state update over its lifetime

        :param update: A function called every year to update the state
        :return: A scenario from 2020 to 2050
        """
        return Scenario([update for _ in range(cls.n_years)])

    def combine(self, other: Scenario):
        """
        Combine two scenarios, that is, each year will call the two state updaters

        :param other: A scenario to combine. Notice the update from `self` will be called before `other`'s
        :return: The combined scenario
        """
        combined: list[StateUpdate] = []

        for (x, y) in zip(self.updates, other.updates):
            def update(state: State):
                x(state)
                y(state)

            combined.append(update)

        return Scenario(combined)

NothingHappens = Scenario.static(nothing.nothing_happens)
ProgressiveElectricalFleet = Scenario.static(fleet.progressive_e_fleet)

n = int(Scenario.n_years / 3)
_progressive_carbon_tax = \
    carbon_tax.linear_carbon_tax(0, 100, n) + \
    carbon_tax.linear_carbon_tax(100, 250, n)
_progressive_carbon_tax += carbon_tax.linear_carbon_tax(250, 300, Scenario.n_years - len(_progressive_carbon_tax))

ProgressiveCarbonTax = Scenario(_progressive_carbon_tax)
ProgressiveCarbonTaxWithElectrifiedFleet = ProgressiveCarbonTax.combine(ProgressiveElectricalFleet)