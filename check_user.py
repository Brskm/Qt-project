from PyQt5 import QtWidgets
import sqlite3


class CheckThread(QtWidgets.QWidget):
    login = ''

    def signIn(self, log, passw):
        con = sqlite3.connect('Users.db')
        cur = con.cursor()

        cur.execute(f'SELECT * FROM Data WHERE name="{log}"')
        value = cur.fetchall()

        if value != [] and str(value[0][2]) == passw:
            self.login = log
            QtWidgets.QMessageBox.information(self, 'Success', 'Успешная авторизация!')
            cur.close()
            con.close()

        else:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'Проверьте правильность ввода данных!')
            cur.close()
            con.close()

    def signUp(self, log, passw):
        con = sqlite3.connect('Users.db')
        cur = con.cursor()

        cur.execute(f'SELECT * FROM Data WHERE name="{log}"')
        value = cur.fetchall()
        if (not log) and (not passw):
            QtWidgets.QMessageBox.warning(self, 'Warning', 'Введена пустая строка!')

        elif value != []:
            QtWidgets.QMessageBox.warning(self, 'Warning', 'Такой ник уже используется!')

        elif value == []:
            cur.execute(f"INSERT INTO Data (name, password) VALUES ('{log}', '{passw}')")
            cur.execute(f"INSERT INTO Records (name) VALUES ('{log}')")
            self.login = log
            QtWidgets.QMessageBox.information(self, 'Success', 'Вы успешно зарегистрированы!')
            con.commit()

        cur.close()
        con.close()

