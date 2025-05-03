import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List

# Load environment variables
load_dotenv()

# Connect to database
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Pydantic model used for validation and POST body
class Token(BaseModel):
    symbol: str
    name: str
    price_usd: float

# Temporary in-memory token list (acts like a fake DB for now)
_db: List[Token] = []

def get_tokens():
    return [token.dict() for token in _db]

def add_token(token: Token):
    _db.append(token)