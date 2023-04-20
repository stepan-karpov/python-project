import sys
from interface.window import MainWindow
from flight_info.info import Info
import time

if __name__ == "__main__":
  # window = MainWindow()
  # window.start_application()
  print(Info.get_launch_coordinated())
  # Info.vessel.auto_pilot.target_pitch_and_heading(90,90)
  # Info.vessel.auto_pilot.engage()
  Info.vessel.control.throttle=1
  time.sleep(1)
  print("Launch!")

  Info.vessel.control.activate_next_stage()

  while (True):
    print(Info.get_launch_coordinated())
    time.sleep(2)