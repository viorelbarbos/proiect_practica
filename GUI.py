import sys
import mysql.connector
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLineEdit, QMessageBox, QLabel
from faceDetection3 import aplicatePrezenta

mydb = mysql.connector.connect(  # accesam baza de date
    host="localhost",
    user="root",
    password="",
    database="mydatabase"
)

mycursor = mydb.cursor()  # obiect de tip cursor pentru a executa interogarile


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.button = QPushButton('Afisare prezente student', self)
        self.buttonFD = QPushButton('Realizare prezenta', self)
        self.buttonAF = QPushButton('Afisare nume studenti', self)
        self.textbox = QLineEdit(self)
        self.label1 = QLabel(self)
        self.title = 'Aplicatie pentru prezenta automana'
        self.left = 500
        self.top = 250
        self.width = 400
        self.height = 400
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.label1.move(20, 80)
        self.label1.setText("Introduceti studentul: ")

        # Create textbox
        self.textbox.move(20, 110)
        self.textbox.resize(180, 30)

        # Create a button in the window
        self.button.move(210, 115)
        self.buttonFD.move(20, 20)
        self.buttonAF.move(20, 60)

        # connect button to function on_click
        self.button.resize(150, 25)
        self.button.clicked.connect(self.on_click)
        self.show()

        self.buttonFD.clicked.connect(self.faceDetect)
        self.show()

        self.buttonAF.resize(150, 25)
        self.buttonAF.clicked.connect(self.afisare)
        self.show()

    @pyqtSlot()
    def on_click(self):
        textboxValue = self.textbox.text()
        sql = "SELECT NumePrenume, NrMatricol, Prezenta, Data FROM tabelprezenta WHERE NumePrenume = %s "
        val = tuple(map(str, textboxValue.split(', ')))
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        student = [item for t in myresult for item in t]
        if student:
            prezenta = ""
            for i in range(2, len(student) - 1, 4):
                prezenta += str(student[i]) + " / " + str(student[i + 1]) + " || "

            QMessageBox.question(self, 'Prezentele studentului: ', "Nume, prenume: " + student[0] + \
                                 "\nNumar matricol: " + student[1] + "\nPrezenta/Data: " + prezenta, QMessageBox.Ok)
        else:
            QMessageBox.question(self, 'ERROR', 'Ati introdus un nume INVALID', QMessageBox.Ok)
        self.textbox.setText("")

    def faceDetect(self):
        aplicatePrezenta()
        self.buttonFD.hide()

    def afisare(self):
        sql = "SELECT NumePrenume FROM facedetection"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        student = [item for t in myresult for item in t]
        nume = ""
        for i in range(len(student)):
            nume += student[i] + "\n"
        QMessageBox.question(self, 'Studenti', nume, QMessageBox.Ok)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
