import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from pydantic import BaseModel
from typing import Optional

# Load environment variables from.env file
load_dotenv()

# Database settings
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

# Create database engine
engine = create_engine(
    f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}',
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=1800,
    poolclass=NullPool
)

# Create database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base model for declarative classes
Base = declarative_base()

# FastAPI app
app = FastAPI()

# Route for health check
@app.get('/')
def health_check():
    return JSONResponse(content={'status': 'OK'}, media_type='application/json')

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()