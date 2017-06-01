# -*- coding: utf-8 -*-
try:
    from PyQt5.QtCore import QString
except ImportError:
    # we are using Python3 so QString is not defined
    QString = str
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget,QMessageBox,QDialog, QPushButton, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import *
from PyQt5.uic import loadUi, loadUiType
from twitterscraper import query_tweets
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import matplotlib.figure as Figure
from matplotlib.pylab import rcParams
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from datetime import datetime
rcParams['figure.figsize'] = 13, 7
import statsmodels.api as sm

app = QApplication(sys.argv)
app.setApplicationName('')
form_class, base_class = loadUiType('mainwindow.ui')


class MainWindow(QMainWindow,QWidget, form_class):
    def __init__(self, *args):
        super(MainWindow, self).__init__(*args)
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Hashtag Application')
        self.setWindowIcon(QIcon("iconTwii.jpg"))
        self.getInforBtn.clicked.connect(self.btnClicked)
    def scrapeTweets(self, hashtag, starttime, endtime):
        data = query_tweets('\'' + '%23' + hashtag + '%20since%3A' + starttime + '%20until%3A' + endtime + '\'')
        raw_data = {'user': [tweet.user for tweet in data],
                    'id': [tweet.id for tweet in data],
                    'created_at': [tweet.timestamp for tweet in data],
                    'text': [tweet.text for tweet in data]}
        df = pd.DataFrame(raw_data, columns=['user',
                                             'id',
                                             'created_at',
                                             'text'])
        df.to_csv(hashtag + starttime + endtime + '.csv', encoding='utf-8')
    # df = df.groupby(["created_at"]).size().reset_index(name="count")

        # self.plot_widget.setGeometry(250, 180, 500, 600)

    def btnClicked(self):
        ''' plot some random stuff '''
        # hashtag_input = self.hashtag_input.text()
        # start_day = self.start_time_input.date().toString('yyyy-MM-dd')
        # end_day = self.end_time_input.date().toString('yyyy-MM-dd')
        # self.scrapeTweets(hashtag_input,start_day,end_day)
        filename = 'lightroom2017-04-102017-04-17.csv'
        # filename= hashtag_input + start_day + end_day + '.csv'
        df = pd.read_csv(filename)
        df2 = pd.DataFrame()
        df2['count'] = pd.Series([0 for x in range(len(df.index))])
        df2['count'] = 1
        df2['datetime'] = pd.to_datetime(df['created_at'])
        df2.index = df2['datetime']
        dataOut = df2.resample('4H').sum()
        ts = dataOut['count']
        ts.to_csv('datafixed.csv')
        # How to Check Stationarity of a Time Series
        plt.plot(ts, 'b-')
        moving_avg = ts.rolling(window=12).mean()
        # plt.plot(moving_avg, color='red', label='Rolling Mean')
        print((moving_avg))
        plt.plot(moving_avg, 'r-')
        plt.show()
    #
    # def scrapeTweets(self, hashtag, starttime, endtime):
    #     data = query_tweets('\'' + '%23' + hashtag + '%20since%3A' + starttime + '%20until%3A' + endtime + '\'')
    #     raw_data = {'user': [tweet.user for tweet in data],
    #                 'id': [tweet.id for tweet in data],
    #                 'created_at': [tweet.timestamp for tweet in data],
    #                 'text': [tweet.text for tweet in data]}
    #     df = pd.DataFrame(raw_data, columns=['user',
    #                                          'id',
    #                                          'created_at',
    #                                          'text'])
    #     df.to_csv(hashtag + starttime + endtime + '.csv', encoding='utf-8')
        # df = df.groupby(["created_at"]).size().reset_index(name="count")

    # def anlyzeTren(self, filename):
    #     # Change to Time Series Form
    #     df = pd.read_csv(filename)
    #     df2= pd.DataFrame()
    #     df2['count'] = pd.Series([0 for x in range(len(df.index))])
    #     df2['count'] = 1
    #     df2['datetime'] = pd.to_datetime(df['created_at'])
    #     df2.index = df2['datetime']
    #     dataOut = df2.resample('4H').sum()
    #     ts = dataOut['count']
    #     ts.to_csv('datafixed.csv')
    #     # How to Check Stationarity of a Time Series
    #     plt.plot(ts)
    #     moving_avg = ts.rolling(window=12).mean()
    #     plt.plot(moving_avg, color='red', label='Rolling Mean')

    # # Notice Quit or no
    # def closeEvent(self, event):
    #     reply = QMessageBox.question(self,'Message','Are you sure to quit', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    #     if reply == QMessageBox.Yes:
    #         event.accept()
    #     else:
    #         event.ignore()

    # def btnClicked(self):
    #     hashtag_input =self.hashtagEdit.text()
    #     start_day =  self.startDateEdit.date().toString('yyyy-MM-dd')
    #     end_day =   self.endDateEdit.date().toString('yyyy-MM-dd')
    #
    #     # self.scrapeTweets(hashtag_input,start_day,end_day)
    #     # filename= hashtag_input + start_day + end_day + '.csv'
    #     filename= 'lightroom2017-04-102017-04-17.csv'
    #     # self.anlyzeTren(filename)
    #     # plt.savefig('Trendwindow=12')
    #     filename = 'lightroom2017-04-102017-04-17.csv'
    #     df = pd.read_csv(filename)
    #     df2 = pd.DataFrame()
    #     df2['count'] = pd.Series([0 for x in range(len(df.index))])
    #     df2['count'] = 1
    #     df2['datetime'] = pd.to_datetime(df['created_at'])
    #     df2.index = df2['datetime']
    #     dataOut = df2.resample('4H').sum()
    #     ts = dataOut['count']
    #     ts.to_csv('datafixed.csv')
    #
    #     moving_avg = ts.rolling(window=12).mean()
    #     # plt.plot(moving_avg, color='red', label='Rolling Mean')
    #     # print((moving_avg))
    #


if __name__ == '__main__':
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())
    # form = MainWindow()
    # form.setWindowTitle('Hashtag Application')
    # form.show()
    # sys.exit(app.exec_())
