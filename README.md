# SplitKaro 💸

![CI](https://github.com/sammihere2001/splitkaro/actions/workflows/ci.yml/badge.svg)

A full-stack app (React frontend + FastAPI backend) for splitting shared expenses between flatmates, hostel friends or trip groups.
Log who paid for what, and SplitKaro works out a **short list of payments** that settles everyone up.

> 🎥 **Demo video:** _add your Loom link here_

## Features

- **JWT authentication**: register, log in, protected routes; passwords hashed with bcrypt
- **Groups**: create a group and add members by email; non-members can't see a group
- **Expenses**: split equally between all members or a chosen subset
- **Balances**: who owes and who is owed, per group
- **Settle up**: a greedy algorithm that settles a group of *n* people in at most *n − 1* payments
- **Money handled in paisa (integers)** to avoid floating-point rounding errors
- **Automated tests** (pytest) running on every push via **GitHub Actions**

## Tech stack

| Layer | Tech |
|---|---|
| Frontend | React 19, React Router, Vite, Tailwind CSS |
| API | Python 3.13, FastAPI, Pydantic |
| Database | SQLAlchemy 2.0 ORM, MySQL (SQLite for local dev and tests) |
| Auth | OAuth2 password flow, JWT (PyJWT), bcrypt |
| Testing / CI | pytest, FastAPI TestClient, GitHub Actions |

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

## How settle-up works

_Write-up coming soon._

<!-- TODO: explain your algorithm here in your own words: the idea, an example, and its time complexity. -->

## Run locally

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

To use MySQL instead of SQLite, create a `splitkaro` database and set `DATABASE_URL` in `.env`
(see `.env.example`).

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
.github/workflows/     # CI pipeline
```

## Roadmap

- [x] React frontend
- [ ] Docker + docker-compose (API + MySQL)
- [ ] Deploy to the cloud
- [ ] Database migrations with Alembic
- [ ] Unequal splits (by amount or percentage)

## Author

**Muhammad Saim**, Software Engineering graduate, Karachi
[GitHub](https://github.com/sammihere2001)
