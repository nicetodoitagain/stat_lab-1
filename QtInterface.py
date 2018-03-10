# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Borys1\Documents\StatisticLabs\mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

#TODO: Додати графіки

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QPushButton, QScrollArea, QTableWidget, QDoubleSpinBox, QTextEdit
from PyQt5.QtWidgets import QSizePolicy, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QWidget,QMainWindow,QApplication

import sys
import Lab1
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib import pyplot as plt


class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = plt.Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.compute_initial_figure()

        #
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class FrequencePoligon(MyMplCanvas):
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)

    def compute_initial_figure(self):
        self.axes.plot([0,1,2,3],[1,2,0,4],'r')

    def update_figure(self):
        self.axes.clear()
        self.axes.plot([i for i in range(4)])
        self.draw()





def table_as_list(q_table: QTableWidget):
    data_set = []
    for i in range(0, q_table.rowCount()):
        data = q_table.item(i, 0)
        if data or data.text(): #TODO: ввід не працює норм
            data_set.append(float(data.text()))
    return data_set

class ApplicationWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("1 task SMDA")
        self.resize(778, 420)

        self.main_widget = QWidget(self)
        main_h_layout = QHBoxLayout(self.main_widget)
        main_h_layout.setSpacing(6)

        self.data = QTableWidget(self.main_widget)
        sizePolicy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.data.sizePolicy().hasHeightForWidth())
        self.data.setSizePolicy(sizePolicy)
        self.data.setInputMethodHints(QtCore.Qt.ImhFormattedNumbersOnly)
        self.data.setRowCount(5)
        self.data.setColumnCount(1)

        self.row_count = QDoubleSpinBox(self.main_widget)
        self.row_count.setDecimals(0)
        self.row_count.setRange(5.0, 100.0)
        self.row_count.setProperty('value', 1.0)
        self.row_count.valueChanged.connect(self.row_count_change)

        self.clear_button = QPushButton(self.main_widget)
        self.clear_button.setText('Clear')
        self.clear_button.clicked.connect(self.data.clear)
        self.get_button = QPushButton(self.main_widget)
        self.get_button.clicked.connect(self.get_statistic)
        self.get_button.setText('Get')
        #  def retranslate_ui(self, main_window):
        # _translate = QtCore.QCoreApplication.translate
        # main_window.setWindowTitle(_translate("MainWindow", "Statistic"))
        # self.clear_btn.setText(_translate("MainWindow", "Clear"))
        # self.get_btn.setText(_translate("MainWindow", "Get Data"))
        #

        tsize_layout = QHBoxLayout(self.main_widget)
        tsize_layout.addWidget(self.row_count)
        tsize_layout.addWidget(self.clear_button)

        data_layout = QVBoxLayout(self.main_widget)
        data_layout.addWidget(self.data)
        data_layout.addLayout(tsize_layout)
        data_layout.addWidget(self.get_button)
        main_h_layout.addLayout(data_layout)

        scroll_layout = QVBoxLayout(self.main_widget)
        self.poligon = FrequencePoligon(self.main_widget)

        self.get_button.clicked.connect(self.poligon.update_figure)

        self.poligon1 = FrequencePoligon(self.main_widget)
        self.poligon2 = FrequencePoligon(self.main_widget)
       # self.poligon.
        scroll_layout.addWidget(self.poligon)
        scroll_layout.addWidget(self.poligon1)
        scroll_layout.addWidget(self.poligon2)

        plots_scroll = QScrollArea(self.main_widget)
        plots_scroll.setLayout(scroll_layout)
        main_h_layout.addWidget(plots_scroll)

        self.output = QTextEdit(self.main_widget)
        self.output.setReadOnly(True)
        main_h_layout.addWidget(self.output)

        self.setCentralWidget(self.main_widget)

    def row_count_change(self):
        self.data_table.setRowCount(self.row_count.value())

    def get_statistic(self):
        try:
            stat_data_set = table_as_list(self.data)
            if len(stat_data_set) < 2:
                raise IOError('Not enough data')

            self.output.setText(str(Lab1.get_data_set(stat_data_set)))
        except Exception as error:
            self.output.setText(error.args[0])



app = QApplication(sys.argv)

w = ApplicationWindow()

w.show()

sys.exit(app.exec_())
