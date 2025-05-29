from fastapi import FastAPI # type: ignore
from models import create_table
from database import get_connection
import requests,os # type: ignore
from dotenv import load_dotenv # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore

app = FastAPI()
load_dotenv()

create_table()

#Allow CORS for frontend

app.add_middleware(
    CORSMiddleware,
    allow_origins=["soccer-react-frontend.vercel.app"],
    allow_methods=["*"],
    allow_headers=["*"]
)
API_URL = "https://api.football-data.org/v4/matches"

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY not found in environment variables!")

HEADERS = {"X-Auth-Token":API_KEY}

@app.get("/matches")

def fetch_matches():
    response = requests.get(API_URL,headers=HEADERS)
    if response.status_code != 200:
        return {"error": "Failed to fetch match data", "status_code": response.status_code}
    data = response.json()
    upcoming = []

    conn = get_connection()
    cursor = conn.cursor()

    for match in data.get("matches",[]):
        home = match["homeTeam"]["name"]
        away = match["awayTeam"]["name"]
        date = match["utcDate"][:19].replace("T"," ")

        #saving to DB

        cursor.execute(
            "INSERT INTO Matches (home_team, away_team, match_time) VALUES (%s,%s,%s)",
            (home,away,date)
        )

        upcoming.append({
            "home":home,
            "away":away,
            "time":date
        })

    conn.commit()
    cursor.close()
    conn.close()
    return upcoming