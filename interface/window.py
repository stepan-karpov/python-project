import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt, QTimer
import pyqtgraph
from interface.interface_constants import *
from interface.trajectory_calculation_constants import *
from flight_info.info import Info
from trajectory_calculation.trajectory_predictor import Trajectory


class Plot():
  def __init__(self, title, y_name, x_name):
    self.graph_widget = pyqtgraph.PlotWidget()

    self.graph_widget.setTitle(title, color="black", size="10pt")

    styles = {'color':'black', 'font-size':'15px'}
    self.graph_widget.setLabel('left', y_name, **styles)
    self.graph_widget.setLabel('bottom', x_name, **styles)
    self.graph_widget.setBackground('grey')
    self.graph_widget.setBackground('#bbccaa')

    self.graph_widget.showGrid(x=True, y=True)



    self.predict_trajectory_y, self.predict_trajectory_x = Trajectory.get_r_y_r_x()
    pen = pyqtgraph.mkPen(color=(0, 0, 0), width=3)
    self.graph_widget.plot(self.predict_trajectory_y, self.predict_trajectory_x, pen=pen)

    self.real_trajectory_y = []
    self.real_trajectory_x = []

      
  def get_widget(self):
    return self.graph_widget

  def add_predict_point(self, point):
    pen = pyqtgraph.mkPen(color=(0, 0, 0), width=3)

    self.real_trajectory_y.append(point[0])
    self.real_trajectory_x.append(point[1])

    # self.graph_widget.clear()
    self.graph_widget.plot(self.real_trajectory_y, self.real_trajectory_x, pen=pen)


class InfoWidget():
  def __init__(self, flight_data, vessel_data):
    text_layout = QHBoxLayout()
    text_layout.addWidget(self.get_info_widget('grey', flight_data, "fligh data"))
    text_layout.addWidget(self.get_info_widget('grey', vessel_data, "vessel data"))
    self.control_widget = QWidget()
    self.control_widget.setLayout(text_layout)


  def get_info_widget(self, color, data: dict, header):
    self.info_widget = QWidget()
    self.info_widget.setAutoFillBackground(True)

    palette = self.info_widget.palette()
    palette.setColor(QPalette.Window, QColor(color))
    self.info_widget.setPalette(palette)

    layout = QVBoxLayout()
    
    header_box = QHBoxLayout()

    header_label = QLabel("")
    header_label2 = QLabel(header)
    header_label2.setFont(QFont("Sanserif", 12))
    header_box.addWidget(header_label, stretch=1)
    header_box.addWidget(header_label2, stretch=2)

    layout.addLayout(header_box)

    for name, value in data.items():
      object = QLabel(str(name) + ": " + str(value))
      object.setFont(QFont("Sanserif", 10))
      layout.addWidget(object)

    self.info_widget.setLayout(layout)

    return self.info_widget

  def get_widget(self):
    return self.control_widget

class StartButton():
  def __init__(self):
    self.in_flight = False
    self.start_button = QPushButton('Launch vessel!')
    self.start_button.setStyleSheet("background-color : green")
    self.start_button.clicked.connect(self.on_click)
  
  def get_widget(self):
    return self.start_button

  def on_click(self):
    if (self.in_flight):
      sys.exit()

    self.in_flight = True
    self.start_button.setText("Launched!")
    self.start_button.setStyleSheet("background-color : red")

class MainWindow(QMainWindow):
  def scroll_widget(self):
    layout = QGridLayout()

    self.trajectory_plot = Plot("trajectory plot", "r_y, m", "r_x, m")
    self.ttw_plot = Plot("ttw plot", "ttw", "r_y, m")
    self.hvelocity_plot = Plot("horizontal velocity plot", "v_h. m/s", "r_y, m")
    self.vvelocity_plot = Plot("vertical velocity plot", "v_v, m/s", "r_y, m")

    layout.addWidget(self.trajectory_plot.get_widget(), 0, 0)
    layout.addWidget(self.ttw_plot.get_widget(), 1, 0)
    layout.addWidget(self.hvelocity_plot.get_widget(), 2, 0)
    layout.addWidget(self.vvelocity_plot.get_widget(), 3, 0)

    w = QWidget()
    w.setLayout(layout)

    w.resize(self.width - SCROLLBAR_WIDTH_SHIFT, SCROLLBAR_HEIGHT)

    scroll = QScrollArea()
    scroll.setWidget(w)
    scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
    scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    return scroll

  def update_state(self):
    if (not self.start_button.in_flight):
      return

    self.trajectory_plot.add_predict_point((Info.get_r_x(), Info.get_r_y()))

    print("hey")

  def __init__(self):
    self.app = QApplication(sys.argv)
    super(MainWindow, self).__init__()

    self.setWindowTitle("KSP Launcher")
    screen = self.app.primaryScreen()
    size = screen.size()

    self.width = WIDTH
    self.height = size.height() - HEIGHT_SHIFT

    self.setGeometry(size.width() - self.width, FRAME_SHIFT, self.width, self.height)
    self.setFixedHeight(self.height)
    self.setFixedWidth(self.width)

    self.info = InfoWidget(INIT_FLIGH_DATA, INIT_VESSEL_DATA)
    self.start_button = StartButton()

    layout = QVBoxLayout()

    layout.addWidget(self.info.get_widget(), stretch=2)
    layout.addWidget(self.scroll_widget(), stretch=8)
    layout.addWidget(self.start_button.get_widget(), stretch=2)

    box = QGroupBox(self)
    box.setLayout(layout)

    self.setCentralWidget(box)
    
    self.timer = QTimer()
    self.timer.setInterval(1000)
    self.timer.timeout.connect(self.update_state)
    self.timer.start()

  def start_application(self):
    self.show()
    sys.exit(self.app.exec())



