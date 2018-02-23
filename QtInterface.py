# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Borys1\Documents\StatisticLabs\mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

#TODO: Додати графіки

from PyQt5 import QtCore, QtGui, QtWidgets

import sys
import Lab1


def table_as_list(q_table: QtWidgets.QTableWidget):
    data_set = []
    for i in range(0, q_table.rowCount()):
        data = q_table.item(i, 0)
        if data or data.text(): #TODO: ввід не працює норм
            data_set.append(float(data.text()))
    return data_set


class UiMainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(778, 420)
        self.main_window = QtWidgets.QWidget(MainWindow)
        self.main_window.setObjectName("main_window")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.main_window)
        self.horizontalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.data_table = QtWidgets.QTableWidget(self.main_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.data_table.sizePolicy().hasHeightForWidth())
        self.data_table.setSizePolicy(sizePolicy)
        self.data_table.setBaseSize(QtCore.QSize(120, 400))
        self.data_table.setInputMethodHints(QtCore.Qt.ImhFormattedNumbersOnly)
        self.data_table.setRowCount(2)
        self.data_table.setColumnCount(1)
        self.data_table.setObjectName("data_table")

        self.verticalLayout.addWidget(self.data_table)
        self.data_ctrl_layout = QtWidgets.QHBoxLayout()
        self.data_ctrl_layout.setSpacing(6)
        self.data_ctrl_layout.setObjectName("data_ctrl_layout")
        self.row_count = QtWidgets.QDoubleSpinBox(self.main_window)
        self.row_count.setDecimals(0)
        self.row_count.setMinimum(2.0)
        self.row_count.setProperty("value", 1.0)
        self.row_count.setObjectName("row_count")
        self.data_ctrl_layout.addWidget(self.row_count)
        self.row_count.valueChanged.connect(self.row_count_change)

        self.clear_btn = QtWidgets.QPushButton(self.main_window)
        self.clear_btn.setObjectName("clear_btn")
        self.data_ctrl_layout.addWidget(self.clear_btn)
        self.verticalLayout.addLayout(self.data_ctrl_layout)
        self.get_btn = QtWidgets.QPushButton(self.main_window)
        self.get_btn.setObjectName("get_btn")
        self.get_btn.clicked.connect(self.get_data_clk)

        self.verticalLayout.addWidget(self.get_btn)
        self.horizontalLayout.addLayout(self.verticalLayout)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.output = QtWidgets.QTextEdit(self.main_window)
        self.output.setReadOnly(True)
        self.output.setObjectName("output")
        self.horizontalLayout.addWidget(self.output)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.main_window)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 778, 21))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslate_ui(MainWindow)
        self.clear_btn.clicked.connect(self.data_table.clear)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslate_ui(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("MainWindow", "Statistic"))
        self.clear_btn.setText(_translate("MainWindow", "Clear"))
        self.get_btn.setText(_translate("MainWindow", "Get Data"))

    def row_count_change(self):
        self.data_table.setRowCount(self.row_count.value())

    def get_data_clk(self):
        try:
            stat_data_set = table_as_list(self.data_table)
            if len(stat_data_set) < 2:
                raise IOError('Not enough data')

            self.output.setText(str(Lab1.get_data_set(stat_data_set)))
        except Exception as error:
            self.output.setText(error.args[0])

app = QtWidgets.QApplication(sys.argv)

w = QtWidgets.QMainWindow()
ui = UiMainWindow()
ui.setupUi(w)

w.show()

sys.exit(app.exec_())