from PyQt5 import QtWidgets


class CheckStr(QtWidgets.QDialog):
    def check(self, text_1, text_2):
        errors = 0
        num = 0
        for sim in text_2:
            if (num == len(text_1) + 1) or (num == len(text_2) + 1):
                break
            if sim != text_1[num]:
                errors += 1
            num += 1
        return errors