FROM python:3.12-slim

# Tambah dependencies
RUN apt-get update && apt-get install -y \
    binutils \
    libproj-dev \
    gdal-bin \
    libgdal-dev \
    gcc \
    g++ \
    python3-dev \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Set environment untuk GDAL agar tidak error di pip
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

WORKDIR /code

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY config/supervisord.conf /etc/supervisord.conf

COPY . .

CMD ["supervisord", "-c", "/etc/supervisord.conf"]
