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
  def get_mass() -> float:
    """ returns mass of the vessel """
    return Info.vessel.mass

  @staticmethod
  def get_thrust() -> float:
    """ returns thrust of the vessels (Nextons) """
    return Info.vessel.thrust

  @staticmethod
  def get_g() -> float:
    """ returns g in the current height """
    rel = (Info.get_launch_coordinates()[1] + Info.kerbin_radius) / Info.kerbin_radius
    rel = math.pow(rel, -2)
    return rel * G_CONSTANT
  
  @staticmethod
  def get_speed() -> float:
    """ returns speed of the vessel relatively to the origin """
    return Info.vessel.flight(Info.vessel.orbit.body.reference_frame).speed

  @staticmethod
  def get_pressure() -> float:
    """ returns pressure at the current height """
    return Info.vessel.flight().static_pressure

  @staticmethod
  def get_ttw() -> float:
    """ returns ttw on the current moment """
    return Info.vessel.flight().g_force

  @staticmethod
  def get_height() -> float:
    """ returns current height """
    return Info.get_launch_coordinates()[1]

  @staticmethod
  def get_ttw_coordinates() -> (float, float):
    """ returns pair (height, ttw) for plot drawing """
    return (Info.get_launch_coordinates()[1], Info.vessel.flight().g_force)

  @staticmethod
  def get_launch_velocity() -> float:
    """ returns launch velocity in launch system coordinates """
    kerbin_velocity = Info.vessel.velocity(Info.vessel.orbit.body.reference_frame)

    launch_velocity = (
      kerbin_velocity[0] * Info.rotation_matrix[1][0] + kerbin_velocity[2] * Info.rotation_matrix[1][1], 
      kerbin_velocity[0] * Info.rotation_matrix[0][0] + kerbin_velocity[2] * Info.rotation_matrix[0][1], 

    )
    return launch_velocity

  @staticmethod
  def get_fuel() -> float:
    """ returns amount of liquid fuel left in kg """
    return Info.vessel.resources.amount('LiquidFuel')

  @staticmethod
  def get_monofuel() -> float:
    """ returns amount of monofuel left in kg """
    return Info.vessel.resources.amount('MonoFuel')

  @staticmethod
  def get_vertical_speed() -> float:
    """ returns vertical speed relatively to the surface of the orbit body """
    return Info.vessel.flight(Info.vessel.orbit.body.reference_frame).vertical_speed

  @staticmethod
  def get_horizontal_speed() -> float:
    """ returns horizontal speed relatively to the surface of the orbit body """
    return Info.vessel.flight(Info.vessel.orbit.body.reference_frame).horizontal_speed

  @staticmethod
  def get_vertical_speed_coordinates() -> (float, float):
    """ returns pair (height, vertical_speed) for plot drawing """
    return (Info.get_launch_coordinates()[1],  Info.get_vertical_speed())
  
  @staticmethod
  def get_horizontal_speed_coordinates() -> (float, float):
    """ returns pair (height, horizontal_speed) for plot drawing """
    return (Info.get_launch_coordinates()[1],  Info.get_horizontal_speed())
