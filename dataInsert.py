import mysql.connector
from datetime import date


def insertData():
    mydb = mysql.connector.connect(  # accesam baza de date
        host="localhost",
        user="root",
        password="",
        database="mydatabase"
    )
    mycursor = mydb.cursor()

    mycursor.execute(
        "SELECT NumePrenume FROM facedetection ")
    myresult = mycursor.fetchall()
    lista_nume_DB = [item for t in myresult for item in t]

    mycursor.execute(
        "SELECT NrMatricol FROM facedetection ")
    myresult = mycursor.fetchall()
    lista_nrMatricol = [item for t in myresult for item in t]

    today = str(date.today())
    for x in range(len(lista_nume_DB)):
        querry = "INSERT INTO tabelprezenta (NumePrenume, NrMatricol, Data) VALUES (%s, %s, %s)"
        val = (lista_nume_DB[x], lista_nrMatricol[x], today)
        mycursor.execute(querry, val)
        mydb.commit()

    print("Datele s-au adaugat cu succes!")



if __name__ == '__main__':
    insertData()
