import cv2
from socket import *
from words_solver import WordsSolver
from cv_recognition import letters_recognition


def write_image_from_client(client, buf=65536):
    """
    Записывает в файл изображение, переданное в бинарном формате от клиента

    Параметры
    ---------
        client : socket.socket
        	Сокет клиента, подключенного к серверу
            

    Возвращает
    ----------
        None

    """	
    with open('images/screenshot.png', 'wb') as image_file:
        try:
            while True:
                # получаем изображение от клиента
                image = client.recv(buf)
                # если все части фото присланы, то выходим из цикла
                if not image:
                    break
                image_file.write(image)
        finally:
            # отключаем соединение с клиентом
            client.close()


def main():
    # резервируем все интерфейсы на локальной машине
    ip = '0.0.0.0'
    # резервируем 50000 порт
    port = 50000
    # адрес сервера
    server_address = (ip, port)
    # создаем экземпляр класса socket
    # AF_INET - используем протокол версии IPv4
    # SOCK_STREAM - использование протокола TCP
    socket_ = socket(AF_INET, SOCK_STREAM)
    # изолирование порта на локальной машине
    socket_.bind(server_address)
    # обрабатываем только 1 соединение
    socket_.listen(1)
    # сервер работает, пока не поступит сигнал прерывания
    while True:
        try:
            print("Waiting to receive image...")
            # ждем подключения клиента
            client, client_address = socket_.accept()
        except KeyboardInterrupt:
        	# закрываем сокетное соединение
            socket_.close()
            break
        else:
            write_image_from_client(client)
            print('Screenshot uploaded!')
            # загрузка изображения по указанному пути
            image = cv2.imread('images/screenshot.png')
            letters = letters_recognition(image)
            print('Letters recognized!')
            solver = WordsSolver(letters)
            solver.find_words()
            # множество найденных слов
            words = solver.found_words
            print('Words found!')
            # сортировка слов в порядке убывания их длины
            words = sorted(words, key=lambda item: len(item), reverse=True)
            # формируем сообщение
            message = 'Нашел следующие слова:\n'
            message += '  '.join(words)
            # подключаем клиента для отправки изображения
            client, client_address = socket_.accept()
            client.sendall(message.encode())
            print('Words sent!')
            client.close()


if __name__ == "__main__":
    main()
