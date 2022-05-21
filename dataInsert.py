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
    rezult = []
    mycursor.execute(
        "SELECT NumePrenume FROM facedetection ")
    myresult = mycursor.fetchall()
    students_names_fromDB = [item for t in myresult for item in t]
    for i in range(len(students_names_fromDB)):
        sql = "SELECT NrMatricol FROM facedetection WHERE NumePrenume = %s"
        val = tuple(map(str, students_names_fromDB[i].split(', ')))
        # print(val)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        rezult += myresult
        # print(rezultat)

    list_registration_number = [item for t in rezult for item in t]
    # print(lista_nrMatricol)

    today = str(date.today())
    for x in range(len(students_names_fromDB)):
        querry = "INSERT INTO tabelprezenta (NumePrenume, NrMatricol, Data) VALUES (%s, %s, %s)"
        val = (students_names_fromDB[x], list_registration_number[x], today)
        # print(lista_nume_DB[x], lista_nrMatricol[x])
        mycursor.execute(querry, val)
        mydb.commit()

    print("Datele s-au adaugat cu succes!")


if __name__ == '__main__':
    insertData()
