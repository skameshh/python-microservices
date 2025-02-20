from fastapi import FastAPI
from routes import router
from db import Base, engine

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# Register Routes
app.include_router(router, prefix="/auth")

@app.get("/")
def read_root():
    return {"message": "Auth Service is Running"}
