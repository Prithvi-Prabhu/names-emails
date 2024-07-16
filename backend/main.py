from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from databases import Database
from models import users, metadata
import uvicorn

DATABASE_URL = "mysql+aiomysql://root:1301@localhost:3306/codeclub"

# Set up the Database and SQLAlchemy engine
database = Database(DATABASE_URL)
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

app = FastAPI()

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins. Adjust this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserIn(BaseModel):
    name: str
    email: str

@app.on_event("startup")
async def startup():
    # Connect to the database
    await database.connect()
    # Create tables in the database
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/users/")
async def create_user(user: UserIn):
    query = users.insert().values(name=user.name, email=user.email)
    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
