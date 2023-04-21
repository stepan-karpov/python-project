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
  #   # print(Info.vessel.flight().speed)
  #   print(Info.get_mass())
  #   print(Info.get_ttw())
  #   print("=================")
  #   time.sleep(0.5)
