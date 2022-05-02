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
    rezultat = []
    mycursor.execute(
        "SELECT NumePrenume FROM facedetection ")
    myresult = mycursor.fetchall()
    lista_nume_DB = [item for t in myresult for item in t]
    for i in range(len(lista_nume_DB)):
        sql = "SELECT NrMatricol FROM facedetection WHERE NumePrenume = %s"
        val = tuple(map(str, lista_nume_DB[i].split(', ')))
        # print(val)
        mycursor.execute(sql, val)
        myresult = mycursor.fetchall()
        rezultat += myresult
        # print(rezultat)

    lista_nrMatricol = [item for t in rezultat for item in t]
    # print(lista_nrMatricol)

    today = str(date.today())
    for x in range(len(lista_nume_DB)):
        querry = "INSERT INTO tabelprezenta (NumePrenume, NrMatricol, Data) VALUES (%s, %s, %s)"
        val = (lista_nume_DB[x], lista_nrMatricol[x], today)
        # print(lista_nume_DB[x], lista_nrMatricol[x])
        mycursor.execute(querry, val)
        mydb.commit()

    print("Datele s-au adaugat cu succes!")


if __name__ == '__main__':
    insertData()
