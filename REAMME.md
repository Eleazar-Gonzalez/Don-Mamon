# Student Housing & Roommate Finder API (MVP)

## Run Locally
pip install -r requirements.txt
uvicorn app:app --reload

Open: http://localhost:8000/docs

## Run with Docker
docker build -t housing-api .
docker run -p 8080:8080 housing-api

## Endpoints
/listings (POST, GET, PUT, DELETE)
/roommates (POST, GET, PUT, DELETE)

## CI
GitHub Actions workflow included.

## Limitations
No auth, no matching algorithm, SQLite only.
