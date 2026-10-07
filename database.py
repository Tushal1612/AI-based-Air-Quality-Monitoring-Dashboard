import sqlite3
from pathlib import Path
import pandas as pd

DB_FILE = Path("data/air_quality.db")

def get_connection():
    DB_FILE.parent.mkdir(exist_ok=True)
    return sqlite3.connect(DB_FILE)

def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                location TEXT NOT NULL,
                pm25 REAL NOT NULL,
                pm10 REAL NOT NULL,
                co2 REAL NOT NULL,
                temperature REAL NOT NULL,
                humidity REAL NOT NULL,
                prediction TEXT NOT NULL
            )
        """)
        conn.commit()

def insert_reading(timestamp, location, pm25, pm10, co2, temperature, humidity, prediction):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO readings
            (timestamp, location, pm25, pm10, co2, temperature, humidity, prediction)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            str(timestamp), location, float(pm25), float(pm10), float(co2),
            float(temperature), float(humidity), prediction
        ))
        conn.commit()

def get_readings(location=None, limit=500):
    query = "SELECT * FROM readings"
    params = []

    if location:
        query += " WHERE location = ?"
        params.append(location)

    query += " ORDER BY timestamp DESC LIMIT ?"
    params.append(limit)

    with get_connection() as conn:
        return pd.read_sql_query(query, conn, params=params)
