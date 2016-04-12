import sys
import re
import requests
from PyQt4 import QtCore, QtGui, uic

qtCreatorFile = "untitled.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.research.clicked.connect(self.put)
        self.clean.clicked.connect(self.clear)
    def put (self):
         word=(self.inputbox.toPlainText())
         url = 'http://dict.youdao.com/search?q='
         r = requests.get(url + word)
         content = r.text

         try:
            ps = re.findall(re.compile('"phonetic">(.*?)</span>'), content)
            pattern = re.compile('"trans-container">(.*?)</div>', re.S)
            tmp = re.findall(pattern, content)
            mean = re.findall(re.compile('<li>(.*?)</li>'), tmp[0])
         except:
                n='can not find it'
                self.outputbox.setText(n)
                return

         if len(ps) is 2:
               self.outputbox.append(u'英{0} 美{1}'.format(ps[0], ps[1]))
         else:
            try:
               self.outputbox.append(ps[0])
            except:
                 pass
         for line in mean:
            words = line.split('.', 1)
            if len(words) is 2:
                 words[0] += '.'
                 self.outputbox.append(u'{0}{1}'.format(words[0], words[1]))
               # word
            else:
                 self.outputbox.append(u'{0}'.format(words[0]))
               # phrase
    def clear(self):
        self.inputbox.clear()
        self.outputbox.clear()



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
