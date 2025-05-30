from fastapi import FastAPI # type: ignore
from models import create_table
from database import get_connection
import requests, os # type: ignore
from dotenv import load_dotenv # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from datetime import datetime

app = FastAPI()
load_dotenv()

create_table()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://soccer-react-frontend.vercel.app", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

API_URL = "https://api.football-data.org/v4/matches"
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("API_KEY not found in environment variables!")

HEADERS = {"X-Auth-Token": API_KEY}

@app.get("/matches")
def fetch_matches():
    response = requests.get(API_URL, headers=HEADERS)
    if response.status_code != 200:
        return {"error": "Failed to fetch match data", "status_code": response.status_code}
    
    data = response.json()
    upcoming = []
    conn = get_connection()
    cursor = conn.cursor()

    for match in data.get("matches", []):
        home = match["homeTeam"]["name"]
        away = match["awayTeam"]["name"]
        date_str = match["utcDate"][:19].replace("T", " ")  # '2024-06-01 15:00:00'
        date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

        # Check if already exists in DB
        cursor.execute(
            "SELECT * FROM Matches WHERE home_team=%s AND away_team=%s AND match_time=%s",
            (home, away, date_obj)
        )
        if cursor.fetchone() is None:
            cursor.execute(
                "INSERT INTO Matches (home_team, away_team, match_time) VALUES (%s, %s, %s)",
                (home, away, date_obj)
            )

        # Append to response
        upcoming.append({
            "home": home,
            "away": away,
            "time": date_obj.isoformat()  # ISO string to simplify frontend Date parsing
        })

    conn.commit()
    cursor.close()
    conn.close()
    return upcoming
