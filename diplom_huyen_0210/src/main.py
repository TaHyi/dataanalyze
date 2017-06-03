# -*- coding: utf-8 -*-
# Libraries using
try:
    from PyQt5.QtCore import QString
except ImportError:
    QString = str
import sys
import os
import ntpath
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, \
    QLineEdit, QDateEdit, QMessageBox, QMenuBar, QAction, QFileDialog, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from twitterscraper import query_tweets
import pandas as pd
import string
import tweepy
import csv
import json
import time
import datetime
from io import StringIO

class Window(QMainWindow):
    def __init__(self, *args):
        super(Window, self).__init__(*args)
        self.setWindowTitle('Hashtag Application')
        self.setWindowIcon(QIcon("./icons/twitterlogo.png"))# Set Icon of Window
        self.resize(900, 600)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        # A statusbar is a widget that is used for displaying status information.
        self.statusBar().showMessage("Ready")  # Statusbar
        self.initmMain_UI()
        self.initMenu()

    def initMenu(self):
        # Create Menubar
        #  Add "Open File" Action
        openAction = QAction(QIcon('./icons/openfile.jpg'), '&Open File', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open application')
        # Connect object "openAction" to function "file_open"
        openAction.triggered.connect(self.get_data_from_file)
        #  Add "Exit" Action
        exitAction = QAction(QIcon('./icons/exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        # Connect object "exitAction" to function "closeEvent"
        # Create status bar and add actions to menubar
        self.statusBar()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)

    # Design Gui of application
    def initmMain_UI(self):
        # Create a figure instance to plot on
        self.figure = plt.figure()
        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Add labels into Gui
        self.hashtag_label = QLabel('Hashtag(#)')
        self.start_time_label = QLabel('Time Start')
        self.end_time_label = QLabel('Time End')

        # Add line edit into Gui
        self.hashtag_input = QLineEdit()
        self.hashtag_input.setPlaceholderText('#')
        # Add Date Edit into Gui
        self.start_time_input = QDateEdit()
        self.start_time_input.setCalendarPopup(True)
        self.start_time_input.setDateTime(QtCore.QDateTime.currentDateTime())
        self.end_time_input = QDateEdit()
        self.end_time_input.setCalendarPopup(True)

        self.end_time_input.setDateTime(QtCore.QDateTime.currentDateTime())
        # Buttion Get Informations
        self.getInforBtn = QPushButton('Get Informations')
        # Arrange item of Gui
        # layout 1: row 1 include label "Hashtag(#)" and QlineEdit hashtag input
        layout1 = QHBoxLayout()
        layout1.addWidget(self.hashtag_label)
        layout1.addWidget(self.hashtag_input)
        # layout 2: row 2 include label "Time Start" and QDateTime start time
        layout2 = QHBoxLayout()
        layout2.addWidget(self.start_time_label)
        layout2.addWidget(self.start_time_input)
        # layout 3: row 3 include label "Time End" and QDateTime end time
        layout3 = QHBoxLayout()
        layout3.addWidget(self.end_time_label)
        layout3.addWidget(self.end_time_input)
        # Layout123 include 2 columns
        layout123 = QVBoxLayout()
        layout123.addLayout(layout1)
        layout123.addLayout(layout2)
        layout123.addLayout(layout3)
        # Layout 3Cot 3 colums
        layout3Cot = QHBoxLayout()
        label= QtWidgets.QLabel()
        layout3Cot.addWidget(label)
        verticalSpacer = QtWidgets.QSpacerItem(200, 100, QtWidgets.QSizePolicy.Maximum, QSizePolicy.Expanding)
        layout3Cot.addItem(verticalSpacer)
        layout3Cot.addLayout(layout123)
        layout3Cot.addWidget(self.getInforBtn)

        # set the layout
        layoutGraph = QVBoxLayout()
        # layoutGraph.addWidget(self.button)
        layoutGraph.addLayout(layout3Cot)
        layoutGraph.addWidget(self.canvas)
        layoutGraph.addWidget(self.toolbar)
        self.central_widget.setLayout(layoutGraph)
        # connect slot, signal
        self.getInforBtn.clicked.connect(self.getInformation)

        self.df = pd.DataFrame()
        self.time_list =[]

        self.show()

    # Work with file
    def get_data_from_file(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, "Open file", "",
                                                       "All Files (*);;CSV Files (*.csv)")
            if file_path:
                file_name = os.path.basename(file_path)
                self.df = pd.read_csv(file_name)
                self.time_list = self.df.created_at.unique().tolist()
                self.analyze_data()
                self.plot(file_name[:-15])
        except  Exception:
            self.statusBar().showMessage('Exception: %s' % sys.exc_info()[0], 2000)

    def analyze_data(self):
        # create new dataFrame. Create into it 1 column "Time", pull list "time_list" into its column
        # replace missing values with 0
        self.df_filter = pd.DataFrame()
        self.df_filter['DateTime'] = self.time_list
        self.df_filter = pd.DataFrame()
        self.df_filter['DateTime'] = self.time_list

        # create a serie form to count value of
        series_count = self.df['created_at'].value_counts()
        # # bi xao tron vi tri
        self.df_filter['Count'] = [value for value in series_count]
        self.df_filter['DateTime'] = pd.to_datetime(self.df['created_at'])
        self.df_filter.index = self.df_filter['DateTime']
        self.ts = self.df_filter['Count']
        self.df_grouped = self.ts.resample('10Min').sum()
        self.df_grouped = self.df_grouped.fillna(0)
        self.moving_avg = self.df_grouped.rolling(window=10).mean()

    def plot(self, hashtag):
        try:
            # instead of ax.hold(False)
            self.figure.clear()
            # create an axis
            ax = self.figure.add_subplot(111)
            # discards the old graph
            ax.set_title('Trend and Count of #' + hashtag)
            ax.set_xlabel('Time')
            ax.set_ylabel('Count')
            plt.xticks(rotation=15)
            ax.plot(self.df_grouped, color='blue', marker='o', markersize=3, label='Origanal line')
            ax.plot(self.moving_avg, color='red', label='Trend line')
            ax.legend()
            # refresh canvas
            self.canvas.draw()
            self.statusBar().showMessage("Ready")
        except  Exception:
            self.statusBar().showMessage('Exception: %s' % sys.exc_info()[0], 2000)

    # Close application
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', 'Are you sure to quit', QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    def getInformation(self):
        try:
            hashtag_input = self.hashtag_input.text()
            start_day = self.start_time_input.date().toString('yyyy-MM-dd')
            end_day = self.end_time_input.date().toString('yyyy-MM-dd')
            if (hashtag_input == ''):
                QMessageBox.information(self, 'Message', 'No Hashtag input!')
            elif (start_day >= end_day):
                QMessageBox.information(self, 'Message', 'Wrong time input!')
            elif ((self.end_time_input.date().toPyDate() - self.start_time_input.date().toPyDate()).days > 7):
                QMessageBox.information(self, 'Message', 'Wrong time input!')
            elif (end_day > datetime.date.today().strftime("%Y-%m-%d")):
                QMessageBox.information(self, 'Message', 'Wrong time input!')
            elif (len(hashtag_input) > 140):
                QMessageBox.information(self, 'Message', 'Limited to under 140 characters')
            elif (' ' in hashtag_input):
                QMessageBox.information(self, 'Message', 'Hashtag do not support spaces')
            elif any(char in (set(string.punctuation.replace("_", ""))) for char in hashtag_input):
                QMessageBox.information(self, 'Message', 'Hashtag include letters, number')
            else:
                # # ************************************************************************************************************************
                API_KEY = "vuuHtQehJVLkfQEL7pUxOX4yW"
                API_SECRET = "XPfT8jIJeSvoghsIjcDpJXYKaKSlS9KGyhSOlksDL3EdirsiRD"
                auth = tweepy.AppAuthHandler(API_KEY, API_SECRET)
                api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
                if (not api):
                    self.statusBar().showMessage("Can't Authenticate")
                    print ("Can't Authenticate")
                    sys.exit(-1)
                searchQuery = '#'+hashtag_input+' since:'+start_day+' until:'+end_day  # this is what we're searching for google since:2016-10-10 until:2016-10-11
                maxTweets = 8000 # Some arbitrary large number
                tweetsPerQry = 100  # this is the max the API permits
                fName = hashtag_input+start_day[5:]+'_'+ end_day[5:]+'.csv' # We'll store the tweets in a text file.
                raw_data = []
                # If results from a specific ID onwards are reqd, set since_id to that ID.
                # else default to no lower limit, go as far back as API allows
                sinceId = None
                # If results only below a specific ID are, set max_id to that ID.
                # else default to no upper limit, start from the most recent tweet matching the search query.
                max_id = -1
                tweetCount = 0
                self.statusBar().showMessage("Downloading max {0} tweets".format(maxTweets))
                print("Downloading max {0} tweets".format(maxTweets))
                with open(fName,'w',encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(["id", "created_at", "text"])
                    while tweetCount < maxTweets:
                        try:

                            if (max_id <= 0):
                                if (not sinceId):
                                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry)
                                else:
                                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                                            since_id=sinceId)
                            else:
                                if (not sinceId):
                                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                                            max_id=str(max_id - 1))
                                else:
                                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                                            max_id=str(max_id - 1),
                                                            since_id=sinceId)
                            if not new_tweets:
                                self.statusBar().showMessage("No more tweets found")
                                print("No more tweets found")
                                break
                            for tweet in new_tweets:
                                writer.writerow([tweet.id, tweet.created_at, tweet.text])
                                raw_data.append(json.loads(json.dumps(tweet._json)))
                            tweetCount += len(new_tweets)
                            self.statusBar().showMessage("Downloaded {0} tweets".format(tweetCount))
                            print("Downloaded {0} tweets".format(tweetCount))
                            max_id = new_tweets[-1].id
                        except tweepy.TweepError as e:
                            # Just exit if any error
                            self.statusBar().showMessage("some error : " + str(e))
                            print("some error : " + str(e))
                            break
                self.df = pd.DataFrame()
                self.df['id'] =list(map(lambda tweet: tweet['id'], raw_data))

                self.df['created_at'] = list(map(lambda tweet: time.strftime('%Y-%m-%d %H:%M:%S',
                                                                            time.strptime(tweet['created_at'],
                                                                                          '%a %b %d %H:%M:%S +0000 %Y')),
                                                raw_data))
                self.df['text'] = list(map(lambda tweet: tweet['text'], raw_data))
                self.time_list = self.df.created_at.unique().tolist()
                self.analyze_data()
                self.plot(fName[:-15])
        except  Exception:
            self.statusBar().showMessage('Exception: %s' % sys.exc_info()[0], 2000)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Window()
    main.show()
    sys.exit(app.exec_())