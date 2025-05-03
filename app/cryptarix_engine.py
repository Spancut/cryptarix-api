import requests
import psycopg2

# --- Connect to PostgreSQL ---
def connect():
    return psycopg2.connect(
        host="localhost",
        database="Cryptarix",
        user="postgres",
        password="Chantec2008!"  # ← Change this if needed
    )

# --- Fetch token data from CoinGecko ---
def fetch_token_data(symbol: str):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "ids": symbol.lower()
    }

    response = requests.get(url, params=params)
    if response.status_code == 200 and response.json():
        data = response.json()[0]
        return {
            "name": data["name"],
            "symbol": data["symbol"],
            "price": data["current_price"],
            "volume": data["total_volume"]
        }
    else:
        print("Token not found or API error.")
        return None

# --- AlphaScore calculation logic ---
def calculate_alpha_score(price: float, volume: float) -> int:
    score = 0

    # Volume-based scoring
    if volume > 1_000_000_000:
        score += 50
    elif volume > 100_000_000:
        score += 40
    elif volume > 10_000_000:
        score += 30
    elif volume > 1_000_000:
        score += 20
    else:
        score += 10

    # Price-based scoring
    if price < 0.01:
        score += 30
    elif price < 0.1:
        score += 20
    elif price < 1:
        score += 10

    return min(score, 100)

# --- Insert or update token in the database ---
def insert_token(token_data: dict, alpha_score: int):
    conn = connect()
    cur = conn.cursor()

    query = """
    INSERT INTO tokens (symbol, name, price_usd, volume_24h, alpha_score, sentiment_score, risk_level, last_updated)
    VALUES (%s, %s, %s, %s, %s, %s, %s, now())
    ON CONFLICT (symbol) DO UPDATE SET
      price_usd = EXCLUDED.price_usd,
      volume_24h = EXCLUDED.volume_24h,
      alpha_score = EXCLUDED.alpha_score,
      sentiment_score = EXCLUDED.sentiment_score,
      risk_level = EXCLUDED.risk_level,
      last_updated = now();
    """

    cur.execute(query, (
        token_data["symbol"].upper(),
        token_data["name"],
        token_data["price"],
        token_data["volume"],
        alpha_score,
        70,         # Placeholder sentiment
        "medium"    # Placeholder risk
    ))

    conn.commit()
    cur.close()
    conn.close()

# --- Run script for a single token ---
if __name__ == "__main__":
    symbols = [
        "bitcoin", "ethereum", "solana", "dogecoin", "ripple",
        "chainlink", "cardano", "tron", "polkadot", "litecoin"
    ]

    for symbol in symbols:
        token = fetch_token_data(symbol)
        if token:
            score = calculate_alpha_score(token["price"], token["volume"])
            insert_token(token, score)
            print(f"{token['name']} AlphaScore {score} inserted.")
        else:
            print(f"❌ Failed to fetch {symbol}")

def generate_alpha_score(symbol: str) -> float:
    # TEMP fake scoring logic
    return len(symbol) * 3.14