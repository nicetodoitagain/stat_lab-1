# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from PyQt5.QtWidgets import QPushButton,  QTextEdit, QSizePolicy, QGridLayout, QWidget, QMainWindow, QApplication
from PyQt5.QtGui import QFont

import sys
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


class FixedPlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100, default_plot=None, title=None):
        fig = plt.Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Maximum)
        FigureCanvas.updateGeometry(self)
        self.bounds = 0.1
        if default_plot:
            self.default_plot = default_plot #TODO: default plot as a callable
        if title:
            self.axes.set_title(title)

    def update_figure(self, data):
        self.data_set = data
        self.data_set.sort()
        self.axes.clear()

        if self.default_plot:
            self.default_plot(self) # FIXME:
        else:
            raise Exception('Default plot function missing')

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

        self.default_set = default_set

        self.get_button = QPushButton(self.main_widget)
        self.get_button.clicked.connect(self.get_statistic)
        self.get_button.setText('Get')

        self.empiric = FixedPlotCanvas(self.main_widget,
                                       default_plot=FixedPlotCanvas.empiric,
                                       title='Емпірична функція розподілу')
        self.freq_pol_rel = FixedPlotCanvas(self.main_widget,
                                            default_plot=FixedPlotCanvas.freq_pol_relative,
                                            title='Полігон за відносними частотами')
        self.freq_pol = FixedPlotCanvas(self.main_widget,
                                        default_plot=FixedPlotCanvas.freq_pol,
                                        title='Полігон за частотами')
        self.cumulate = FixedPlotCanvas(self.main_widget,
                                        default_plot=FixedPlotCanvas.cumulate,
                                        title='Кумулята за частотами')

        self.cumulate_rel = FixedPlotCanvas(self.main_widget,
                                        default_plot=FixedPlotCanvas.freq_pol,
                                        title='Кумулята за відносними частотами')

        self.output = QTextEdit(self.main_widget)
        self.output.setReadOnly(True)
        self.output.setFont(QFont('times', 15, 75))

        self.setup_layouts()
        self.setCentralWidget(self.main_widget)

    def setup_layouts(self):
        main_grid_layout = QGridLayout(self.main_widget)
        main_grid_layout.setSpacing(6)

        main_grid_layout.addWidget(self.output, 0, 1)
        main_grid_layout.addWidget(self.empiric, 1, 1)
        main_grid_layout.addWidget(self.get_button, 2, 1)

        main_grid_layout.addWidget(self.freq_pol, 0, 0)
        main_grid_layout.addWidget(self.freq_pol_rel, 1, 0)

        main_grid_layout.addWidget(self.cumulate, 0, 3)
        main_grid_layout.addWidget(self.cumulate_rel, 1, 3)

        self.main_widget.setLayout(main_grid_layout)

    def get_statistic(self):

        try:
            stat_data_set = choices(self.default_set, k=15) # first task

            self.freq_pol.update_figure(stat_data_set)
            self.empiric.update_figure(stat_data_set)
            self.cumulate.update_figure(stat_data_set)
            self.cumulate_rel.update_figure(stat_data_set)
            self.freq_pol_rel.update_figure(stat_data_set)
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
