from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

@app.get("/tokens")
def get_tokens():
    try:
        print(">> Hitting /tokens route...")

        conn = psycopg2.connect(
            host="localhost",          # or update with actual Render config
            database="your_db_name",   # UPDATE THIS
            user="your_db_user",       # UPDATE THIS
            password="your_password",  # UPDATE THIS
            port="5432"
        )

        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT symbol, name, price_usd, alpha_score FROM tokens")
        rows = cur.fetchall()

        cur.close()
        conn.close()

        return rows

    except Exception as e:
        print("🔥 ERROR in /tokens:", str(e))
        return {"error": str(e)}

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