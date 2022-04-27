import gc
import json
import os
from datetime import date
import cv2
import face_recognition
import mysql.connector
import numpy as np
from dataInsert import insertData


def aplicatePrezenta():
    today = str(date.today())  # preluam data curenta, pentru a crea un fisier
    parent_directory = r"C:\Users\viore\Desktop\proiect_practica"  # specificam calea absoluta unde o sa cream fisierul
    dir_create = os.path.join(parent_directory, today)  # realizam calea
    if os.path.exists(dir_create):  # daca directorul exista, afisam un mesaj corespunzator
        print("Directorul exista!")
    else:  # daca nu exista il cream si afisam un mesaj
        os.mkdir(dir_create)
        insertData()
        print("Directorul a fost creat cu succes")

    mydb = mysql.connector.connect(  # accesam baza de date
        host="localhost",
        user="root",
        password="",
        database="mydatabase"
    )

    mycursor = mydb.cursor()  # obiect de tip cursor pentru a executa interogarile

    with open("imagini_codificate.json", "r") as read_file:
        decodedArray = json.load(read_file)
    lista_nume_DB = list(decodedArray.keys())
    listaFete_codificateDB = [tuple(codificare) for codificare in decodedArray.values()]

    # video_capture = cv2.VideoCapture(0)  # capturam camera video
    video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    #  liste unde se vor stoca informatii din fluxul video
    fetele_gasite = []
    fetele_gasite_codificate = []
    numele_fetelor_gasite = []
    process_this_frame = True

    while True:
        # preluam frame cu frame din video
        ret, frame = video_capture.read()
        # relizam o redimensionare a capturii, pentru a face recunoasterea faciala mai rapida
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        # se converteste imaginea de la BGR, pe care OpenCV-ul o utilizeaza la RGB deoarece modulul face_recognition il
        # utilizeaza
        rgb_small_frame = small_frame[:, :, ::-1]
        # Procesam frame cu frame
        if process_this_frame:
            # Gasim fetele, pe care le codificam
            fetele_gasite = face_recognition.face_locations(rgb_small_frame)
            fetele_gasite_codificate = face_recognition.face_encodings(rgb_small_frame, fetele_gasite)
            numele_fetelor_gasite = []
            for fata_codificata in fetele_gasite_codificate:
                # verificam daca fetele din fluxul video se regasesc in baza de date
                matches = face_recognition.compare_faces(listaFete_codificateDB, fata_codificata)
                # returnează o listă booleană (true/false) care indică dacă o față găsita este regăsită in baza de date
                name = "Unknown"  # presupunem ca nu
                face_distances = face_recognition.face_distance(listaFete_codificateDB, fata_codificata)
                # compară captura din fluxul video și imaginea din baza de date returnând un numpy array, în care se
                # regăsesc distanțe euclidiene.
                best_match_index = np.argmin(face_distances)
                # returnează indicele celei mai mici valori dintr-un numpy array.
                if matches[best_match_index]:  # in cazul in care se regaseste, adaugam numele in baza de date
                    name = lista_nume_DB[best_match_index]
                    # aici inseram imaginea in fisier
                    nume = name + ".jpg"  # numele imaginei
                    imgscr = today + "\\" + nume

                    sql = "SELECT NrMatricol FROM facedetection WHERE NumePrenume = %s"
                    val = tuple(map(str, name.split(', ')))
                    mycursor.execute(sql, val)
                    myresult = mycursor.fetchall()
                    matricol = [item for t in myresult for item in t]
                    mat = "" + matricol[0]

                    sql = "UPDATE tabelprezenta SET Prezenta = %s, LocatieImagine = %s \
                    WHERE NumePrenume = %s AND NrMatricol = %s"
                    val = ("1", imgscr, name, mat)
                    mycursor.execute(sql, val)
                    mydb.commit()

                    img_path = os.path.join(dir_create, nume)
                    os.chdir(dir_create)  # schimbam directorul curent, cu cel unde  o sa salvam imaginile
                    if not os.path.exists(img_path):  # verificam daca imagina exsita
                        cv2.imwrite(nume, frame)
                numele_fetelor_gasite.append(name)

        process_this_frame = not process_this_frame  # incheiem prelucrarea frame-ului curent

        # afisam rezultatul
        for (top, right, bottom, left), name in zip(fetele_gasite, numele_fetelor_gasite):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # se deseneaza un patrat in jurul fetei
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 128, 0), 2)

            # adaugam labe-ul cu numele persoanei
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 128, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # afisam in fluxul video
        cv2.imshow('Video', frame)

        # se apasa tasta 'q' pentru a iesi din program
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    print("Prezenta a fost adaugata studentiilor: ", numele_fetelor_gasite)
    # inchidem camera si fereastra
    mycursor.close()
    video_capture.release()
    del video_capture
    gc.collect()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    aplicatePrezenta()
