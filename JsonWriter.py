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
students_names_fromDB = [item for t in myresult for item in t]  # intrucat se preia ca si un tuplu, o convertim la lista

mycursor.execute(
    "SELECT locatieImagine FROM facedetection ")  # comanda pentru a prelua path-ul pentru imaginea studentului
myresult = mycursor.fetchall()
students_face_fromDB = [item for t in myresult for item in t]  # intrucat se preia ca si un tuplu, o convertim la lista

students_coded_face_fromDB = []  # codificam imaginile preluate din baza de date
for i in range(len(students_face_fromDB)):
    image = students_face_fromDB[i]  # luam fiecare imagine pe rand si o codificam
    image_loaded = face_recognition.load_image_file(image)
    image_coded = face_recognition.face_encodings(image_loaded)[0]
    students_coded_face_fromDB.append(image_coded)  # adaugam imaginile codificate la o lista


dicti = {students_names_fromDB[i]: students_coded_face_fromDB[i] for i in range(len(students_names_fromDB))}
print(dicti)


with open("imagini_codificate.json", "w") as write_file:
    json.dump(dicti, write_file, cls=NumpyArrayEncoder)
