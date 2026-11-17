from typing import Callable, ReadOnly
from .Vehicle import Vehicle

"""
Each scenario has a state that evolves along the years.
A scenario can mutate attributes of the state along the years, including :
    - fleet using dedicated methods (to enforce that a vehicle in the fleet should also define the distance it's expected to travel over 1 year)
    - costs and taxes
    - vehicles consumptions

Then, a scenario retrieves cost data (fleet_price) and emissions (fleet_emissions)
"""
class State:
    start_autocars: ReadOnly[int] = 12
    start_minibuses: ReadOnly[int] = 8
    start_total_distance: ReadOnly[int] = 850000

    diesel_emission: ReadOnly[float] = 2.68 # Kg_CO2 / L
    e_emission: ReadOnly[float] = .05 # KgCO2 / kWh
    vehicles: ReadOnly[set[Vehicle]] = set(Vehicle.all())
    default_distance: ReadOnly[float] = start_total_distance / (start_autocars + start_minibuses)  

    def __init__(self):
        distance = self.start_total_distance / (self.start_autocars + self.start_minibuses)

        self.__fleet = [(x, distance) for x in 
            [Vehicle.AUTOCAR for _ in range(12)] + [Vehicle.MINIBUS for _ in range(8)]
        ]
        
        self.e_cost = .20 # € / kWh
        self.diesel_cost = 2.25 # € / L
        self.carbon_tax = 0. # € / Kg_Co2

        self.autocar_diesel_consumption = 30 # L / 100km
        self.minibus_diesel_consumption = 10 # L / 100km
        self.autocar_e_consumption = 45 # kWh / 100km
        self.minibus_e_consumption = 150 # kWh / 100km

    def __total_diesel_cost(self):
        return self.diesel_cost + (self.diesel_emission * self.carbon_tax)

    def __total_e_cost(self):
        return self.diesel_cost + (self.e_emission * self.carbon_tax)

    def __filter(self, filter: set[Vehicle]):
        return [x for x in self.__fleet if x[0] in filter]

    def __price(self, v: Vehicle):
        match(v):
            case Vehicle.MINIBUS: return self.minibus_diesel_consumption * self.__total_diesel_cost()
            case Vehicle.AUTOCAR: return self.autocar_diesel_consumption * self.__total_diesel_cost()
            case Vehicle.E_MINIBUS: return self.minibus_e_consumption * self.__total_e_cost()
            case Vehicle.E_AUTOCAR: return self.autocar_e_consumption * self.__total_e_cost()

    def __emissions(self, v: Vehicle):
        match(v):
            case Vehicle.MINIBUS: return self.minibus_diesel_consumption * self.diesel_emission
            case Vehicle.AUTOCAR: return self.autocar_diesel_consumption * self.diesel_emission
            case Vehicle.E_MINIBUS: return self.minibus_e_consumption * self.e_emission
            case Vehicle.E_AUTOCAR: return self.autocar_e_consumption * self.e_emission

    def get_fleet(self): return list(self.__fleet)

    def replace_vehicle(self, target: Vehicle, replace_by: tuple[Vehicle, float]|None = None):
        """
        Replace the first occurrence of one vehicle type by another
    
        :param target: The type of vehicle to search and delete.
        :param replace_by: The type of vehicle to replace by along with its expected travel distance. None if we only intend to delete.
        :return: True if a instance of the target vehicle was found in the fleet 
        """
        
        index = next((i for i, (v, _) in enumerate(self.__fleet) if v == target), None)
        if (index == None): return False

        if replace_by == None: del self.__fleet[index]
        else: self.__fleet[index] = replace_by

        return True

    def fleet_price(self, filter: set[Vehicle] = vehicles):
        """
        Get the total price of the current fleet

        :param filter: the set of vehicle types to consider in the fleet. By default, all types are included so we output the price of the entire fleet
        :return: the total price
        """
        return sum([self.__price(x[0]) * x[1] for x in self.__filter(filter)])

    def fleet_emissions(self, filter: set[Vehicle] = vehicles):
        """
        Get the total emissions of the current fleet

        :param filter: the set of vehicle types to consider in the fleet. By default, all types are included so we output the price of the entire fleet
        :return: the total price
        """
        return sum([self.__emissions(x[0]) * x[1] for x in self.__filter(filter)])

StateUpdate = Callable[[State], None]
    