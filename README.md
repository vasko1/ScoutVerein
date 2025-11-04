# ScoutVerein

FastAPI-Backend für Scout-Verein: Rollen (Admin/Scout/Praktikant), Kinder, Berichte, Events, Zusagen und E-Mail-Benachrichtigungen (Konsolen-Demo).

## 🚀 Schnellstart

```bash
# 1) Virtuelle Umgebung (optional, aber empfohlen)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2) Abhängigkeiten installieren
pip install -r requirements.txt

# 3) Umgebung konfigurieren
cp .env.example .env  # SECRET_KEY später ändern!

# 4) Starten (entwicklungsmodus)
uvicorn app.main:app --reload
```

Öffne danach die interaktive API-Doku:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## 🔐 Default-Login (Bootstrap)

Beim ersten Start werden automatisch angelegt:
- Admin: `admin@verein.de` / `admin123`
- 2 Scouts, 1 Praktikant, 3 Kinder, 1 Event, 2 Berichte

> **Wichtig:** Logge dich als Admin ein und ändere dein Passwort über `/users/me/password` (POST, JSON: `{"new_password": "DEIN_NEUES_PASSWORT"}`).

## ✉️ Benachrichtigungen (Demo)

- Beim **Anlegen eines Kindes** oder **Erstellen eines Berichts** sowie **Zusage zu Event** wird eine E-Mail-Simulation in der Konsole ausgegeben.

## 📦 Endpunkte (Auswahl)

- `POST /auth/login` — erhalte JWT
- `GET /children` — Liste (Filter: name, birth_year, status)
- `POST /children` — Kind anlegen (Scout/Admin)
- `POST /reports` — Bericht anlegen (Scout/Admin) → mit Autor & Datum
- `GET /children/{id}/reports` — Berichte zu Kind
- `GET /events` / `POST /events` — Events auflisten/erstellen (Admin)
- `POST /events/{id}/attend` — Zusage durch Scout → Admin-Mail

## 🗂️ Rollenlogik

- **Admin**: volle Rechte, Events/Konten verwalten
- **Scout**: Kinder anlegen/bearbeiten (eigene Reports), Events zusagen
- **Praktikant**: Nur Leserechte

## 🧰 Hinweise

- DB: SQLite-Datei `scoutverein.db` im Projektroot (für Produktion PostgreSQL empfehlen)
- Migrations: Für den Start unnötig — später Alembic hinzufügen
