from PyQt5 import QtWidgets, QtChart, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtChart import QPieSeries, QChartView, QChart
from PyQt5.QtCore import Qt

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
        self.setWindowTitle('Spending watcher')
        self.add_r_but.clicked.connect(self.new_expense)
        self.add_d_but.clicked.connect(self.new_income)
        self.stat_but.clicked.connect(self.show_chart)
        self.history_but.clicked.connect(self.show_history)
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

    @staticmethod
    def show_chart() -> NoReturn:
        """
        Changes active screen from menu to chart screen
        :return: NoReturn
        """
        menu.hide()
        chart_pie = MyChart(generate_chart_data())
        chart_view = QtChart.QChartView(chart_pie)
        chart_view.setRenderHint(QtGui.QPainter.Antialiasing)
        chart.setCentralWidget(chart_view)
        chart.show()

    @staticmethod
    def show_history() -> NoReturn:
        """
        Changes active screen from menu to history
        :return: NoReturn
        """
        menu.hide()
        history.update_result()
        history.show()


class IncomeForm(QWidget):
    def __init__(self):
        super(IncomeForm, self).__init__()
        loadUi("screens/screen_3.ui", self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Spending watcher')
        self.add_but.clicked.connect(self.get_content)
        self.back_but.clicked.connect(self.back)

    @staticmethod
    def back() -> NoReturn:
        """
        Changes active screen from income form to menu
        :return: NoReturn
        """
        menu.show()
        income_form.hide()

    @staticmethod
    def create_error_messagebox(title: str, text: str) -> NoReturn:
        """
        Generates and shows error message
        :param title: title of an error
        :param text: error's description
        :return: NoReturn
        """
        msg_box = QMessageBox()
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.exec_()

    def keyPressEvent(self, event) -> NoReturn:
        """
        Catches pushed keyboard buttons and marshrouts them
        :param event: compulsory argument
        :return: NoReturn
        """
        if event.key() == Qt.Key_Escape:
            menu.show()
            income_form.hide()

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
        self.setWindowTitle('Spending watcher')
        self.add_but.clicked.connect(self.get_content)
        self.back_but.clicked.connect(self.back)

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

    @staticmethod
    def back() -> NoReturn:
        """
        Changes active screen from income form to menu
        :return: NoReturn
        """
        menu.show()
        spend_form.hide()

    def keyPressEvent(self, event) -> NoReturn:
        """
        Catches pushed keyboard buttons and marshrouts them
        :param event: compulsory argument
        :return: NoReturn
        """
        if event.key() == Qt.Key_Escape:
            menu.show()
            spend_form.hide()

    def get_content(self) -> NoReturn:
        """
        Adds parametres from user to a record and tries to submit it
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
            self.create_error_messagebox(str(e), 'Напишите, где вы потратили деньги')

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


class ChartView(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(ChartView, self).__init__(parent)
        self.setFixedSize(QtCore.QSize(700, 400))

        datas = generate_chart_data()
        chart = MyChart(datas)
        self.setWindowTitle('Spending watcher')

        chart_view = QtChart.QChartView(chart)
        chart_view.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setCentralWidget(chart_view)

    def keyPressEvent(self, event) -> NoReturn:
        """
        Catches pushed keyboard buttons and marshrouts them
        :param event: compulsory argument
        :return: NoReturn
        """
        if event.key() == Qt.Key_Escape:
            menu.show()
            chart.hide()


class MyChart(QtChart.QChart):

    def __init__(self, datas, parent=None):
        super(MyChart, self).__init__(parent)
        self._datas = generate_chart_data()

        self.legend().hide()
        self.setAnimationOptions(QtChart.QChart.SeriesAnimations)

        self.outer = QtChart.QPieSeries()
        self.inner = QtChart.QPieSeries()
        self.outer.setHoleSize(0.35)
        self.inner.setPieSize(0.35)
        self.inner.setHoleSize(0.3)

        self.set_outer_series()
        self.set_inner_series()

        self.addSeries(self.outer)
        self.addSeries(self.inner)

    def set_outer_series(self) -> NoReturn:
        """
        Sorts data into the chart
        :return: NoReturn
        """
        slices = list()
        for data in self._datas:
            slice_ = QtChart.QPieSlice(data.name, data.value)
            slice_.setLabelVisible()
            slice_.setColor(data.primary_color)
            slice_.setLabelBrush(data.primary_color)

            slices.append(slice_)
            self.outer.append(slice_)
        for slice_ in slices:
            color = 'black'
            if slice_.percentage() > 0.1:
                slice_.setLabelPosition(QtChart.QPieSlice.LabelInsideHorizontal)
                color = 'white'
            label = "<p align='center' style='color:{}'>{}<br>{}%</p>".format(
                color,
                slice_.label(),
                round(slice_.percentage()*100, 2)
                )
            slice_.setLabel(label)

    def set_inner_series(self) -> NoReturn:
        """
        Sets chart style
        :return: NoReturn
        """
        for data in self._datas:
            slice_ = self.inner.append(data.name, data.value)
            slice_.setColor(data.secondary_color)
            slice_.setBorderColor(data.secondary_color)


class History(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("screens/screen_4.ui", self)
        self.setWindowTitle('Spending watcher')
        self.update_result()

    def keyPressEvent(self, event) -> NoReturn:
        """
        Catches pushed keyboard buttons and marshrouts them
        :param event: compulsory argument
        :return: NoReturn
        """
        if event.key() == Qt.Key_Escape:
            menu.show()
            history.hide()

    def update_result(self) -> NoReturn:
        """
        Updates table widget
        :return: NoReturn
        """
        result = get_history()
        if not result:
            return
        columns = ['Дата', 'Где потратили', "Сумма"]
        self.tableWidget.setHorizontalHeaderLabels(columns)
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]) - 1)
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                if j == 0:
                    continue
                self.tableWidget.setItem(i, j - 1, QTableWidgetItem(str(val)))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    menu = MainScreen()
    spend_form = SpendForm()
    income_form = IncomeForm()
    chart = ChartView()
    history = History()

    menu.show()
    sys.exit(app.exec())
