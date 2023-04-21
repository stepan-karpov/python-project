import krpc
import math

G_CONSTANT = 9.81

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

  @staticmethod
  def get_kerbin_coordinates() -> (float, float, float):
    """
    this function returns kerbin coordinated relatively to Kerbin origin

    you can see it here:
    https://krpc.github.io/krpc/tutorials/reference-frames.html#introduction
    """
    return Info.vessel.position(Info.vessel.orbit.body.reference_frame)
  
  @staticmethod
  def kerbin_to_launch_coordinates(current_kerbin_coordinates) -> (float, float):
    """
    this function transforms kerbin coordinated (from API) to launch system
    """
    rotated_coordinates = (
      -current_kerbin_coordinates[0] * Info.rotation_matrix[1][0] - current_kerbin_coordinates[1] * Info.rotation_matrix[1][1], 
      current_kerbin_coordinates[0] * Info.rotation_matrix[0][0] + current_kerbin_coordinates[1] * Info.rotation_matrix[0][1] - Info.kerbin_radius, 
    )
    return rotated_coordinates

  @staticmethod
  def get_launch_coordinates() -> (float, float):
    """
    returns coordinates in launch system
    """
    current_kerbin_coordinates = (
      Info.vessel.position(Info.vessel.orbit.body.reference_frame)[2],
      Info.vessel.position(Info.vessel.orbit.body.reference_frame)[0],
    )
    return Info.kerbin_to_launch_coordinates(current_kerbin_coordinates)
  
  @staticmethod
  def get_mass():
    return Info.vessel.mass

  @staticmethod
  def get_thrust():
    return Info.vessel.thrust

  @staticmethod
  def get_g():
    rel = (Info.get_launch_coordinates()[1] + Info.kerbin_radius) / Info.kerbin_radius
    rel = math.pow(rel, 2)
    return rel * G_CONSTANT
  
  @staticmethod
  def get_speed():
    return Info.vessel.flight(Info.vessel.orbit.body.reference_frame).speed

  @staticmethod
  def get_pressure():
    return Info.vessel.flight().static_pressure

  @staticmethod
  def get_ttw():
    return Info.vessel.flight().g_force

  @staticmethod
  def get_height():
    return Info.get_launch_coordinates()[1]

  @staticmethod
  def get_ttw_coordinates():
    return (Info.get_launch_coordinates()[1], Info.vessel.flight().g_force)

  @staticmethod
  def get_launch_velocity():
    kerbin_velocity = Info.vessel.velocity(Info.vessel.orbit.body.reference_frame)

    launch_velocity = (
      kerbin_velocity[0] * Info.rotation_matrix[1][0] + kerbin_velocity[2] * Info.rotation_matrix[1][1], 
      kerbin_velocity[0] * Info.rotation_matrix[0][0] + kerbin_velocity[2] * Info.rotation_matrix[0][1], 

    )
    return launch_velocity

  @staticmethod
  def get_fuel():
    return Info.vessel.resources.amount('LiquidFuel')

  @staticmethod
  def get_monofuel():
    return Info.vessel.resources.amount('MonoFuel')

