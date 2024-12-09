import sys
import sqlite3
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QTableWidget
from PyQt6.QtWidgets import QTableWidgetItem, QWidget


class CoffeeApp(QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi('main.ui', self)
        self.setWindowTitle("Информация о кофе")
        self.load_data()

    def load_data(self):
        connection = sqlite3.connect("coffee.sqlite")
        cursor = connection.cursor()

        cursor.execute("""SELECT Название_сорта, Степень_обжарки,
        Молотый_или_в_зернах, Описание_вкуса, Цена,
        Объем_упаковки FROM Coffee""")
        rows = cursor.fetchall()

        self.table.setRowCount(len(rows))
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Название сорта",
                                              "Степень обжарки",
                                              "Молотый/Зерна",
                                              "Описание вкуса",
                                              "Цена",
                                              "Объем упаковки"])

        for row_index, row_data in enumerate(rows):
            for column_index, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))
                self.table.setItem(row_index, column_index, item)

        connection.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec())