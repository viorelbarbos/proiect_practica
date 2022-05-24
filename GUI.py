import os.path
import sys
import mysql.connector
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLineEdit, QMessageBox, QLabel
from faceDetection3 import aplicatePrezenta
from datetime import date

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="mydatabase"
)

mycursor = mydb.cursor()


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.button = QPushButton('Afisare prezente student', self)
        self.buttonRP = QPushButton('Raport prezenta', self)
        self.buttonFD = QPushButton('Realizare prezenta', self)
        self.buttonAF = QPushButton('Afisare nume studenti', self)
        self.textbox = QLineEdit(self)
        self.label1 = QLabel(self)
        self.title = 'Aplicatie pentru prezenta automata'
        self.left = 500
        self.top = 250
        self.width = 400
        self.height = 400
        self.initUI()
        # self.setStyleSheet("color:rgb(204, 204, 204)")

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
        self.buttonRP.move(140, 20)

        # connect button to function on_click
        self.button.resize(150, 25)
        self.button.clicked.connect(self.on_click)
        self.show()

        self.buttonRP.clicked.connect(self.generareRaport)
        self.buttonRP.hide()

        self.buttonFD.clicked.connect(self.faceDetect)
        self.show()

        self.buttonAF.resize(150, 25)
        self.buttonAF.clicked.connect(self.afisare)
        self.show()

    @pyqtSlot()
    def on_click(self):
        textboxValue = self.textbox.text()
        sql = "SELECT NumePrenume, NrMatricol, Prezenta, Data FROM tabelprezenta WHERE NumePrenume = %s"
        val = tuple(map(str, textboxValue.split(', ')))
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        student = [item for t in myresult for item in t]
        if student:
            present = ""
            for i in range(2, len(student) - 1, 4):
                present += str(student[i]) + " / " + str(student[i + 1]) + " || "

            QMessageBox.question(self, 'Prezentele studentului: ', "Nume, prenume: " + student[0] + \
                                 "\nNumar matricol: " + student[1] + "\nPrezenta/Data: " + present, QMessageBox.Ok)
        else:
            QMessageBox.question(self, 'ERROR', 'Ati introdus un nume INVALID', QMessageBox.Ok)
        self.textbox.setText("")

    def faceDetect(self):
        aplicatePrezenta()
        self.buttonRP.show()
        print("S-a realizat prezenta")

    def afisare(self):
        sql = "SELECT NumePrenume FROM facedetection"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        student = [item for t in myresult for item in t]
        name = ""
        for i in range(len(student)):
            name += student[i] + "\n"
        QMessageBox.question(self, 'Studenti', name, QMessageBox.Ok)

    def generareRaport(self):
        current_day = str(date.today())
        sql = "SELECT NumePrenume, NrMatricol, Prezenta, Data FROM tabelprezenta WHERE Data = %s "
        val = tuple(map(str, current_day.split(', ')))
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()

        completePath = os.path.join("rapoarte", "RAPORT_PREZENTE_" + current_day + ".txt")
        file = open(completePath, "w+")
        for student in myresult:
            if int(student[2] == 1):
                file.write(
                    "Studentul/Studenta {st}, avand numarul matricol {mat}, a fost prezent in data de {dat} ".format(
                        st=student[0], mat=student[1], dat=student[3]))
            else:
                file.write(
                    "Studentul/Studenta  {st}, avand numarul matricol {mat}, NU a fost prezent in data de {dat} ".format
                    (st=student[0],
                     mat=student[1],
                     dat=student[3]))
            file.write("\n\n")
        file.close()
        print("Raportul cu studentii prezenti a fost realizat!  Se poate accesa din " + completePath)
        QMessageBox.question(self, 'ERROR', "Raportul cu studentii prezenti a fost realizat!  Se poate accesa din " +
                             completePath, QMessageBox.Ok)

        self.buttonRP.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
