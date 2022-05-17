import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic, QtCore, QtWidgets, QtGui
from check_user import *
from check_str import *
from check_rec import *
import random
import time


if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

data = ['Вся семья Королевых, с часу на час поджидавшая своего Володю, бросилась к окнам.',
        'У подъезда стояли широкие розвальни, и от тройки белых лошадей шел густой туман.',
        'Сани были пусты, потому что Володя уже стоял в сенях и красными, озябшими пальцами развязывал башлык.',
        'Все смешалось в один сплошной радостный звук, продолжавшийся минуты две.',
        'До двух часов, когда сели обедать, все было тихо, но за обедом вдруг оказалось, что мальчиков нет дома.']


class SecretWin(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(SecretWin, self).__init__(parent)
        uic.loadUi('secrett.ui', self)


class SecondWin(QtWidgets.QDialog):
    speed = ''

    def __init__(self, parent=None):
        super(SecondWin, self).__init__(parent)
        uic.loadUi('second.ui', self)

        self.home_button.clicked.connect(self.home)
        self.start_button.clicked.connect(self.start)
        self.aboutButton.clicked.connect(self.about)

        self.check_str = CheckStr()

    def home(self):
        self.hide()

    def about(self):
        QtWidgets.QMessageBox.information(self, 'About', 'Чтобы завершить тест нажмите <CapsLock>')

    def start(self):
        global data
        self.fst = time.time()
        self.text_output = random.choice(data)
        self.enterLab.setText(self.text_output)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_CapsLock:
            self.text = self.inputLine.text()
            self.scd = time.time()
            if not self.text:
                QtWidgets.QMessageBox.warning(self, 'Warning', 'Мы не можем проверить пустую строку')
                return
            ers = self.check_str.check(self.text_output, self.text)
            percent = round(((len(self.text) - ers)/len(self.text)) * 100)
            timm = round(self.scd - self.fst, 2)
            self.speed = round((len(self.text) - ers) * 60 / timm, 2)
            self.resultLab.setText(f'Время прохождения теста: {timm}секунд'
                                   f'\nПроцент точности набора:{percent}%'
                                   f'\nСкорость: {self.speed}wpm')
            self.enterLab.setText('')
            if ex.check_user.login:
                ex.check_rec.saveRec(ex.check_user.login, self.speed)


class Signwin(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Signwin, self).__init__(parent)
        uic.loadUi('sign.ui', self)  # дизайн окна регистрации

        self.singInButton.clicked.connect(self.runIn)
        self.singUpButton.clicked.connect(self.runUp)

    def runIn(self):
        name = self.Logline.text()
        passw = self.Passline.text()
        ex.check_user.signIn(name, passw)
        self.hide()

    def runUp(self):
        name = self.Logline.text()
        passw = self.Passline.text()
        ex.check_user.signUp(name, passw)
        self.hide()


class Mainwin(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('first.ui', self)

        self.start_button.clicked.connect(self.runStart)
        self.log_button.clicked.connect(self.runSign)
        self.record_button.clicked.connect(self.runRec)
        self.secretButton.clicked.connect(self.secret)

        self.check_user = CheckThread()
        self.check_rec = CheckRec()

    def secret(self):
        self.parent4 = SecretWin()
        self.parent4.show()

    def runStart(self):
        self.parent3 = SecondWin()
        self.parent3.exec()

    def runSign(self):
        self.parent = Signwin()
        self.parent.show()

    def runRec(self):
        try:
            if self.check_user.login and self.parent3.speed:
                rec = self.check_rec.check_rec(self.check_user.login, self.parent3.speed)
                QtWidgets.QMessageBox.information(self, 'Record', f'Ваш наилучший результат - {rec}wpm')
            else:
                QtWidgets.QMessageBox.information(self, 'Record', f'Нет данных.')
        except AttributeError:
            self.check_rec.returnRec(self.check_user.login)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Mainwin()
    ex.show()
    sys.exit(app.exec_())
