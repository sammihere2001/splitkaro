# SplitKaro 💸

![CI](https://github.com/sammihere2001/splitkaro/actions/workflows/ci.yml/badge.svg)

A full-stack app (React frontend + FastAPI backend) for splitting shared expenses between flatmates, hostel friends or trip groups.
Log who paid for what, and SplitKaro works out a **short list of payments** that settles everyone up.

<!-- Demo video: add the Loom link here once it's recorded. -->

## Features

- **JWT authentication**: register, log in, protected routes; passwords hashed with bcrypt
- **Groups**: create a group and add members by email; non-members can't see a group
- **Expenses**: split equally between all members or a chosen subset
- **Balances**: who owes and who is owed, per group
- **Settle up**: a greedy algorithm that settles a group of *n* people in at most *n − 1* payments
- **Money handled in paisa (integers)** to avoid floating-point rounding errors
- **31 automated tests** (pytest) running on every push via **GitHub Actions**
- **Dockerized**: the whole stack (PostgreSQL + API + frontend) starts with one command, and CI
  builds the images and smoke-tests the running stack on every push

## Tech stack

| Layer | Tech |
|---|---|
| Frontend | React 19, React Router, Vite, Tailwind CSS |
| API | Python 3.13, FastAPI, Pydantic |
| Database | SQLAlchemy 2.0 ORM: PostgreSQL (Docker), MySQL also supported, SQLite for tests |
| Auth | OAuth2 password flow, JWT (PyJWT), bcrypt |
| Testing / CI | pytest, FastAPI TestClient, GitHub Actions |
| DevOps | Docker (multi-stage builds), Docker Compose, nginx |

## How settle-up works

Every expense changes each member's **balance**: the payer goes up by the full amount, and everyone
who shared it goes down by their share. The balances always add up to zero.

Settle-up turns those balances into payments:

1. Split people into **debtors** (balance below 0) and **creditors** (balance above 0). People at
   exactly 0 are already settled and are left out.
2. Take the first debtor and the first creditor. The debtor pays the creditor the **smaller** of
   what one owes and the other is owed.
3. At least one of the two is now at 0, so remove them. Repeat until nobody is left.

**Example:** Ali paid Rs 3,000 rent for three people, and Sara paid Rs 600 for groceries for herself
and Hamza. Balances: Ali +2,000, Sara −700, Hamza −1,300. Settle-up gives two payments:
Sara pays Ali 700, and Hamza pays Ali 1,300.

Because every payment fully settles at least one person, a group with *n* people who aren't
settled needs at most *n − 1* payments. The tests check every rule: everyone ends at 0, every amount
is positive, nobody pays themselves, and there are never more than *n − 1* payments.

## API endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Create an account |
| POST | `/auth/login` | Get a JWT access token |
| GET | `/auth/me` | Current user |
| POST | `/groups` | Create a group |
| GET | `/groups` | My groups |
| GET | `/groups/{id}` | Group details and members |
| POST | `/groups/{id}/members` | Add a member by email |
| POST | `/groups/{id}/expenses` | Add an expense |
| GET | `/groups/{id}/expenses` | List expenses |
| DELETE | `/groups/{id}/expenses/{expense_id}` | Delete an expense (payer or group creator) |
| GET | `/groups/{id}/balances` | Net balance of each member |
| GET | `/groups/{id}/settle-up` | Payments that settle the group |

Interactive docs (Swagger UI) are available at `http://localhost:8000/docs` when running locally.

## Run with Docker (easiest)

Needs [Docker Desktop](https://www.docker.com/products/docker-desktop/).

```bash
git clone https://github.com/sammihere2001/splitkaro.git
cd splitkaro
docker compose up --build
```

- App: http://localhost:8080
- API docs: http://localhost:8000/docs

Stop with `Ctrl+C`. `docker compose down -v` also deletes the database.

## Run locally without Docker

```bash
git clone https://github.com/sammihere2001/splitkaro.git
cd splitkaro
python -m venv .venv
.venv\Scripts\activate        # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env        # macOS/Linux: cp .env.example .env
uvicorn app.main:app --reload
```

Open http://localhost:8000/docs.

Then start the frontend in a second terminal (needs Node.js 20+):

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173.

> **Windows PowerShell:** if `npm` fails with "running scripts is disabled on this system",
> use `npm.cmd run dev` instead (or run the commands from Command Prompt).

To use MySQL or PostgreSQL instead of SQLite, create a `splitkaro` database and set `DATABASE_URL`
in `.env` (see `.env.example`).

## Run tests

```bash
pytest -v
```

## Project structure

```
app/
  main.py              # FastAPI app, routers, CORS
  config.py            # settings from environment variables
  database.py          # SQLAlchemy engine and session
  models.py            # database tables
  schemas.py           # request/response models (Pydantic)
  security.py          # password hashing and JWT
  deps.py              # auth and group-membership dependencies
  money.py             # rupees <-> paisa conversion
  routers/             # auth, groups, expenses endpoints
  services/settlement.py   # split, balance and settle-up logic
tests/                 # pytest suite
frontend/
  src/api.js           # fetch wrapper for the API
  src/auth.jsx         # login state shared with every page
  src/pages/           # Login, Register, Groups, GroupDetail
  src/components/      # forms and reusable UI pieces
  Dockerfile           # builds the app, then serves it with nginx
.github/workflows/     # CI pipeline: tests + Docker smoke test
Dockerfile             # backend image
compose.yaml           # PostgreSQL + API + frontend together
render.yaml            # deployment config for Render (prepared, not live yet)
```

## Roadmap

- [x] React frontend
- [x] Docker + Docker Compose (PostgreSQL + API + frontend)
- [ ] Live deployment (config for Render + Neon is ready in `render.yaml`)
- [ ] End-to-end tests with Playwright
- [ ] Database migrations with Alembic
- [ ] Unequal splits (by amount or percentage)

## Author

**Muhammad Saim**, Software Engineering graduate, Karachi
[GitHub](https://github.com/sammihere2001)
