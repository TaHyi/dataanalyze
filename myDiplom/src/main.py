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


class Window(QMainWindow):
    def __init__(self, *args):
        super(Window, self).__init__(*args)
        self.resize(900, 600)
        # noinspection PyArgumentList
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.initUI()

    # Design Gui of application
    def initUI(self):
        # Set Title of Window
        self.setWindowTitle('Hashtag Application')
        # Set Icon of Window
        self.setWindowIcon(QIcon("./icons/twitterlogo.png"))
        # Statusbar
        # A statusbar is a widget that is used for displaying status information.
        self.statusBar().showMessage("Ready")
        # Create Menubar
        #  Add "Open File" Action
        openAction = QAction(QIcon('./icons/openfile.jpg'), '&Open File', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open application')
        # Connect object "openAction" to function "file_open"
        openAction.triggered.connect(self.file_open)
        #  Add "Exit" Action
        exitAction = QAction(QIcon('./icons/exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        # Connect object "exitAction" to function "closeEvent"
        exitAction.triggered.connect(self.closeEvent)
        # Create status bar and add actions to menubar
        self.statusBar()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)
        # For plot graph
        # Create a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Add labels into Gui
        self.main_label = QLabel('Hashtag Application')
        self.hashtag_label = QLabel('Hashtag(#)')
        self.start_time_label = QLabel('Time Start')
        self.end_time_label = QLabel('Time End')
        self.graph_label = QLabel('Graph trend of Hashtags')
        # Add line edit into Gui
        self.hashtag_input = QLineEdit()
        self.hashtag_input.setPlaceholderText('#')
        # Add Date Edit into Gui
        self.start_time_input = QDateEdit()
        self.start_time_input.setCalendarPopup(True)
        self.start_time_input.setDateTime(QtCore.QDateTime.currentDateTime())
        self.end_time_input = QDateEdit()
        self.end_time_input.setCalendarPopup(True)
        # self.end_time_input.setDateTime(QtCore.QDateTime(QtCore.QDate(2017, 4, 12), QtCore.QTime(1, 0, 0)))
        self.end_time_input.setDateTime(QtCore.QDateTime.currentDateTime())
        # Buttion Get Informations
        self.getInforBtn = QPushButton('Get Informations')
        # Arrange item of Gui
        # layout 1 column 1
        layout1 = QHBoxLayout()
        layout1.addWidget(self.hashtag_label)
        layout1.addWidget(self.hashtag_input)
        # layout 2 column 2
        layout2 = QHBoxLayout()
        layout2.addWidget(self.start_time_label)
        layout2.addWidget(self.start_time_input)
        # layout 3 column 3
        layout3 = QHBoxLayout()
        layout3.addWidget(self.end_time_label)
        layout3.addWidget(self.end_time_input)
        # Layout 123 two columns
        layout123 = QVBoxLayout()
        layout123.addLayout(layout1)
        layout123.addLayout(layout2)
        layout123.addLayout(layout3)
        # Layout 3Cot 3 colums
        layout3Cot = QHBoxLayout()
        layout3Cot.addWidget(self.main_label)
        layout3Cot.addLayout(layout123)
        layout3Cot.addWidget(self.getInforBtn)

        # set the layout
        layoutGraph = QVBoxLayout()
        # layoutGraph.addWidget(self.button)
        layoutGraph.addLayout(layout3Cot)
        layoutGraph.addWidget(self.graph_label)
        layoutGraph.addWidget(self.canvas)
        layoutGraph.addWidget(self.toolbar)
        self.central_widget.setLayout(layoutGraph)
        # connect slot, signal
        self.getInforBtn.clicked.connect(self.getInformation)

    # Work with file
    def file_open(self):
        # First go to the "./DataScraped/" directory
        # os.chdir('./DataScraped')
        # options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(self, "Open file", "",
                                                   "All Files (*);;CSV Files (*.csv)")
        if file_path:
            file_name = os.path.basename(file_path)
            # print(file_name)
            # with open(file_name, newline='') as f:
            #     reader = csv.reader(f)
            #     try:
            #         for row in reader:
            #             print(row)
            #     except csv.Error as e:
            #         sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))
            # with open(file_name, "rb") as fileInput:
            #     for row in csv.reader(fileInput):
            #         print(row)
            df = pd.read_csv(file_name,encoding='utf-8')
            print(df.head(6))
            # df2 = pd.DataFrame()
            # df2['count'] = pd.Series([0 for x in range(len(df.index))])
            # df2['count'] = 1
            # df2.index = df2['datetime']
            # dataOut = df2.resample('30T').sum()
            # ts = dataOut['count']
            # print(ts.head())


    # Close application
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', 'Are you sure to quit', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def getInformation(self):

        hashtag_input = self.hashtag_input.text()
        start_day = self.start_time_input.date().toString('yyyy-MM-dd')
        end_day = self.end_time_input.date().toString('yyyy-MM-dd')
        # invalidChars = set(string.punctuation.replace("_", ""))
        if (hashtag_input == ''):
            QMessageBox.information(self, 'Message', 'No Hashtag input!')
        elif (start_day >= end_day):
            QMessageBox.information(self, 'Message', 'Wrong time input!')
        elif (len(hashtag_input) > 140):
            QMessageBox.information(self, 'Message', 'Limited to under 140 characters')
        elif (' ' in hashtag_input):
            QMessageBox.information(self, 'Message', 'Hashtag do not support spaces')
        elif any(char in (set(string.punctuation.replace("_", ""))) for char in hashtag_input):
            QMessageBox.information(self, 'Message', 'Hashtag include letters, number')
        else:
            data = query_tweets(
                '\'' + '%23' + hashtag_input + '%20since%3A' + start_day + '%20until%3A' + end_day + '\'')
            raw_data = {'user': [tweet.user for tweet in data],
                        'id': [tweet.id for tweet in data],
                        'created_at': [tweet.timestamp for tweet in data],
                        'text': [tweet.text for tweet in data]}
            df = pd.DataFrame(raw_data, columns=['user',
                                                 'id',
                                                 'created_at',
                                                 'text'])
            # Save to file .csv
            # os.chdir('./DataScraped')
            path = r"C:\\Users\\TaHyi\\PycharmProjects\\myDiplom\\src\\DataScraped\\"
            # df.to_csv(path + file_name, encoding='utf-8', columns=header)
            df.to_csv(path+ hashtag_input + start_day + end_day + '.csv', encoding='utf-8', columns=header)
            # Create an other dataFrame to  container filtered data
            df2 = pd.DataFrame()
            df2['count'] = pd.Series([0 for x in range(len(df.index))])
            df2['count'] = 1
            df2['datetime'] = pd.to_datetime(df['created_at'])
            df2.index = df2['datetime']
            # Group data per 30 minutes per row
            dataOut = df2.resample('30Min').sum()
            # Count grouped data
            ts = dataOut['count']
            # Find trend of data
            moving_avg = ts.rolling(window=2).mean()

            # instead of ax.hold(False)
            self.figure.clear()

            # create an axis
            ax = self.figure.add_subplot(111)

            # discards the old graph
            # ax.hold(False) # deprecated, see above

            # plot data
            ax.set_title('Trend and Count of #' + hashtag_input)
            ax.set_xlabel('Time')
            ax.set_ylabel('Count')
            plt.xticks(rotation=15)

            ax.plot(ts, color='blue', marker='o', markersize=3, label='Origanal line')
            ax.plot(moving_avg, color='red', label='Trend line')
            ax.legend()
            # ax.savefig(hashtag_input+start_day+end_day)
            # refresh canvas
            self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())
