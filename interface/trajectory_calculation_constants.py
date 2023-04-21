from flight_info.info import *

INIT_FLIGH_DATA = {
  "height": (-1, Info.get_height),
  "ttw": (-1, Info.get_ttw),
  "speed": (-1, Info.get_speed),
  "thrust": (-1, Info.get_thrust),
  "g": (-1, Info.get_g),
  "pressure": (-1, Info.get_pressure)
}

INIT_VESSEL_DATA = {
  "fuel on current stage": (-1, Info.get_fuel),
  "mass of the vessel": (-1, Info.get_mass),
}
