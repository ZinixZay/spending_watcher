from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox
from PyQt5.uic import loadUi

import sys
import traceback

from database_commands import *
from axuilary_classes import *


class MainScreen(QMainWindow):
    def __init__(self):
        super(MainScreen, self).__init__()
        loadUi("screens/screen_1.ui", self)
        self.initUI()

    def initUI(self):
        self.add_but.clicked.connect(self.new_expense)

    @staticmethod
    def new_expense() -> NoReturn:
        menu.hide()
        form.show()
        form.value_line.setText('')
        form.description_line.setText('')


class SpendForm(QWidget):
    def __init__(self):
        super(SpendForm, self).__init__()
        loadUi("screens/screen_2.ui", self)
        self.initUI()

    def initUI(self):
        self.add_but.clicked.connect(self.get_content)

    def get_content(self) -> NoReturn:
        """
        adds parametres from user to a record and tries to submit it
        :return: NoReturn
        """
        try:

            try:
                val = int(self.value_line.text())
            except ValueError:
                raise RecordValueError('Введено не числовое значение')
            if val <= 0:
                raise RecordValueError('Введено неверное числовое значение')

            des = str(self.description_line.text())
            if des == '':
                raise RecordDescriptionError('Пустое поле содержания покупки')

            record = SpendRecord(value=val, description=des)
            record.submit_record()

        except RecordValueError as e:
            msg_box = QMessageBox()
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setWindowTitle(str(e))
            msg_box.setText('Введите числовое значение суммы, которую вы потратили на покупку')
            msg_box.exec_()

        except RecordDescriptionError as e:
            msg_box = QMessageBox()
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setWindowTitle(str(e))
            msg_box.setText('Напишите, на что вы потратили деньги')
            msg_box.exec_()

        except Exception:
            msg_box = QMessageBox()
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setWindowTitle('Непредвиденная ошибка')
            msg_box.setText('Произошла непредвиденная ошибка, попробуйте еще раз')
            msg_box.exec_()

        else:
            msg_box = QMessageBox()
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setWindowTitle('Запись добавлена')
            msg_box.setText('Ваша запись была успешна записана')
            msg_box.exec_()
            menu.show()
            form.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    menu = MainScreen()
    form = SpendForm()
    menu.show()
    sys.exit(app.exec())
