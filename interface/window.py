import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
import pyqtgraph
from interface.interface_constants import *
from interface.trajectory_calculation_constants import *


class Plot():
  def __init__(self, title, y_name, x_name):
    self.graph_widget = pyqtgraph.PlotWidget()

    hour = [1,2,3,4,5,6,7,8,9,10]
    temperature = [30,32,34,32,33,31,29,32,35,45]

    self.graph_widget.setTitle(title, color="black", size="10pt")

    styles = {'color':'black', 'font-size':'15px'}
    self.graph_widget.setLabel('left', y_name, **styles)
    self.graph_widget.setLabel('bottom', x_name, **styles)
    self.graph_widget.setBackground('white')
    self.graph_widget.setBackground('#bbccaa')

    pen = pyqtgraph.mkPen(color=(0, 0, 0), width=5)
    self.graph_widget.plot(hour, temperature, pen=pen)

    self.graph_widget.showGrid(x=True, y=True)
    self.graph_widget.plot(hour, temperature)

  def get_widget(self):
    return self.graph_widget

class InfoWidget():
  def __init__(self, flight_data, vessel_data):
    text_layout = QHBoxLayout()
    text_layout.addWidget(self.get_info_widget('grey', flight_data))
    text_layout.addWidget(self.get_info_widget('grey', vessel_data))
    self.control_widget = QWidget()
    self.control_widget.setLayout(text_layout)


  def get_info_widget(self, color, data: dict):
    self.info_widget = QWidget()
    self.info_widget.setAutoFillBackground(True)

    palette = self.info_widget.palette()
    palette.setColor(QPalette.Window, QColor(color))
    self.info_widget.setPalette(palette)

    layout = QVBoxLayout()

    for name, value in data.items():
      object = QLabel(str(name) + ": " + str(value))
      layout.addWidget(object)

    self.info_widget.setLayout(layout)

    return self.info_widget

  def get_widget(self):
    return self.control_widget

class StartButton():
  def __init__(self):
    self.start_button = QPushButton('Launch vessel!')
    self.start_button.setStyleSheet("background-color : green")
    self.start_button.clicked.connect(self.on_click)
  
  def get_widget(self):
    return self.start_button

  def on_click(self):
    print("clicked")
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
  
  def start_application(self):
    self.show()

    sys.exit(self.app.exec())



