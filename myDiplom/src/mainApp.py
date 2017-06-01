import sys
from PyQt5.QtWidgets import QDialog,QWidget, QApplication, QPushButton, QVBoxLayout, QMainWindow

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

import pandas as pd

class Window(QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.resize(900,600)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to `plot` method
        self.button = QPushButton('Plot')
        self.button.clicked.connect(self.plot)

        # set the layout
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.central_widget.setLayout(layout)

    def plot(self):
        ''' plot some random stuff '''
        hashtag_input = 'photoshop'
        filename = 'photoshop2017-04-112017-04-12.csv'

        df = pd.read_csv(filename)

        df2 = pd.DataFrame()
        df2['count'] = pd.Series([0 for x in range(len(df.index))])
        df2['count'] = 1
        df2['datetime'] = pd.to_datetime(df['created_at'])
        df2.index = df2['datetime']
        dataOut = df2.resample('30Min').sum()
        ts = dataOut['count']
        print(ts)
        ts.to_csv('datafixed.csv')
        # How to Check Stationarity of a Time Series
        plt.plot(ts)
        moving_avg = ts.rolling(window=2).mean()
        # plt.plot(moving_avg, color='red', label='Rolling Mean')
        # print((moving_avg))

        # instead of ax.hold(False)
        self.figure.clear()

        # create an axis
        ax = self.figure.add_subplot(111)

        # discards the old graph
        # ax.hold(False) # deprecated, see above

        # plot data
        ax.set_title('Trend and Count of #'+ hashtag_input)
        ax.set_xlabel('Time')
        ax.set_ylabel('Count')
        plt.xticks(rotation=15)

        # ax.plot(ts, color= 'blue',marker='o',markersize=3 ,label='real data')
        ax.plot(ts, color='blue', label='real data')
        ax.plot(moving_avg, color='red',label='Rolling Mean')
        ax.legend()
        # refresh canvas
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())