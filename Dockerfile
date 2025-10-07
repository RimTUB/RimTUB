# Используем официальный образ Python
FROM python:3.11.9-slim

# Устанавливаем рабочую директорию в корне контейнера
WORKDIR /

# создаём виртуальное окружение
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем зависимости, игнорируя root-предупреждение
RUN pip install --root-user-action=ignore -r requirements.txt

# Копируем весь код приложения в корень
COPY . .

# Команда по умолчанию
CMD ["python", "main.py"]