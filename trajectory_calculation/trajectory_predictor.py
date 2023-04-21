import math
from trajectory_calculation.trajectory_constants import *

class Trajectory:
  is_calculated = False
  """
  trajectory configuration
  all of the following calculation based on the fact that we're
  approximate rocket's trajectory by formula

  r_y(r_x) = (r_x/l)^p1 * l

  and the vessel stops it's engine at the h_end, waiting for the apoapsis to reach

  """
  # trajectory by itself
  p1 = 0.8
  h_end = 40000
  h_ap = 70000
  l = 30000
  l_end = int(math.pow(h_end / h_ap, 1 / p1) * l)
  
  # speed of the vessel configurations
  p2 = 0.4
  v_vend = 500
  v_hend = 500

  @staticmethod
  def calculate_trajectory() -> None:
    """
    main calculations should be here
    """
    Trajectory.is_calculated = True

  @staticmethod
  def r_y(r_x: float) -> float:
    """
    function returns r_y(r_x)
    """
    Trajectory.check()
    return math.pow(r_x / Trajectory.l, Trajectory.p1) * Trajectory.h_ap
  
  @staticmethod
  def check() -> None:
    """
    help-function to determine whether the calculations were done or not
    """
    if (not Trajectory.is_calculated):
      Trajectory.calculate_trajectory()

  @staticmethod
  def get_r_y_r_x() -> (list, list):
    """
    function returns a whole trajectory as a pair of lists,
    where the first list is r_x, the second is r_y
    you can set splitting value (H_PLOT_STEP) in constants
    """
    Trajectory.check()
    r_y = []
    r_x = []
    for i in range(0, Trajectory.l_end, H_PLOT_STEP):
      r_y.append(Trajectory.r_y(i))
      r_x.append(i)
    return (r_x, r_y)

  @staticmethod
  def ttw(r_x: float) -> float:
    """
    function returns ttw(r_x)

    p.s. r_x in unused yet
    """
    Trajectory.check()
    return 1.1

  @staticmethod
  def get_ttw_r_y() -> (list, list):
    """
    function returns a ttw(r_y) as a pair of lists,
    where the first list is r_y, the second is ttw
    you can set splitting value (H_PLOT_STEP) in constants
    """
    Trajectory.check()
    ttw = []
    r_y = []
    for i in range(0, Trajectory.l_end, H_PLOT_STEP):
      ttw.append(Trajectory.ttw(i))
      r_y.append(i)
    return (r_y, ttw)

  @staticmethod
  def v_x(r_y: float) -> float:
    return math.pow(r_y / Trajectory.h_end, 1 / Trajectory.p2) * Trajectory.v_hend

  @staticmethod
  def get_v_x_r_y() -> (list, list):
    """
    function returns a v_x(r_y) as a pair of lists,
    where the first list is r_y, the second is v_x
    you can set splitting value (H_PLOT_STEP) in constants
    """
    Trajectory.check()
    v_x = []
    r_y = []
    for i in range(0, Trajectory.l_end, H_PLOT_STEP):
      v_x.append(Trajectory.v_x(i))
      r_y.append(i)
    return (r_y, v_x)

  @staticmethod
  def v_y(r_y: float) -> float:
    return math.pow(r_y / Trajectory.h_end, Trajectory.p2) * Trajectory.v_vend

  @staticmethod
  def get_v_y_r_y() -> (list, list):
    """
    function returns a v_y(r_y) as a pair of lists,
    where the first list is r_y, the second is v_y
    you can set splitting value (H_PLOT_STEP) in constants
    """
    Trajectory.check()
    v_y = []
    r_y = []
    for i in range(0, Trajectory.l_end, H_PLOT_STEP):
      v_y.append(Trajectory.v_y(i))
      r_y.append(i)
    return (r_y, v_y)
