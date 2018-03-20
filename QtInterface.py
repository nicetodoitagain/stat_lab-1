# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Borys1\Documents\StatisticLabs\mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QPushButton, QScrollArea, QTableWidget, QDoubleSpinBox, QTextEdit
from PyQt5.QtWidgets import QSizePolicy, QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication, QTableWidgetItem

import sys
from threading import Timer
import Lab1

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib import pyplot as plt

from numpy import arange
from numpy import unique
from random import choices

data_set1 = [-5, -4.9, -4.8, -4.7, -4.6, -4.5, -4.4, -4.3, -4.2, -4.1, -4.0, -3.8, -3.8, -3.6, -3.4, -3.2, -3.0, -2.9,
             -2.8, -2.7, -2.6, -2.5, -2.4, -2.3, -2.2, -2.1, -2.0, -1.9, -1.7, -1.5, -1.5, -1.3, -1.1, -1.1, -1.0, -0.6,
             -0.6, -0.6, -0.6, -0.4, -0.4, -0.4, -0.4, -0.2, -0.2, -0.2, -0.2, -0.2, -0.2, 0, 0.2, 0.2, 0.2, 0.2, 0.2,
             0.4, 0.4, 0.4, 0.4, 0.6, 0.6, 0.6, 1.0, 1.1, 1.1, 1.3, 1.5, 1.5, 1.7, 1.9, 2.0, 2.2, 2.4, 2.6, 2.8, 2.8,
             3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 4.9,
             4.9, 5]



def table_to_list(q_table: QTableWidget):
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

        self.data_set = data
        self.data_set.sort()
        self.axes.clear()
        if plot_type == 'empiric':
            self.empiric()
        elif plot_type == 'freq_pol':
            self.freq_pol()
        elif plot_type == 'cumulate':
            self.cumulate()
        elif plot_type == 'cumulate_relative':
            self.cumulate_relative()
        elif plot_type == 'freq_pol_relative':
            self.freq_pol_relative()
        self.axes.draw(renderer=None)

    def freq_pol(self):

        spread = (self.data_set[0] - self.bounds, self.data_set[-1] + self.bounds, self.bounds)

        self.axes.plot(unique(self.data_set + [spread[0], spread[1]]),
                       [self.data_set.count(i) for i in unique(self.data_set + [spread[0], spread[1]])],
                       "r")

    def empiric(self):
        probability = 1.0 / len(self.data_set)
        emp_args = []
        last_grow = self.data_set[0] - self.bounds
        increase = float(0)  # звідки починати малювати графік
        for i, j in map(lambda l: (self.data_set.count(l), l),
                        unique(self.data_set +
                                       [self.data_set[0] - self.bounds, self.data_set[-1] + self.bounds])):
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

    def cumulate_relative(self):
        x = [self.data_set[0] - self.bounds]
        y = [0.0]
        possibility = 1 / len(self.data_set)
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
                y.append(y[-1] + i * possibility)
        self.axes.plot(x, y, 'b')

    def freq_pol_relative(self):
        spread = (self.data_set[0] - self.bounds, self.data_set[-1] + self.bounds, self.bounds)
        possibility = 1 / len(self.data_set)
        self.axes.plot(unique(self.data_set + [spread[0], spread[1]]),
                       [self.data_set.count(i) * possibility for i in unique(self.data_set + [spread[0], spread[1]])],
                       "r")


class ApplicationWindow(QMainWindow):
    def __init__(self, default_set = None):
        QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("1 task SMDA")

        self.main_widget = QWidget(self)

        self.data = QTableWidget(self.main_widget)
        self.setup_data_table()

        if default_set:
            self.default_set = default_set
        self.row_count = QDoubleSpinBox(self.main_widget)
        self.setup_row_count()

        self.clear_button = QPushButton(self.main_widget)
        self.clear_button.setText('Clear')
        self.clear_button.clicked.connect(self.data.clear)
        self.get_button = QPushButton(self.main_widget)
        self.get_button.clicked.connect(self.get_statistic)
        self.get_button.setText('Get')

        self.poligon = MyMplCanvas(self.main_widget)
        self.empiric = MyMplCanvas(self.main_widget)
        self.cumulate = MyMplCanvas(self.main_widget)

        self.output = QTextEdit(self.main_widget)
        self.output.setReadOnly(True)

        self.freq_pol_rel = MyMplCanvas(self.main_widget)
        self.cumulate_rel = MyMplCanvas(self.main_widget)

        self.setup_layouts()
        self.setCentralWidget(self.main_widget)

    def setup_data_table(self):
        size_policy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.data.sizePolicy().hasHeightForWidth())
        self.data.setSizePolicy(size_policy)
        self.data.setRowCount(15)
        self.data.setInputMethodHints(QtCore.Qt.ImhFormattedNumbersOnly)
        self.data.setColumnCount(1)

    def setup_row_count(self):
        self.row_count.setDecimals(0)
        self.row_count.setRange(15.0, 100.0)
        self.row_count.setProperty('value', 1.0)
        self.row_count.valueChanged.connect(self.row_count_change)

    def setup_layouts(self):
        main_h_layout = QHBoxLayout(self.main_widget)
        main_h_layout.setSpacing(6)

        table_size_setter_layout = QHBoxLayout(self.main_widget)
        table_size_setter_layout.addWidget(self.row_count)
        table_size_setter_layout.addWidget(self.clear_button)

        data_layout = QVBoxLayout(self.main_widget)
        data_layout.addWidget(self.data)
        data_layout.addLayout(table_size_setter_layout)
        data_layout.addWidget(self.get_button)
        main_h_layout.addLayout(data_layout)

        scroll_layout = QVBoxLayout(self.main_widget)
        scroll_layout.addWidget(self.poligon)
        scroll_layout.addWidget(self.empiric)
        scroll_layout.addWidget(self.cumulate)

        plots_scroll = QScrollArea(self.main_widget)
        plots_scroll.setLayout(scroll_layout)
        main_h_layout.addWidget(plots_scroll)

        l_layout = QVBoxLayout(self.main_widget)
        l_layout.addWidget(self.output)
        l_layout.addWidget(self.freq_pol_rel)
        l_layout.addWidget(self.cumulate_rel)

        main_h_layout.addLayout(l_layout)
        self.main_widget.setLayout(main_h_layout)

    def row_count_change(self):
        self.data.setRowCount(self.row_count.value())

    def get_statistic(self):

        try:
            if not self.data.item(0, 0):
                stat_data_set = choices(self.default_set, k=15) # first task
            else:
                stat_data_set = table_to_list(self.data)

            if len(stat_data_set) < 2:
                raise IOError('Not enough data')
            self.poligon.update_figure(stat_data_set, 'freq_pol')
            self.empiric.update_figure(stat_data_set, 'empiric')
            self.cumulate.update_figure(stat_data_set, 'cumulate')
            self.cumulate_rel.update_figure(stat_data_set, 'cumulate_relative')
            self.freq_pol_rel.update_figure(stat_data_set, 'freq_pol_relative')
            self.output.setText(str(Lab1.get_data_set(stat_data_set)))
            self.update()
            self.updateGeometry()
        except Exception as error:
            self.output.setText(error.args[0])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = ApplicationWindow(default_set=data_set1)
    w.showMaximized()
    w.show()
    sys.exit(app.exec_())
