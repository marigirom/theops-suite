import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, Session

DB_URL = (
    f"postgresql://{os.environ['DB_USER']}:{os.environ['DB_PASS']}"
    f"@{os.environ['DB_HOST']}:{os.environ.get('DB_PORT', '5432')}"
    f"/{os.environ['DB_NAME']}"
)
engine = create_engine(DB_URL)

class Base(DeclarativeBase):
    pass

class Item(Base):
    __tablename__ = "items"
    id   = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

app = FastAPI()

@app.on_event("startup")
def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"WARNING: could not create tables at startup: {e}")

class ItemIn(BaseModel):
    name: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/items")
def list_items():
    with Session(engine) as session:
        return session.query(Item).all()

@app.post("/items", status_code=201)
def create_item(item: ItemIn):
    with Session(engine) as session:
        db_item = Item(name=item.name)
        session.add(db_item)
        session.commit()
        session.refresh(db_item)
        return db_item
