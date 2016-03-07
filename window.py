import urllib2
import urllib
import json
import sys
from PyQt4 import QtGui,QtCore

class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.saveLabel = QtGui.QLabel('Output folder')
        self.linkLabel = QtGui.QLabel('Link')
        self.statusLabel = QtGui.QLabel('Status')

        self.saveLineEdit = QtGui.QLineEdit(self)
        self.saveLineEdit.setReadOnly(1)
        self.linkLineEdit = QtGui.QLineEdit(self)

        self.downloadButtom = QtGui.QPushButton("Download")
        self.browseButtom = QtGui.QPushButton("Browse")
        self.browseButtom.clicked.connect(self.btBrowserClicked)
        self.downloadButtom.clicked.connect(self.btDownloadClicked)

        self.grid = QtGui.QGridLayout(self)
        self.grid.setSpacing(10)

        self.grid.addWidget(self.saveLabel, 1, 0)
        self.grid.addWidget(self.saveLineEdit, 1, 1)
        self.grid.addWidget(self.browseButtom, 1,2)

        self.grid.addWidget(self.linkLabel, 2, 0)
        self.grid.addWidget(self.linkLineEdit, 2, 1)
        self.grid.addWidget(self.downloadButtom, 2, 2)
        self.grid.addWidget(self.statusLabel, 3, 1)

        self.setLayout(self.grid)
        self.setWindowTitle('Download Mp3 Youtube')
        self.show()

    def btBrowserClicked(self):
        openfile = QtGui.QFileDialog.getExistingDirectory(self)
        self.saveLineEdit.setText(openfile)

    def showMessage(self,str):
        error = QtGui.QMessageBox()
        error.setWindowTitle("ERROR")
        error.setText(str)
        error.exec_()


    def btDownloadClicked(self):
        if self.saveLineEdit.text() == "":
            self.showMessage("Path is empty")
        elif self.linkLineEdit.text() == "":
            self.showMessage("Link is empty")
        else:
            try:
                link = self.linkLineEdit.text()
                r = urllib2.urlopen("http://www.youtubeinmp3.com/fetch/?format=JSON&video=%s" % link)
            except urllib2.HTTPError, err:
                if err.code == 404:
                    self.showMessage("Page not Found")
                    r.close()
                if err.code == 403:
                    self.showMessage("Access denied!")
                    r.close()
                else:
                    self.showMessage("Something went wrong, try again!, Error code: "+err.code)
                    r.close()

            except urllib2.URLError, err:
                self.showMessage("Something went wrong: "+err.reason)


            j = json.load(r)
            r.close()
            if 'error' in j:
                self.showMessage("ERROR:  There ir no mp3 for this link, please try later")
                self.statusLabel.setText('Error : %s ' % j['error'])
            else:
                self.downloadButtom.setEnabled(0)
                self.statusLabel.setText(j['title'])
                urllib.urlretrieve(j["link"], "%s\%s.mp3" % (self.saveLineEdit.text() ,j['title']))
                self.downloadButtom.setEnabled(1)
                self.statusLabel.setText("Finished")




def main():
    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
