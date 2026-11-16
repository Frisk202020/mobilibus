from model.State import State
from model.Vehicle import Vehicle

# The company progressively removes its carbonated vehicles
def progressive_e_fleet(state: State):
    for (v, e) in [(Vehicle.AUTOCAR, Vehicle.E_AUTOCAR), (Vehicle.MINIBUS, Vehicle.E_MINIBUS)]:
        if (state.replace_vehicle(v, (e, State.default_distance))): break