import os 
from socket import *
from PIL import Image
from io import BytesIO


def image_to_binary(image):
    """
    Преобразует изображение в бинарную строку

    Параметры
    ---------
        image : PIL.Image.Image
            Исходное изображение

    Возвращает
    ----------
        bytes
            Изображение в бинарном представлении

    """
    # инициализируем бинарный поток BytesIO
    with BytesIO() as output:
        # сохраняем в изображение в памяти
        image.save(output, format='PNG')
        # получаем массив байтов
        binary_image = output.getvalue()
        return binary_image


def main():
    # указываем ip хоста, на котором запущен docker 
    ip = "localhost"
    # порт, через который взаимодействует с сервером
    port = 50000
    # адрес сервера
    server_address = (ip, port)
    # создаем экземпляр класса socket
    # AF_INET - используем протокол версии IPv4
    # SOCK_STREAM - использование протокола TCP
    socket_ = socket(AF_INET, SOCK_STREAM)
    # подключаемся к серверу
    socket_.connect(server_address)
    # открываем изображение
    image = Image.open("images/screenshot_example_1.png")
    # конвертируем изображение в бинарный формат
    binary_image = image_to_binary(image)
    # отправляем бинарное изображение серверу
    socket_.sendall(binary_image)
    print("Sent photo")
    # закрываем соединение с сервером
    socket_.close()
    # создаем экземпляр класса socket
    socket_ = socket(AF_INET, SOCK_STREAM)
    # пытаемся подключиться к серверу
    connect = False
    while not connect:
        try:            
            socket_.connect(server_address)
            connect = True
        except Exception:
            pass
    # получаем сообщение
    text = socket_.recv(65536)
    print('Received text')
    # выводим найденные слова
    print(text.decode())
    # закрываем соединение с сервером
    socket_.close()


if __name__ == "__main__":
    main()
