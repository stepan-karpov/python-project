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
  def get_ttw():
    return Info.vessel.flight().g_force

  @staticmethod
  def get_ttw_coordinates():
    return (Info.get_launch_coordinates()[1], Info.vessel.flight().g_force)
