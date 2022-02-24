import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from screeninfo import get_monitors

def runsettings():
    app = QApplication(sys.argv)
    mainwindow = MainWindow()
    widget = QtWidgets.QStackedWidget()
    widget.addWidget(mainwindow)
    widget.setFixedHeight(277)
    widget.setFixedWidth(385)
    widget.show()
    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("Settings.ui",self)

        #fill in monitor list
        self.monitors = get_monitors()
        for idx, m in enumerate(self.monitors):
            print(m)
            self.monitor.addItem(m.name)
            self.monitor.setItemData(idx, m)

        #fill in cam list
        for num in range(4):
            self.cam.addItem(str(num))

        #ok click
        self.okButton.clicked.connect(self.save)


    def save(self):
        selectedmonitor = None
        print("I ran the save function")
        fullscreen = self.isfullscreen.isChecked()
        print("is fullscreen: " + str(fullscreen))
        print(self.monitor.currentData())
        #print("Camera number: " + self.cam.currentData())

        #for m in self.monitors:
            #if str(m.name) == str(self.monitor.currentText()):
                #selectedmonitor = m

        #print("selected monitor: " + selectedmonitor.name + "with position x="+selectedmonitor.x + " y="+selectedmonitor.y)



    def cancle(self):
        pass





