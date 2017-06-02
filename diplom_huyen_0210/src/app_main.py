# -*- coding: utf-8 -*-
# Libraries using
try:
    from PyQt5.QtCore import QString
except ImportError:
    # we are using Python3 so QString is not defined
    QString = str
import sys
import os
import ntpath
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, \
    QLineEdit, QDateEdit, QMessageBox, QMenuBar, QAction, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from twitterscraper import query_tweets
import pandas as pd
import string
import tweepy
import csv
from app_ui import Window0

class App_main_ui(QMainWindow, Window0):
    def __init__(self, *args):
        super(Window0, self).__init__(*args)
        self.resize(900, 600)
        # noinspection PyArgumentList
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.initUI()






if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = App_main_ui()
    main.show()

    sys.exit(app.exec_())
