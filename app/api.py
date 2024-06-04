from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.email_verify.router import router as email_verify_router
from app.user.router import router as user_router

# app = FastAPI(docs_url=None, redoc_url=None)
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
# app.mount("/build", StaticFiles(directory="build"), name='frontent')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(email_verify_router, prefix="/api")
app.include_router(user_router, prefix="/api")

# route handlers
@app.exception_handler(404)
async def not_found_404(request, exc):
    return FileResponse("build/index.html")