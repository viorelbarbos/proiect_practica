import json
import os
from datetime import date
import cv2
import face_recognition
import mysql.connector
import numpy as np
from dataInsert import insertData


def aplicatePrezenta():
    current_day = str(date.today())  # preluam data curenta, pentru a crea un fisier
    parent_directory = r"C:\Users\viore\OneDrive\Desktop\proiect_practica"  # specificam calea absoluta unde o sa cream fisierul
    dir_create = os.path.join(parent_directory, current_day)  # realizam calea
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
    students_names_fromDB = list(decodedArray.keys())
    students_coded_face_fromDB = [tuple(codificare) for codificare in decodedArray.values()]


    # video_capture = cv2.VideoCapture(0)  # capturam camera video
    video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    #  liste unde se vor stoca informatii din fluxul video
    students_detected_faces = []
    students_detected_faces_coded = []
    students_names_found = []
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
            students_detected_faces = face_recognition.face_locations(rgb_small_frame)
            students_detected_faces_coded = face_recognition.face_encodings(rgb_small_frame, students_detected_faces)
            students_names_found = []
            for student_face_coded in students_detected_faces_coded:
                # verificam daca fetele din fluxul video se regasesc in baza de date
                matches = face_recognition.compare_faces(students_coded_face_fromDB, student_face_coded)
                # returnează o listă booleană (true/false) care indică dacă o față găsita este regăsită in baza de date
                name = "Unknown"  # presupunem ca nu
                face_distances = face_recognition.face_distance(students_coded_face_fromDB, student_face_coded)
                # compară captura din fluxul video și imaginea din baza de date returnând un numpy array, în care se
                # regăsesc distanțe euclidiene.
                best_match_index = np.argmin(face_distances)
                # returnează indicele celei mai mici valori dintr-un numpy array.
                if matches[best_match_index]:  # in cazul in care se regaseste, adaugam numele in baza de date
                    name = students_names_fromDB[best_match_index]
                    # aici inseram imaginea in fisier
                    nume = name + ".jpg"  # numele imaginei
                    imgscr = current_day + "\\" + nume

                    sql = "SELECT NrMatricol FROM facedetection WHERE NumePrenume = %s"
                    val = tuple(map(str, name.split(', ')))
                    mycursor.execute(sql, val)
                    myresult = mycursor.fetchall()
                    rezult = [item for t in myresult for item in t]
                    registration_number = "" + rezult[0]

                    sql = "UPDATE tabelprezenta SET Prezenta = %s, LocatieImagine = %s \
                    WHERE NumePrenume = %s AND NrMatricol = %s AND Data = %s"
                    val = ("1", imgscr, name, registration_number, current_day)
                    mycursor.execute(sql, val)
                    mydb.commit()

                    img_path = os.path.join(dir_create, nume)
                    os.chdir(dir_create)  # schimbam directorul curent, cu cel unde  o sa salvam imaginile
                    if not os.path.exists(img_path):  # verificam daca imagina exsita
                        cv2.imwrite(nume, frame)
                students_names_found.append(name)

        process_this_frame = not process_this_frame  # incheiem prelucrarea frame-ului curent

        # afisam rezultatul
        for (top, right, bottom, left), name in zip(students_detected_faces, students_names_found):
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

    print("Prezenta a fost adaugata studentiilor: ", students_names_found)
    # inchidem camera si fereastra
    mydb.close()
    mycursor.close()
    video_capture.release()
    cv2.destroyAllWindows()
    os.chdir(r"C:\Users\viore\OneDrive\Desktop\proiect_practica")


if __name__ == '__main__':
    aplicatePrezenta()