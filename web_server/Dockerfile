# Используем базовый образ Python 3.9
FROM python:3.9

# Устанавливаем зависимости
RUN pip install fastapi requests uvicorn httpx

# Создаем рабочий каталог внутри контейнера
WORKDIR /app

# Копируем файл с вашим кодом в контейнер
COPY main.py /app/main.py

# Экспонируем порт 8000, который использует FastAPI
EXPOSE 8000

# Запускаем FastAPI-сервис с помощью Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
