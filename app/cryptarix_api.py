from fastapi import FastAPI
from app.cryptarix_db import get_tokens, add_token, Token
from app.cryptarix_engine import generate_alpha_score

app = FastAPI()

@app.get("/tokens")
def read_tokens():
    tokens = get_tokens()
    for token in tokens:
        token["alpha_score"] = generate_alpha_score(token["symbol"])
    return tokens

@app.post("/tokens")
def create_token(token: Token):
    add_token(token)
    return {"message": f"{token.name} added successfully."}