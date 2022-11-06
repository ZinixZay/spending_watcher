from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox
from PyQt5.uic import loadUi

import sys
import traceback

from database_commands import *
from axuilary_staff import *
from logical_part import *


class MainScreen(QMainWindow):
    def __init__(self):
        super(MainScreen, self).__init__()
        loadUi("screens/screen_1.ui", self)
        self.initUI()

    def initUI(self):
        self.add_r_but.clicked.connect(self.new_expense)
        self.add_d_but.clicked.connect(self.new_income)
        self.amount_l.setText(str(get_current_amount()))

    @staticmethod
    def new_expense() -> NoReturn:
        """
        Changes active screen from menu to expense creating
        :return: NoReturn
        """
        menu.hide()
        spend_form.show()
        spend_form.value_line.setText('')
        spend_form.description_line.setText('')

    @staticmethod
    def new_income() -> NoReturn:
        """
        Changes active screen from menu to income form
        :return: NoReturn
        """
        menu.hide()
        income_form.show()
        income_form.value_line.setText('')
        income_form.description_line.setText('')


class IncomeForm(QWidget):
    def __init__(self):
        super(IncomeForm, self).__init__()
        loadUi("screens/screen_3.ui", self)
        self.initUI()

    def initUI(self):
        self.add_but.clicked.connect(self.get_content)

    @staticmethod
    def create_error_messagebox(title: str, text: str) -> NoReturn:
        msg_box = QMessageBox()
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.exec_()

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
            record = IncomeRecord(value=val, description=des)
            record.submit_record()
            menu.amount_l.setText(str(get_current_amount()))

        except RecordValueError as e:
            self.create_error_messagebox(str(e), 'Введите числовое значение суммы, которую вы получили')

        except RecordDescriptionError as e:
            self.create_error_messagebox(str(e), 'Напишите, за что вы получили деньги')

        except Exception:
            self.create_error_messagebox(str(e), 'Произошла непредвиденная ошибка, попробуйте еще раз')

        else:
            msg_box = QMessageBox()
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setWindowTitle('Запись добавлена')
            msg_box.setText('Ваша запись была успешна добавлена')
            msg_box.exec_()
            menu.show()
            income_form.hide()


class SpendForm(QWidget):
    def __init__(self):
        super(SpendForm, self).__init__()
        loadUi("screens/screen_2.ui", self)
        self.initUI()

    def initUI(self):
        self.add_but.clicked.connect(self.get_content)

    @staticmethod
    def create_error_messagebox(title: str, text: str) -> NoReturn:
        """
        Shows filled pattern of an error message
        :param title: title of the error message
        :param text: text of the error message
        :return: NoReturn
        """
        msg_box = QMessageBox()
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.exec_()

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
            menu.amount_l.setText(str(get_current_amount()))

        except RecordValueError as e:
            self.create_error_messagebox(str(e), 'Введите числовое значение суммы, которую вы потратили на покупку')

        except RecordDescriptionError as e:
            self.create_error_messagebox(str(e), 'Напишите, на что вы потратили деньги')

        except Exception:
            self.create_error_messagebox(str(e), 'Произошла непредвиденная ошибка, попробуйте еще раз')

        else:
            msg_box = QMessageBox()
            msg_box.setStandardButtons(QMessageBox.Ok)
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setWindowTitle('Запись добавлена')
            msg_box.setText('Ваша запись была успешна добавлена')
            msg_box.exec_()
            menu.show()
            spend_form.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    menu = MainScreen()
    spend_form = SpendForm()
    income_form = IncomeForm()
    menu.show()
    sys.exit(app.exec())
