# Използваме официален Python образ
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Копирай requirements и инсталирай
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Копирай всички файлове на проекта
COPY . .

# Експонираме порт
EXPOSE 8000

# Стартираме FastAPI с uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
