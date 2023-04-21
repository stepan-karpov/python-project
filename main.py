import sys
from interface.window import MainWindow
from flight_info.info import Info
import time

if __name__ == "__main__":
  window = MainWindow()
  window.start_application()

  # Info.vessel.control.throttle=1
  # time.sleep(1)
  # print("Launch!")

  # Info.vessel.control.activate_next_stage()

  # while (True):
  #   print(Info.get_vertical_speed_coordinates())
  #   print(Info.get_horizontal_speed_coordinates())
  #   print("=================")
  #   time.sleep(0.5)
