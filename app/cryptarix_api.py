from fastapi import FastAPI
from typing import List
import psycopg2
from pydantic import BaseModel

app = FastAPI()

# 🔐 Replace this with your actual PostgreSQL password
DB_PASSWORD = "Chantec2008!"

class Token(BaseModel):
    symbol: str
    name: str
    price_usd: float
    alpha_score: int

def connect():
    return psycopg2.connect(
        host="localhost",
        database="Cryptarix",
        user="postgres",
        password=DB_PASSWORD
    )

@app.get("/tokens", response_model=List[Token])
def get_tokens():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT symbol, name, price_usd, alpha_score FROM tokens;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return [
        Token(symbol=row[0], name=row[1], price_usd=row[2], alpha_score=row[3])
        for row in rows
    ]
@app.post("/add_token")
def add_token(token: Token):
    conn = connect()
    cur = conn.cursor()

    query = """
    INSERT INTO tokens (symbol, name, price_usd, volume_24h, alpha_score, sentiment_score, risk_level, last_updated)
    VALUES (%s, %s, %s, %s, %s, %s, %s, now());
    """

    # Just for now: default some fields
    cur.execute(query, (
        token.symbol,
        token.name,
        token.price_usd,
        1000000,          # volume_24h placeholder
        token.alpha_score,
        75,               # sentiment_score placeholder
        "low"             # risk_level placeholder
    ))

    conn.commit()
    cur.close()
    conn.close()

    return {"message": f"{token.symbol} inserted successfully"}