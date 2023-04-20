import krpc
import math

class Info:
  conn = krpc.connect(name='Vessel')
  vessel = conn.space_center.active_vessel
  start_coordinates = (
    vessel.position(vessel.orbit.body.reference_frame)[2],
    vessel.position(vessel.orbit.body.reference_frame)[0],
  )
  rotation_angle = -math.pi - math.atan(start_coordinates[1] / start_coordinates[0])

  rotation_matrix = (
    (math.cos(rotation_angle), -math.sin(rotation_angle)),
    (math.sin(rotation_angle), math.cos(rotation_angle))
  )

  kerbin_radius = start_coordinates[0] * rotation_matrix[0][0] + start_coordinates[1] * rotation_matrix[0][1]

  @classmethod
  def get_kerbin_coordinates(cls):
    return cls.vessel.position(cls.vessel.orbit.body.reference_frame)
  
  @classmethod
  def kerbin_to_launch_coordinates(cls, current_kerbin_coordinates):
    rotated_coordinates = (
      -current_kerbin_coordinates[0] * cls.rotation_matrix[1][0] - current_kerbin_coordinates[1] * cls.rotation_matrix[1][1], 
      current_kerbin_coordinates[0] * cls.rotation_matrix[0][0] + current_kerbin_coordinates[1] * cls.rotation_matrix[0][1] - cls.kerbin_radius, 
    )
    return rotated_coordinates

  @classmethod
  def get_launch_coordinates(cls):
    current_kerbin_coordinates = (
      cls.vessel.position(cls.vessel.orbit.body.reference_frame)[2],
      cls.vessel.position(cls.vessel.orbit.body.reference_frame)[0],
    )
    return cls.kerbin_to_launch_coordinates(current_kerbin_coordinates)



# flight_info = vessel.flight()
# vessel.auto_pilot.target_pitch_and_heading(90, 90)
# vessel.auto_pilot.engage()
# vessel.control.throttle=1

# print("Launch!")
# vessel.control.activate_next_stage()

# time.sleep(1)

# while True:
#     current_height = flight_info.mean_altitude
#     vessel.auto_pilot.target_pitch_and_heading(90, 90)
#     vessel.auto_pilot.target_pitch_and_heading(calculate_angle(current_height), 90)

