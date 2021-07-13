import sys
from PyQt4 import QtGui, QtCore

class Example(QtGui.QMainWindow):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):

##        exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)        
##        exitAction.setShortcut('Ctrl+Q')
##        exitAction.setStatusTip('Exit application')
##        exitAction.triggered.connect(QtGui.qApp.quit)
##        menubar = self.menuBar()
##        fileMenu = menubar.addMenu('&File')
##        fileMenu.addAction(exitAction)


        self.statusBar().showMessage('Ready')

        QtGui.QToolTip.setFont(QtGui.QFont('Times', 10))


        #Window Tip
        self.setToolTip('This is a <b>QWidget</b> widget')

        #generic botton
        btn = QtGui.QPushButton('Click Here', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())
        btn.move(50, 50)

        #quit botton

        qbtn = QtGui.QPushButton('Quit', self)
        qbtn.setToolTip('This is <b>going to explode</b> widget')
        qbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(150, 150)       
        
        
        self.setGeometry(300, 300, 400, 400)
        self.center()
        self.setWindowTitle('Tooltips')    
        self.show()

    def closeEvent(self, event):

        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self):
        
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
