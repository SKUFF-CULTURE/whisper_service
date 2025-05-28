# Используем официальный образ NVIDIA с CUDA
FROM nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04

# Устанавливаем зависимости
# Устанавливаем Python 3.11 из стандартных репозиториев Ubuntu 22.04
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.11 \
    python3.11-dev \
    python3.11-venv \
    python3.11-distutils \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем pip для Python 3.11
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11

# Создаем и активируем venv
RUN python3.11 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем Python-зависимости
RUN pip3 install --no-cache-dir -r requirements.txt

# Копируем ваш скрипт
COPY . .
COPY audio/ ./audio/

# Указываем команду для запуска
CMD ["python3", "pipeline.py"]