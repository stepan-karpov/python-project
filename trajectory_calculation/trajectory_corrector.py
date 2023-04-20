import krpc
import time

def calculate_angle(height):
    b = -30000
    k = 1350000
    c = 135
    return k / (height + b) + c

conn = krpc.connect(name='Vessel')

vessel = conn.space_center.active_vessel

flight_info = vessel.flight()
vessel.auto_pilot.target_pitch_and_heading(90, 90)
vessel.auto_pilot.engage()
vessel.control.throttle=1

print("Launch!")
vessel.control.activate_next_stage()

time.sleep(1)

while True:
    current_height = flight_info.mean_altitude
    vessel.auto_pilot.target_pitch_and_heading(90, 90)
    vessel.auto_pilot.target_pitch_and_heading(calculate_angle(current_height), 90)

