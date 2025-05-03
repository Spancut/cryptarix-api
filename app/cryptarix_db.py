import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from pydantic import BaseModel

# Load variables from .env file
load_dotenv()

# Get the database URL from the environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# Set up the database engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Token(BaseModel):
    symbol: str
    name: str
    price_usd: float