import psycopg2
from datetime import datetime

# 🔌 Connect to PostgreSQL
def connect():
    return psycopg2.connect(
        host="localhost",
        database="Cryptarix",           # 🔁 Make sure this matches your DB name exactly
        user="postgres",                # ✅ This is the default admin user
        password="Chantec2008!"   # 🔁 Replace with your real password
    )

# 💾 Insert a new token
def insert_token(symbol, name, price_usd, volume_24h, alpha_score, sentiment_score, risk_level):
    conn = connect()
    cur = conn.cursor()

    query = """
    INSERT INTO tokens (symbol, name, price_usd, volume_24h, alpha_score, sentiment_score, risk_level, last_updated)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """
    cur.execute(query, (
        symbol,
        name,
        price_usd,
        volume_24h,
        alpha_score,
        sentiment_score,
        risk_level,
        datetime.now()
    ))

    conn.commit()
    cur.close()
    conn.close()
    print(f"Inserted {symbol} into database.")

# 📥 Read all token records
def get_all_tokens():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT symbol, name, price_usd, alpha_score FROM tokens;")
    rows = cur.fetchall()

    for row in rows:
        symbol, name, price, score = row
        print(f"{symbol} - {name} - ${price} - AlphaScore: {score}")

    cur.close()
    conn.close()

# ✅ Uncomment to insert a new record
# insert_token("DOGE", "Dogecoin", 0.065, 25000000, 82, 78, "medium")

# 🔍 Fetch and display all records
get_all_tokens()