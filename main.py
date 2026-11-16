import numpy as np
import matplotlib.pyplot as plt

from model.Scenario import ProgressiveCarbonTaxWithElectrifiedFleet, Scenario
from model.State import State
from model.Vehicle import Vehicle

# The company never changes anything
def nothing_happens(_: State):
    return

# The company progressively removes its carbonated vehicles
def progressive_e_fleet(state: State):
    for (v, e) in [(Vehicle.AUTOCAR, Vehicle.E_AUTOCAR), (Vehicle.MINIBUS, Vehicle.E_MINIBUS)]:
        if (state.replace_vehicle(v, (e, State.default_distance))): break

def main():
    scenario = ProgressiveCarbonTaxWithElectrifiedFleet
    costs: list[float] = []
    emissions: list[float] = []

    while(not scenario.finished()):
        scenario.update()
        costs.append(scenario.state.fleet_price())
        emissions.append(scenario.state.fleet_emissions())

    plots = [
        (costs, "Coût par an (Carburant)", "cost"),
        (np.cumsum(np.array(costs)), "Coût cumulé par an (Carburant)", "cumulative_cost"),
        (emissions, "Emissions par an", "emissions")
    ]

    for i, (y, title, name) in enumerate(plots):
        plt.figure(i) # type: ignore
        plt.plot(Scenario.years, y) # type: ignore
        plt.title(title) # type: ignore
        plt.savefig(f"out/{name}.png") # type: ignore
        plt.close()

main()