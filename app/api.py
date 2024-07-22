from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.email_verify.router import router as email_verify_router
from app.user.router import router as user_router
from app.glassbiller.router import router as glassbiller_router
from app.qbo.router import router as qbo_router

# app = FastAPI(docs_url=None, redoc_url=None)
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(email_verify_router, prefix="/api")
app.include_router(user_router, prefix="/api")
app.include_router(glassbiller_router, prefix="/api/glassbiller")
app.include_router(qbo_router, prefix="/api/qbo")

# route handlers
@app.get("/")
async def index():
    return FileResponse("static/index.html")