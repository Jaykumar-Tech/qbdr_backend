import uvicorn

from app.api import app as qbdr_app

app = qbdr_app

if __name__ == "__main__":
    uvicorn.run(app)