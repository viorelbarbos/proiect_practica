from json import JSONEncoder
import face_recognition
import mysql.connector
import numpy
import json


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


mydb = mysql.connector.connect(  # accesam baza de date
    host="localhost",
    user="root",
    password="",
    database="mydatabase"
)

mycursor = mydb.cursor()  # obiect de tip cursor pentru a executa interogarile

mycursor.execute(
    "SELECT NumePrenume FROM facedetection ")  # comanda pentru a prelua Numele studentului din baza de date
myresult = mycursor.fetchall()
lista_nume_DB = [item for t in myresult for item in t]  # intrucat se preia ca si un tuplu, o convertim la lista

mycursor.execute(
    "SELECT locatieImagine FROM facedetection ")  # comanda pentru a prelua path-ul pentru imaginea studentului
myresult = mycursor.fetchall()
lista_imagini = [item for t in myresult for item in t]  # intrucat se preia ca si un tuplu, o convertim la lista

listaFete_codificateDB = []  # codificam imaginile preluate din baza de date
for i in range(len(lista_imagini)):
    imagine = lista_imagini[i]  # luam fiecare imagine pe rand si o codificam
    imagine_incarcata = face_recognition.load_image_file(imagine)
    imagine_codificata = face_recognition.face_encodings(imagine_incarcata)[0]
    listaFete_codificateDB.append(imagine_codificata)  # adaugam imaginile codificate la o lista


dicti = {lista_nume_DB[i]: listaFete_codificateDB[i] for i in range(len(lista_nume_DB))}
print(dicti)

with open("imagini_codificate.json", "w") as write_file:
    json.dump(dicti, write_file, cls=NumpyArrayEncoder)
