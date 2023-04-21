from flight_info.info import *

INIT_FLIGH_DATA = {
  "height, m": (-1, Info.get_height),
  "ttw": (-1, Info.get_ttw),
  "speed, m/s": (-1, Info.get_speed),
  "thrust, N": (-1, Info.get_thrust),
  "g, m/s^2": (-1, Info.get_g),
  "pressure, Pa": (-1, Info.get_pressure)
}

INIT_VESSEL_DATA = {
  "fuel on current stage, kg": (-1, Info.get_fuel),
  "mass of the vessel, kg": (-1, Info.get_mass),
}
