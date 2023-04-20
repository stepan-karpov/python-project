import math
from trajectory_calculation.trajectory_constants import *

class Trajectory:
  is_calculated = False
  # trajectory configuration
  p1 = 0.325
  h_end = 40000
  h_ap = 70000
  L = 30000
  h_end = math.pow(h_end / h_ap, 1 / p1) * L
  
  # velocity configuration
  # v_end = 600

  @classmethod
  def calculate_trajectory(cls):
    cls.is_calculated = True

  @classmethod
  def r_y(cls, r_x):
    cls.check()
    return math.pow(r_x / cls.L, cls.p1) * cls.h_ap
  
  @classmethod
  def check(cls):
    if (not cls.is_calculated):
      cls.calculate_trajectory()
    
  @classmethod
  def get_r_y_r_x(cls):
    cls.check()
    r_y = []
    r_x = []
    for i in range(0, cls.L, H_PLOT_STEP):
      r_y.append(cls.r_y(i))
      r_x.append(i)
    return r_x, r_y


