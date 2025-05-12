# 📰 AI-Powered Brief Generator

Generate short, AI-written summaries on any topic and store them for later use. Built with FastAPI, OpenAI, and SQLAlchemy.

---

## 🚀 Features

* Submit topics + tone and receive a short AI-generated brief
* Store briefs in a PostgreSQL database
* Retrieve a paginated list of recent briefs
* Scheduler support with secure API key access
* Global error handling and test coverage

---

## 🛠️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/your-user/daily_brief_ai_etl.git
cd daily_brief_ai_etl
```

### 2. Create a `.env` File

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```env
OPENAI_API_KEY=sk-...
```

### 3. Start PostgreSQL with Docker

```bash
docker compose up -d
```

This starts a local PostgreSQL database on port `5432` using the credentials in `.env.example`.

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Start the API Server

```bash
./run.sh
```

The app runs at: `http://127.0.0.1:8000`

---

## 📬 API Endpoints

### `POST /api/v1/briefs`

Submit a request to generate a brief:

```json
{
  "topics": "AI in healthcare",
  "tone": "professional"
}
```

### `GET /api/v1/briefs`

Returns a paginated list of briefs:

```
/api/v1/briefs?limit=10&offset=0
```

### `POST /api/v1/briefs/run-schedule`

Trigger a scheduled brief generation (requires `x-api-key` header)

---

## ✅ Running Tests

```bash
pytest -v
```
---

## 🧪 Running Tests

This project uses `pytest` for testing, along with `pytest-mock` for mocking external dependencies like the OpenAI API.

### 📦 Install Test Dependencies
If you haven't already:
```bash
pip install -r requirements.txt


---

## 🧠 Project Structure

```
app/
├── api/            # Versioned API routes
├── db/             # Database session & CRUD logic
├── models/         # Pydantic and SQLAlchemy models
├── services/       # OpenAI + scheduling logic
│   ├── brief_generator.py   # Calls OpenAI API
│   ├── scheduler.py         # Core scheduler logic
│   └── scheduler_service.py # Standalone service that runs scheduled briefs
├── security/       # API key verification
├── main.py         # FastAPI entry point
```

---

## 🐳 Docker

This project uses Docker to run PostgreSQL locally for development. You can adapt this setup for production deployments to Render, Railway, Fly.io, etc.

---

## 🧩 To-Do Highlights

* [x] Modularize routes, models, DB
* [x] Add test coverage and mocking
* [x] Secure scheduler route
* [x] Switch from SQLite → PostgreSQL
* [x] Containerize app server
* [x] Add CI/CD pipeline
* [ ] Deploy to cloud host

---

Built with ❤️ by \[Your Name]
