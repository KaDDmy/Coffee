import sys
import sqlite3
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QTableWidget
from PyQt6.QtWidgets import QTableWidgetItem, QWidget, QMessageBox


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


class Edit_Window(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)

        self.pushButton.clicked.connect(self.save_record)

        self.connection = sqlite3.connect('coffee.sqlite')

    def save_record(self):
        try:
            coffee_id = self.spinBox_3.text().strip()
            name = self.lineEdit.text()
            roast = self.comboBox_2.currentText()
            ground_or_beans = self.comboBox.currentText()
            flavor = self.lineEdit_2.text()
            price = int(self.spinBox.text())
            volume = int(self.spinBox_2.text())

            if not name or not roast or not price or not volume:
                QMessageBox.warning(self, "Ошибка", "Заполните все обязательные поля!")
                return

            cursor = self.connection.cursor()

            if self.checkBox.isChecked():
                    cursor.execute(
                        """
                        INSERT INTO coffee (Название_сорта, Степень_обжарки, Молотый_или_в_зернах,
                            Описание_вкуса, Цена, Объем_упаковки)
                        VALUES (?, ?, ?, ?, ?, ?)
                        """,
                        (name, roast, ground_or_beans, flavor, float(price), int(volume))
                    )
            else:
                if coffee_id != '0':
                    cursor.execute(
                        """
                        UPDATE coffee
                        SET Название_сорта = ?, Степень_обжарки = ?, Молотый_или_в_зернах = ?,
                            Описание_вкуса = ?, Цена = ?, Объем_упаковки = ?
                        WHERE ID = ?
                        """,
                        (name, roast, ground_or_beans, flavor, float(price), int(volume), int(coffee_id))
                    )
                else:
                    QMessageBox.information(self, 'Ошибка', 'Вы не выбрали тип записи')
                    return

            self.connection.commit()
            QMessageBox.information(self, "Успех", "Запись успешно сохранена!")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {e}")

    def closeEvent(self, event):
        self.connection.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CoffeeApp()
    ex = Edit_Window()
    window.show()
    ex.show()
    sys.exit(app.exec())