FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PLAYWRIGHT_BROWSERS_PATH=/root/.cache/ms-playwright

# Утилиты + зависимости Chromium
RUN apt-get update && apt-get install -y \
    bash curl wget git vim nano htop tree \
    procps net-tools iputils-ping dnsutils \
    libglib2.0-0 libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 \
    libcups2 libdrm2 libdbus-1-3 libxkbcommon0 libxcomposite1 \
    libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2 \
    fonts-liberation xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Playwright + скачивание Chromium ПРИ СБОРКЕ
RUN pip install --no-cache-dir playwright && \
    playwright install chromium && \
    playwright install-deps chromium

WORKDIR /workspace
CMD ["tail", "-f", "/dev/null"]
