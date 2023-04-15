import psycopg2
from PIL import Image
import io
import os
import cv2


def webcam():
    # создаем объект VideoCapture, который представляет собой вебкамеру с номером 0
    cap = cv2.VideoCapture(0)

    # пока видеопоток открыт
    while cap.isOpened():

        # считываем кадр с вебкамеры
        ret, frame = cap.read()

        # если кадр успешно считался
        if ret:

            # выводим кадр на экран
            cv2.imshow('Webcam', frame)

            # ждем нажатия клавиши q для выхода из цикла
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Сохраняем захваченное изображение в файл
    cv2.imwrite("image/screenshot.jpg", frame)

    # Освобождаем вебку и закрываем окно
    cap.release()
    cv2.destroyAllWindows()


webcam()
# Подключаемся к базе данных
conn = psycopg2.connect(
    database="photo",
    user="postgres",
    password="Pudge",
    host="localhost",
    port="5432")

# Создаем курсор для выполнения запросов к базе данных
cur = conn.cursor()

# Открываем изображение с помощью библиотеки Pillow
image = Image.open("image/screenshot.jpg")

# Конвертируем изображение в бинарный формат
image_bytes = io.BytesIO()
image.save(image_bytes, format='JPEG')
image_binary = image_bytes.getvalue()

# Выполняем запрос на добавление записи в таблицу "фото"
cur.execute("INSERT INTO users (photo) VALUES (%s) RETURNING id_user", (image_binary,))

# Получаем значение первичного ключа для новой записи
new_id = cur.fetchone()[0]

# Фиксируем изменения в базе данных
conn.commit()

# Закрываем соединение с базой данных
conn.close()
os.remove("image/screenshot.jpg")