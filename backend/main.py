from configuration import config
from configuration.config import app as app


@app.get("/dummy-endpoint")
async def root():
    return {"message": "Hello from the fastAPI backend!"}