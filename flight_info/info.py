import krpc
import math

class Info:
  conn = krpc.connect(name='Vessel')
  vessel = conn.space_center.active_vessel
  start_coordinated = (
    vessel.position(vessel.orbit.body.reference_frame)[2],
    vessel.position(vessel.orbit.body.reference_frame)[0],
  )
  rotation_angle = -math.pi - math.atan(start_coordinated[1] / start_coordinated[0])

  rotation_matrix = (
    (math.cos(rotation_angle), -math.sin(rotation_angle)),
    (math.sin(rotation_angle), math.cos(rotation_angle))
  )

  kerbin_radius = start_coordinated[0] * rotation_matrix[0][0] + start_coordinated[1] * rotation_matrix[0][1]

  @classmethod
  def get_kerbin_coordinated(cls):
    return cls.vessel.position(cls.vessel.orbit.body.reference_frame)
  
  @classmethod
  def kerbin_to_launch_coordinated(cls, current_kerbin_coordinated):
    rotated_coordinates = (
      current_kerbin_coordinated[0] * cls.rotation_matrix[0][0] + current_kerbin_coordinated[1] * cls.rotation_matrix[0][1] - cls.kerbin_radius, 
      -current_kerbin_coordinated[0] * cls.rotation_matrix[1][0] - current_kerbin_coordinated[1] * cls.rotation_matrix[1][1], 
    )
    return rotated_coordinates

  @classmethod
  def get_launch_coordinated(cls):
    current_kerbin_coordinated = (
      cls.vessel.position(cls.vessel.orbit.body.reference_frame)[2],
      cls.vessel.position(cls.vessel.orbit.body.reference_frame)[0],
    )
    return cls.kerbin_to_launch_coordinated(current_kerbin_coordinated)

  @classmethod
  def get_r_y(cls):
    return cls.vessel.flight().mean_altitude

  @classmethod
  def info(cls):
    print(cls.start_coordinated)
    print(cls.rotation_angle)
    print(cls.kerbin_radius)
    print(cls.get_launch_coordinated())

  @classmethod
  def get_r_x(cls):
    return 100500



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

