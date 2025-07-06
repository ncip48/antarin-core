# 🙵 Ojek Online Realtime System

Sistem backend ojek online modern dengan arsitektur **asynchronous, real-time**, dan **terdistribusi**. Proyek ini mengintegrasikan **Django**, **PostgreSQL + PostGIS**, **Celery**, **Redis**, **RabbitMQ**, **WebSocket via Daphne**, dan **Flower** untuk monitoring task worker. Cocok untuk aplikasi ride-hailing dan logistik berbasis lokasi.

---

## 🚀 Fitur Utama

- ✅ **Autentikasi & Manajemen User**
- 🧽 **Tracking Lokasi Realtime** (driver dan customer)
- 📡 **WebSocket (Django Channels + Daphne)** untuk komunikasi langsung
- 🐇 **Queueing System dengan Celery + RabbitMQ**
- 📍 **PostGIS** untuk penyimpanan titik lokasi (GPS) driver
- 🌼 **Flower Dashboard** untuk monitoring Celery tasks

---

## 📦 Stack Teknologi

| Komponen   | Teknologi                |
| ---------- | ------------------------ |
| Backend    | Django + Django Channels |
| Database   | PostgreSQL + PostGIS     |
| Task Queue | Celery                   |
| Broker     | RabbitMQ                 |
| Caching    | Redis                    |
| WebSocket  | Daphne (ASGI server)     |
| Monitoring | Flower (untuk Celery)    |
| Dev Tools  | Docker & Docker Compose  |

---

## 🧪 Cara Menjalankan (Local Dev)

1. **Buat file **`` di root project:

```env
# PostgreSQL
POSTGRES_DB=ojek_db
POSTGRES_USER=ojek_user
POSTGRES_PASSWORD=ojek_pass

# Django
DJANGO_DB_NAME=ojek_db
DJANGO_DB_USER=ojek_user
DJANGO_DB_PASSWORD=ojek_pass
DJANGO_DB_HOST=postgres
DJANGO_DB_PORT=5432

# pgAdmin
PGADMIN_DEFAULT_EMAIL=admin@ojek.com
PGADMIN_DEFAULT_PASSWORD=admin123
```

2. **Build dan Jalankan semua container:**

```bash
docker compose up --build
```

3. **Akses layanan:**

| Layanan          | URL                                              |
| ---------------- | ------------------------------------------------ |
| Django API       | [http://localhost:8000](http://localhost:8000)   |
| Daphne WebSocket | ws\://localhost:8001/ws/driver/ (example)        |
| pgAdmin          | [http://localhost:5050](http://localhost:5050)   |
| Flower           | [http://localhost:5555](http://localhost:5555)   |
| RabbitMQ Admin   | [http://localhost:15672](http://localhost:15672) |

---

## 🔧 Struktur Penting

```
project-root/
├── core/                # Django main project
├── services/booking/    # Modul booking, konsumer websocket, dan celery tasks
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

---

## 📡 WebSocket Endpoint

| Endpoint        | Deskripsi            |
| --------------- | -------------------- |
| `/ws/driver/`   | Untuk driver login   |
| `/ws/customer/` | Untuk customer login |

> Gunakan auth token/session yang tepat agar `scope["user"]` bisa diakses dalam Django Channels middleware.

---

## 🌼 Monitoring Flower

Flower akan otomatis memonitor celery worker melalui RabbitMQ.\
Akses Flower di [http://localhost:5555](http://localhost:5555)

---

## ❓ Contoh WebSocket Ping Test (HTML)

```html
<script>
  const socket = new WebSocket("ws://localhost:8001/ws/customer/");

  socket.onopen = () => {
    console.log("Connected to WS");
    socket.send(JSON.stringify({ action: "ping" }));
  };

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log("WS Message:", data);
  };
</script>
```

---

## ✅ TODO (Pengembangan Selanjutnya)

- ***

## 💡 Kontribusi

Pull Request dan ide baru sangat diterima!\
Silakan buat issue jika ada pertanyaan, bug, atau fitur tambahan.

---

## 🧠 Lisensi

Open source untuk pembelajaran dan eksplorasi. Silakan gunakan untuk keperluan non-komersial atau edukasi.
