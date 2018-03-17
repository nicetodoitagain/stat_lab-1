# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Borys1\Documents\StatisticLabs\mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

# TODO: Додати графіки

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QPushButton, QScrollArea, QTableWidget, QDoubleSpinBox, QTextEdit
from PyQt5.QtWidgets import QSizePolicy, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication, QTableWidgetItem

import sys
import Lab1

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib import pyplot as plt

from numpy import arange
from numpy import unique

data_set1 = arange(-4.9, -3, 0.1)


def table_as_list(q_table: QTableWidget):
    return [
        float(data.text()) for data in
        map(lambda i: q_table.item(i, 0), range(q_table.rowCount()))
        if data or data.text
    ]


class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = plt.Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Maximum)
        FigureCanvas.updateGeometry(self)
        self.bounds = 0.1
        self.data_set = None
        self.unique = set()
        self.axes.set_xticks(arange(-10, 10, self.bounds))

    def update_figure(self, data, plot_type):

        if data == self.data_set:
            return
        self.data_set = data
        self.data_set.sort()
        self.axes.clear()
        data.sort()

        if plot_type == 'empiric':
            self.empiric()
        elif plot_type == 'freq_pol':
            self.freq_pol()
        elif plot_type == 'cumulate':
            self.cumulate()

        self.axes.draw(renderer=None)

    def freq_pol(self):

        spread = (self.data_set[0] - self.bounds, self.data_set[-1] + self.bounds, self.bounds)

        self.axes.plot(unique(self.data_set+[spread[0], spread[1]]),
                       [self.data_set.count(i) for i in unique(self.data_set+[spread[0], spread[1]])],
                       "r")

    def empiric(self):
        probability = 1.0 / len(self.data_set)
        emp_args = []
        last_grow = self.data_set[0] - self.bounds
        increase = float(0)  # звідки починати малювати графік
        for i, j in map(lambda l: (self.data_set.count(l), l),
                        unique(self.data_set +
                               [self.data_set[0] - self.bounds, self.data_set[-1]+self.bounds])):
            if i:
                emp_args.extend(([last_grow, j], [increase, increase], 'g',
                                 [j, j], [increase, increase + probability * i], 'r--'))
                increase += probability * i
                last_grow = j

        emp_args.extend(([last_grow, last_grow + self.bounds], [1, 1], 'g'))
        self.axes.plot(*emp_args)

    def cumulate(self):
        x = [self.data_set[0] - self.bounds]
        y = [0]
        for i, j in map(
                        lambda l:
                        (self.data_set.count(l), l),
                        unique(self.data_set +
                               [self.data_set[0] - self.bounds,
                                self.data_set[-1] + self.bounds]
                               )
                        ):
            if i:
                x.append(j)
                y.append(y[-1] + i)
        self.axes.plot(x, y, 'b')


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
        self.data.setRowCount(15)
        self.set_default_data_set()
        self.data.setColumnCount(1)

        self.row_count = QDoubleSpinBox(self.main_widget)
        self.row_count.setDecimals(0)
        self.row_count.setRange(15.0, 100.0)
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
        self.poligon = MyMplCanvas(self.main_widget)
        self.empiric = MyMplCanvas(self.main_widget)
        self.cumulate = MyMplCanvas(self.main_widget)

        scroll_layout.addWidget(self.poligon)
        scroll_layout.addWidget(self.empiric)
        scroll_layout.addWidget(self.cumulate)

        plots_scroll = QScrollArea(self.main_widget)
        plots_scroll.setLayout(scroll_layout)
        main_h_layout.addWidget(plots_scroll)

        self.output = QTextEdit(self.main_widget)
        self.output.setReadOnly(True)
        main_h_layout.addWidget(self.output)

        self.setCentralWidget(self.main_widget)

    def set_default_data_set(self):
        for i in range(self.data.rowCount()):
            item = QTableWidgetItem()
            item.setText(str(data_set1[i]))
            self.data.setItem(i, 0, item)

    def row_count_change(self):
        self.data.setRowCount(self.row_count.value())

    def get_statistic(self):
        try:
            stat_data_set = table_as_list(self.data)
            if len(stat_data_set) < 2:
                raise IOError('Not enough data')
            self.poligon.update_figure(stat_data_set, 'freq_pol')
            self.empiric.update_figure(stat_data_set, 'empiric')
            self.cumulate.update_figure(stat_data_set, 'cumulate')
            self.output.setText(str(Lab1.get_data_set(stat_data_set)))

        except Exception as error:
            self.output.setText(error.args[0])


app = QApplication(sys.argv)

w = ApplicationWindow()

w.show()

sys.exit(app.exec_())
