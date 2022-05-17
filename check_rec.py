from PyQt5 import QtWidgets
import sqlite3


class CheckRec(QtWidgets.QDialog):
    def check_rec(self, login, record2):
        con = sqlite3.connect('Users.db')
        cur = con.cursor()

        cur.execute(f'SELECT * FROM Records WHERE name = "{login}"')
        value = cur.fetchall()

        if value[0][2]:
            if float(value[0][2]) < float(record2):
                cur.execute(f"UPDATE Records SET record = '{record2}' WHERE name = '{login}'")
                return record2
            else:
                return value[0][2]
        elif not value[0][2]:
            cur.execute(f"UPDATE Records SET record = '{record2}' WHERE name = '{login}'")
            return record2
        con.commit()
        cur.close()
        con.close()

    def returnRec(self, login):
        con = sqlite3.connect('Users.db')
        cur = con.cursor()

        cur.execute(f'SELECT * FROM Records WHERE name = "{login}"')
        value = cur.fetchall()
        if value[0][2]:
            rec = value[0][2]
            QtWidgets.QMessageBox.information(self, 'Record', f'Ваш наилучший результат - {rec}wpm')
        else:
            QtWidgets.QMessageBox.information(self, 'Record', f'Нет данных.')

    def saveRec(self, login, record):
        con = sqlite3.connect('Users.db')
        cur = con.cursor()

        cur.execute(f'SELECT * FROM Records WHERE name = "{login}"')
        value = cur.fetchall()
        if not value[0][2]:
            cur.execute(f"UPDATE Records SET record = '{record}' WHERE name = '{login}'")

        con.commit()
        cur.close()
        con.close()

