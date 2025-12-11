from fastapi import FastAPI
from app.api import endpoints

# Create the FastAPI application
app = FastAPI(title="Mini Battleship")

# Include all routes from our API router
app.include_router(endpoints.router)

@app.get("/")
def root():
    return {"message": "Welcome to Mini Battleship API"}
