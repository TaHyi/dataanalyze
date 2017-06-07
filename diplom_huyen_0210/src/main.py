# -*- coding: utf-8 -*-
# Libraries using
try:
    from PyQt5.QtCore import QString
except ImportError:
    QString = str
import sys
import os
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, \
    QLineEdit, QDateEdit, QMessageBox, QMenuBar, QAction, QFileDialog, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QIcon, QFont
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import pandas as pd
import string
import tweepy
import csv
import json
import time
import datetime


class Window(QMainWindow):
    def __init__(self, *args):
        super(Window, self).__init__(*args)
        self.setWindowTitle('Выявление трендов на основе анализа хештегов Твиттер')
        self.setWindowIcon(QIcon("./icons/twitterlogo.png"))  # Set Icon of Window
        self.resize(900, 600)
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        # A statusbar is a widget that is used for displaying status information.
        self.statusBar().showMessage("Готово")  # Statusbar
        self.init_menu()

    def init_menu(self):
        # Create Menubar
        #  Add "Open File" Action
        open_action = QAction(QIcon('./icons/openfile.jpg'), '&Открыть файл', self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('Открыть приложение')
        # Connect object "open_action" to function "file_open"
        open_action.triggered.connect(self.get_data_from_file)
        #  Add "Exit" Action
        exit_action = QAction(QIcon('./icons/exit.png'), '&Закрыть приложение', self)
        exit_action.setShortcut('Ctrl+W')
        exit_action.setStatusTip('Закрыть приложение')
        exit_action.triggered.connect(self.close)
        # Connect object "exit_action" to function "closeEvent"
        # Create status bar and add actions to menubar
        self.statusBar()
        menubar = self.menuBar()
        file_menu = menubar.addMenu('&Файл')
        file_menu.addAction(open_action)
        file_menu.addAction(exit_action)

    # Design Gui of application
        # Create a figure instance to plot on
        self.figure = Figure()
        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Add labels into Gui
        self.hashtag_label = QLabel('Хештег(#)')
        self.start_time_label = QLabel('Время начала')
        self.end_time_label = QLabel('Время окончания')

        # Add line edit into Gui
        self.hashtag_input = QLineEdit()
        self.hashtag_input.setPlaceholderText('#')
        # Add Date Edit into Gui
        self.start_time_input = QDateEdit()
        self.start_time_input.setCalendarPopup(True)
        self.start_time_input.setDateTime(QtCore.QDateTime(QtCore.QDate(2017, 6, 5), QtCore.QTime(1, 0, 0)))
        self.end_time_input = QDateEdit()
        self.end_time_input.setCalendarPopup(True)
        self.end_time_input.setDateTime(QtCore.QDateTime.currentDateTime())
        # Buttion Get Informations
        self.getInforBtn = QPushButton('Получить информацию')
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
        label = QtWidgets.QLabel()
        layout3Cot.addWidget(label)
        verticalSpacer = QtWidgets.QSpacerItem(200, 100, QtWidgets.QSizePolicy.Maximum, QSizePolicy.Expanding)
        layout3Cot.addItem(verticalSpacer)
        layout3Cot.addLayout(layout123)
        layout3Cot.addWidget(self.getInforBtn)
        self.result = QLabel("")
        self.time = QLabel("")
        # set the layout
        layoutGraph = QVBoxLayout()
        # layoutGraph.addWidget(self.button)
        layoutGraph.addLayout(layout3Cot)
        layoutGraph.addWidget(self.canvas)
        layoutGraph.addWidget(self.time)
        layoutGraph.addWidget(self.result)
        self.time.setFont(QtGui.QFont("Times", 10, weight=QtGui.QFont.Normal))
        self.result.setFont(QtGui.QFont("Times",12, weight=QtGui.QFont.DemiBold))
        layoutGraph.addWidget(self.toolbar)
        self.central_widget.setLayout(layoutGraph)
        # connect slot, signal
        self.getInforBtn.clicked.connect(self.getInformation)
        self.df = pd.DataFrame()
        self.time_list = []
        self.show()

    # Work with file

    def get_data_from_file(self):
        print("load file")
        try:
            file_choices = "CSV (*.csv)|*.csv"
            path = (QFileDialog.getOpenFileName(self, 'Load test file', '', file_choices))
            self.df = pd.read_csv(path[0], ',')
            self.time_list = self.df.created_at.unique().tolist()
            self.analyze_data()
            file_name = os.path.basename(path[0])
            self.plot(file_name[:-15])
            self.statusBar().showMessage('Визуализация данных файла о #%s' % file_name[:-15], 2000)
        except  Exception:
            self.statusBar().showMessage('Exception: %s' % sys.exc_info()[0], 2000)

    def analyze_data(self):
        # create new dataFrame. Create into it 1 column "Time", pull list "time_list" into its column
        # replace missing values with 0
        self.df_filter = pd.DataFrame()
        self.df_filter['DateTime'] = self.time_list
        date0 = datetime.datetime.strptime(self.time_list[0], "%Y-%m-%d %H:%M:%S")
        date1 = datetime.datetime.strptime(self.time_list[-1], "%Y-%m-%d %H:%M:%S")
        # create a serie form to count value of
        series_count = self.df['created_at'].value_counts()
        # # bi xao tron vi tri
        self.df_filter['Count'] = [value for value in series_count]
        self.df_filter['DateTime'] = pd.to_datetime(self.df['created_at'])
        self.df_filter.index = self.df_filter['DateTime']
        self.ts = self.df_filter['Count']
        if ((date1 - date0).days >= 100):
            self.df_grouped = self.ts.resample('60Min').sum()
            self.df_grouped = self.df_grouped.fillna(0)
            print(self.df_grouped.isnull().sum())
            self.moving_avg = self.df_grouped.rolling(window=24).mean()
            y_t0 = self.moving_avg.ix[self.moving_avg.index.min(), 'DateTime']
            y_tk = self.moving_avg.ix[self.moving_avg.index.max(), 'DateTime']
            print("Первая точка функции скользящего среднего y_t0= ", end='')
            print(y_t0)
            print("Последняя точка функции скользящего среднего y_tk= ", end='')
            print(y_tk)
            if (y_t0 > y_tk):
                self.time.setText("Выявление тренды в промежутке времени ["+ self.time_list[0] + ";" + self.time_list[-1]+ "]")
                print("Долгосрочный, тренд нисходящий")
                self.result.setText("Долгосрочный, тренд нисходящий")
            else:
                self.time.setText("Выявление тренды в промежутке времени ["+ self.time_list[0] + ";" + self.time_list[-1]+ "]")
                print("Долгосрочный, тренд восходящий")
                self.result.setText("Долгосрочный, тренд восходящий")
        else:
            self.df_grouped = self.ts.resample('30Min').sum()
            self.df_grouped = self.df_grouped.fillna(0)
            self.moving_avg = self.df_grouped.rolling(window=2).mean()
            x_tk = self.df_grouped.ix[self.df_grouped.index.max(), 'DateTime']
            y_tk = self.moving_avg.ix[self.moving_avg.index.max(), 'DateTime']
            print("Последняя точка функции скользящего среднего y_tk= ", end='')
            print(y_tk)
            print("Последняя точка на реальном x_tk= ", end='')
            print(x_tk)
            if (y_tk > x_tk):
                self.time.setText("Выявление тренды в промежутке времени ["+ self.time_list[0] + ";" + self.time_list[-1]+ "]")
                print("Краткосрочный, тренд нисходящий")
                self.result.setText("Краткосрочный, тренд нисходящий")
            else:
                self.time.setText("Выявление тренды в промежутке времени ["+ self.time_list[0] + ";" + self.time_list[-1]+ "]")
                print("Краткосрочный, тренд восходящий")
                self.result.setText("Краткосрочный, тренд восходящий")

    def plot(self, hashtag):
        try:
            # instead of ax.hold(False)
            self.figure.clear()
            # create an axis
            ax = self.figure.add_subplot(111)
            # discards the old graph
            ax.set_title('Визуализация тренды хештеги #' + hashtag)
            ax.set_xlabel('Время')
            ax.set_ylabel('Количество')
            # ax.xticks(rotation=15)
            ax.plot(self.df_grouped, color='blue', marker='o', markersize=3, label='Количество хештеги линии')
            ax.plot(self.moving_avg, color='red', label='Тренды хештеги линии')
            ax.legend()
            # refresh canvas
            self.canvas.draw()
            self.statusBar().showMessage("Готово")
        except  Exception:
            self.statusBar().showMessage('Exception: %s' % sys.exc_info()[0], 2000)

    # Close application
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Сообщение', 'Вы хотите выйти?', QMessageBox.Yes | QMessageBox.No,
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
                QMessageBox.information(self, 'Сообщение', 'Вводите хештег, пожалуйста!')
            elif (start_day >= end_day):
                QMessageBox.information(self, 'Сообщение', 'Неправильный формат времени!')
            elif ((self.end_time_input.date().toPyDate() - self.start_time_input.date().toPyDate()).days > 7):
                QMessageBox.information(self, 'Сообщение', 'Неправильный формат времени!')
            elif (end_day > datetime.date.today().strftime("%Y-%m-%d")):
                QMessageBox.information(self, 'Сообщение', 'Неправильный формат времени!')
            elif (len(hashtag_input) > 140):
                QMessageBox.information(self, 'Сообщение', 'Ограничено до 140 символов')
            elif (' ' in hashtag_input):
                QMessageBox.information(self, 'Сообщение', 'Хештег не поддерживает " "')
            elif any(char in (set(string.punctuation.replace("_", ""))) for char in hashtag_input):
                QMessageBox.information(self, 'Сообщение', 'Хэштег включает в себя букв, цифры')
            else:
                # # ************************************************************************************************************************
                API_KEY = "vuuHtQehJVLkfQEL7pUxOX4yW"
                API_SECRET = "XPfT8jIJeSvoghsIjcDpJXYKaKSlS9KGyhSOlksDL3EdirsiRD"
                auth = tweepy.AppAuthHandler(API_KEY, API_SECRET)
                api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
                if (not api):
                    self.statusBar().showMessage("Не удается аутентифицировать")
                    print("Не удается аутентифицировать")
                    sys.exit(-1)
                searchQuery = '#' + hashtag_input + ' since:' + start_day + ' until:' + end_day
                # this is what we're searching for hashtag_input since:start_day until:end_day
                maxTweets = 10000000  # Some arbitrary large number
                tweetsPerQry = 100  # this is the max the API permits
                fName = hashtag_input + start_day[5:] + '_' + end_day[5:] + '.csv'
                fNamePath = "./" + fName  # We'll store the tweets in a text file.
                raw_data = []
                # If results from a specific ID onwards are reqd, set since_id to that ID.
                # else default to no lower limit, go as far back as API allows
                sinceId = None
                # If results only below a specific ID are, set max_id to that ID.
                # else default to no upper limit, start from the most recent tweet matching the search query.
                max_id = -1
                tweetCount = 0
                self.statusBar().showMessage("Загрузка максимум {0} твитов".format(maxTweets))
                print("Загрузка максимум {0} твитов".format(maxTweets))
                with open(fNamePath, 'w', encoding='utf-8') as f:
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
                                self.statusBar().showMessage("Найти конец")
                                print("Найти конец")
                                break
                            for tweet in new_tweets:
                                writer.writerow([tweet.id, tweet.created_at, tweet.text])
                                raw_data.append(json.loads(json.dumps(tweet._json)))
                            tweetCount += len(new_tweets)
                            self.statusBar().showMessage("Загрузил {0} твитов".format(tweetCount), 2000)
                            print("Загрузил {0} твитов".format(tweetCount))
                            max_id = new_tweets[-1].id
                        except tweepy.TweepError as e:
                            # Just exit if any error
                            self.statusBar().showMessage("some error : " + str(e))
                            print("some error : " + str(e))
                            break
                # self.df = pd.DataFrame()
                self.df['id'] = list(map(lambda tweet: tweet['id'], raw_data))

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
