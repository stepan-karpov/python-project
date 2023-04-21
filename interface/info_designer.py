from interface.window import *

class InfoWidget():
  def __init__(self, flight_data, vessel_data):
    text_layout = QHBoxLayout()

    text_layout.addWidget(self.create_flight_info_widget('grey', flight_data, "fligh data"))
    text_layout.addWidget(self.create_vessel_data_widget('grey', vessel_data, "vessel data"))
    self.control_widget = QWidget()
    self.control_widget.setLayout(text_layout)

  def create_flight_info_widget(self, color, data, header):
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

    self.flight_info_labels = []

    for name, value in data.items():
      info = (QLabel(str(name) + ": " + str(value[0])), name, value[1])
      self.flight_info_labels.append(info)
      self.flight_info_labels[-1][0].setFont(QFont("Sanserif", 10))
      layout.addWidget(self.flight_info_labels[-1][0])

    self.info_widget.setLayout(layout)

    return self.info_widget

  def create_vessel_data_widget(self, color, data, header):
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

    self.vessel_info_labels = []

    for name, value in data.items():
      info = (QLabel(str(name) + ": " + str(value[0])), name, value[1])
      self.vessel_info_labels.append(info)
      self.vessel_info_labels[-1][0].setFont(QFont("Sanserif", 10))
      layout.addWidget(self.vessel_info_labels[-1][0])

    self.info_widget.setLayout(layout)

    return self.info_widget

  def get_widget(self):
    return self.control_widget

  def monitor(self):
    for label in self.vessel_info_labels:
      value = label[2]()
      if (value < 0.001):
        value = 1
      value = round(value, 2)
      label[0].setText(str(label[1]) + ": " + str(value))

    for label in self.flight_info_labels:
      value = label[2]()
      if (value < 0.001):
        value = 1
      value = round(value, 2)
      label[0].setText(str(label[1]) + ": " + str(value))