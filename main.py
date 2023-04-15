import os
import face_recognition
import cv2
import psycopg2
from PIL import Image
import io



def compare_faces(img1_path, img2_path):
    try:
        # Загрузка первого изображения и получение его кодировки
        img1 = face_recognition.load_image_file(img1_path)
        img1_encoding = face_recognition.face_encodings(img1)[0]

        # Загрузка второго изображения и получение его кодировки
        img2 = face_recognition.load_image_file(img2_path)
        img2_encoding = face_recognition.face_encodings(img2)[0]

        # Сравнение кодировок двух лиц и запись результата
        result = face_recognition.compare_faces([img1_encoding], img2_encoding)

        # Вывод результата
        if result[0]:
            print("Вход разрешен")
        else:
            print("Лицо не распознано")

    except:
        print("Невозможно распознать лицо, проверьте качество съёмки")
    os.remove("image/result.jpg")
    os.remove("image/screenshot.jpg")


def main():
    #Создаем соединение с базой данных
    conn = psycopg2.connect(
        dbname = "photo",
        user = "postgres",
        password = "Pudge",
        host = "localhost",
        port = "5432")
    # Создаем курсор для выполнения запросов к базе данных
    cur = conn.cursor()

    # Получаем все ID из таблицы "фотографии"
    cur.execute("SELECT id_user FROM Users")
    ids = cur.fetchall()

    # Проходим по каждому ID и получаем фотографию
    for id in ids:
        cur.execute("SELECT photo FROM Users WHERE id_user = %s", (id,))
        row = cur.fetchone()

    # Если фотография найдена, то открываем ее с помощью библиотеки Pillow
    if row is not None:
        image_binary = row[0]
        image = Image.open(io.BytesIO(image_binary))
        image.save("image/result.jpg")


    # Вызываем функцию сравнения лиц
    compare_faces("image/result.jpg", "image/screenshot.jpg")

    # Закрываем соединение с базой данных
    conn.close()


def webcam():

    cap = cv2.VideoCapture(0)


    while cap.isOpened():


        ret, frame = cap.read()


        if ret:


            cv2.imshow('Webcam', frame)


            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


    cv2.imwrite("image/screenshot.jpg", frame)


    cap.release()
    cv2.destroyAllWindows()


print("1. Распознование лиц \n2. Добавить лицо в базу данных")
x = int(input("Выберите операцию: "))
if x == 1:
   webcam()
   main()
elif x == 2:
    import Upload_face
    Upload_face
else:
    print("Выберите корректный вариант")