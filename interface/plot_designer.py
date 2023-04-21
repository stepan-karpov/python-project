from interface.window import *

class Plot():
  def __init__(self, title: str, y_name: str, x_name: str, predict_function, monitor_function) -> None:
    """
    this constructor initializes the plot body
    """
    self.predict_function = predict_function
    self.monitor_function = monitor_function

    self.graph_widget = pyqtgraph.PlotWidget()

    self.graph_widget.setTitle(title, color="black", size="10pt")

    styles = {'color':'black', 'font-size':'15px'}
    self.graph_widget.setLabel('left', y_name, **styles)
    self.graph_widget.setLabel('bottom', x_name, **styles)
    self.graph_widget.setBackground('grey')
    self.graph_widget.setBackground('#bbccaa')

    self.graph_widget.showGrid(x=True, y=True)


    self.predict_trajectory_y, self.predict_trajectory_x = self.predict_function()
    pen = pyqtgraph.mkPen(color=(0, 0, 0), width=3)
    self.graph_widget.plot(self.predict_trajectory_y, self.predict_trajectory_x, pen=pen)

    self.real_trajectory_y = []
    self.real_trajectory_x = []

      
  def get_widget(self) -> QWidget:
    """ returns widget of the InfoWidget class instance """
    return self.graph_widget

  def monitor(self) -> None:
    """
    function updates information
    on the screen
    """
    point = self.monitor_function()
    pen = pyqtgraph.mkPen(color=(255, 0, 0), width=1)

    self.real_trajectory_y.append(point[0])
    self.real_trajectory_x.append(point[1])

    self.graph_widget.plot(self.real_trajectory_y, self.real_trajectory_x, pen=pen)
