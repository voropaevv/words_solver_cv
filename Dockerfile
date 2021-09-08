# Задаем базовый образ
FROM python:3.7-slim

# Устанавливаем необходимые зависимости
RUN apt-get update && \
    apt-get install -yq libgtk2.0-dev && \
    apt-get install -yq libtesseract-dev  && \
    apt-get install -yq tesseract-ocr && \
    pip install --upgrade pip

# Копируем языковой файл для tesseract-ocr в нужное место
COPY rus.traineddata /usr/share/tesseract-ocr/4.00/tessdata/

# Устанавливаем постоянные переменные среды
ENV PROJECT_ROOT /app
ENV IMAGE_ROOT /images

# Создаем дополнительные директории
RUN mkdir $PROJECT_ROOT $IMAGE_ROOT

# Копируем код из локального контекста в рабочую директорию образа
COPY . $PROJECT_ROOT

# Задаём текущую рабочую директорию
WORKDIR $PROJECT_ROOT

# Установка необходимых модулей и удаление лишего файла
RUN pip install -r requirements.txt --no-cache-dir && \
    rm rus.traineddata

# Запуск основной программы с отключением буферизации stdout 
CMD ["python3", "-u", "./main.py"]